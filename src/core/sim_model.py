import logging
from collections import defaultdict

from device.road_side_unit import RoadsideUnit
from mesa import DataCollector, Model
from mesa.space import ContinuousSpace

from src.core.common_constants import CoordSpace, DeviceName
from src.core.constants import Defaults, Stage
from src.core.scheduler import OrderedMultiStageScheduler, TypeStage
from src.device.base_station import BaseStation
from src.device.controller import CentralController
from src.device.vehicle import Vehicle
from src.orchestrator.cloud_orchestrator import CloudOrchestrator
from src.orchestrator.edge_orchestrator import EdgeOrchestrator

logger = logging.getLogger(__name__)


class SimModel(Model):
    def __init__(
        self,
        vehicles: dict[int, Vehicle],
        base_stations: dict[int, BaseStation],
        controllers: dict[int, CentralController],
        roadside_units: dict[int, RoadsideUnit],
        edge_orchestrator: EdgeOrchestrator,
        cloud_orchestrator: CloudOrchestrator,
        space_settings: dict,
        start_time: int,
        end_time: int,
    ):
        """
        Initialize the simulation model.
        """
        super().__init__()
        self._vehicles: dict[int, Vehicle] = vehicles
        self._base_stations: dict[int, BaseStation] = base_stations
        self._controllers: dict[int, CentralController] = controllers
        self._roadside_units: dict[int, RoadsideUnit] = roadside_units

        self._edge_orchestrator: EdgeOrchestrator = edge_orchestrator
        self._cloud_orchestrator: CloudOrchestrator = cloud_orchestrator

        self._vehicle_activation_times: dict[int, set[int]] = defaultdict(set)
        self._vehicle_deactivation_times: dict[int, set[int]] = defaultdict(set)
        self._roadside_unit_activation_times: dict[int, set[int]] = defaultdict(set)
        self._roadside_unit_deactivation_times: dict[int, set[int]] = defaultdict(set)
        self._base_station_activation_times: dict[int, set[int]] = defaultdict(set)
        self._base_station_deactivation_times: dict[int, set[int]] = defaultdict(set)
        self._controller_activation_times: dict[int, set[int]] = defaultdict(set)
        self._controller_deactivation_times: dict[int, set[int]] = defaultdict(set)

        self._space_settings: dict = space_settings
        self._start_time: int = start_time
        self._end_time: int = end_time
        self.current_time: int = -1

    def do_model_setup(self) -> None:
        """
        Set up the model before the simulation starts.
        """
        logger.debug("Initializing the scheduler.")
        self._initialize_scheduler()

        logger.debug("Initializing the 2D space.")
        self._initialize_space()

        logger.debug("Add orchestrators to the scheduler.")
        self._add_orchestrators_to_scheduler()

        logger.debug("Reading activation and deactivation times for all the devices.")
        self.save_device_activation_times()

        # logger.debug("Assign simulation model to all the devices.")
        # self.assign_sim_model_to_devices()

        logger.debug("Create data collector.")
        self._create_data_collector()

    def step(self) -> None:
        """
        Step through the simulation model.
        """
        logger.info(f"Running step {self.current_time}")
        logger.debug(
            f"Active vehicles: {self._edge_orchestrator.active_vehicle_count()}"
        )
        logger.debug(
            f"Active base stations: {self._edge_orchestrator.active_base_station_count()}"
        )
        logger.debug(
            f"Active controllers: {self._cloud_orchestrator.active_controller_count()}"
        )

        # Collect data from the previous time step
        self.data_collector.collect(self)
        self._do_device_activations()
        self.schedule.step()
        self._do_device_deactivations()

    def _initialize_scheduler(self) -> None:
        """
        Initialize the scheduler.

        The order of the types and stages is important. The order in which the types
        and stages are added to the scheduler is the order of execution of the stages.
        """
        type_stage_list: list[TypeStage] = []
        type_stage_list.extend(self._get_uplink_stages_in_order())
        type_stage_list.extend(self._get_downlink_stages_in_order())
        self.schedule = OrderedMultiStageScheduler(self, type_stage_list, shuffle=True)

    def _get_uplink_stages_in_order(self) -> list[TypeStage]:
        """
        Add the uplink stages to the scheduler.

        Order is as follows - Vehicle, Edge Orchestrator, Base Station,
        Controller
        """
        type_stage_list: list[TypeStage] = []
        vehicle_uplink = TypeStage(
            type=type(list(self._vehicles.values())[0]), stage=Stage.UPLINK
        )
        type_stage_list.append(vehicle_uplink)

        rsu_uplink = TypeStage(
            type=type(list(self._roadside_units.values())[0]), stage=Stage.UPLINK
        )
        type_stage_list.append(rsu_uplink)

        edge_orchestrator_uplink = TypeStage(
            type=type(self._edge_orchestrator), stage=Stage.UPLINK
        )
        type_stage_list.append(edge_orchestrator_uplink)

        base_station_uplink = TypeStage(
            type=type(list(self._base_stations.values())[0]), stage=Stage.UPLINK
        )
        type_stage_list.append(base_station_uplink)

        cloud_orchestrator_uplink = TypeStage(
            type=type(self._cloud_orchestrator), stage=Stage.UPLINK
        )
        type_stage_list.append(cloud_orchestrator_uplink)

        controller_uplink = TypeStage(
            type=type(list(self._controllers.values())[0]), stage=Stage.UPLINK
        )
        type_stage_list.append(controller_uplink)
        return type_stage_list

    def _get_downlink_stages_in_order(self) -> list[TypeStage]:
        """
        Add the downlink stages to the scheduler.

        Order is as follows - Controller, Cloud Orchestrator, Base Station,
        Edge Orchestrator, Vehicles
        """
        type_stage_list: list[TypeStage] = []
        controller_downlink = TypeStage(
            type=type(list(self._controllers.values())[0]), stage=Stage.DOWNLINK
        )
        type_stage_list.append(controller_downlink)

        cloud_orchestrator_downlink = TypeStage(
            type=type(self._cloud_orchestrator), stage=Stage.DOWNLINK
        )
        type_stage_list.append(cloud_orchestrator_downlink)

        base_station_downlink = TypeStage(
            type=type(list(self._base_stations.values())[0]), stage=Stage.DOWNLINK
        )
        type_stage_list.append(base_station_downlink)

        edge_orchestrator_downlink = TypeStage(
            type=type(self._edge_orchestrator), stage=Stage.DOWNLINK
        )
        type_stage_list.append(edge_orchestrator_downlink)

        rsu_downlink = TypeStage(
            type=type(list(self._roadside_units.values())[0]), stage=Stage.DOWNLINK
        )
        type_stage_list.append(rsu_downlink)

        vehicle_downlink = TypeStage(
            type=type(list(self._vehicles.values())[0]), stage=Stage.DOWNLINK
        )
        type_stage_list.append(vehicle_downlink)
        return type_stage_list

    def _initialize_space(self) -> None:
        """
        Initialize the space.
        """
        self.space = ContinuousSpace(
            x_max=self._space_settings[CoordSpace.X_MAX] + Defaults.BUFFER_SPACE,
            y_max=self._space_settings[CoordSpace.Y_MAX] + Defaults.BUFFER_SPACE,
            torus=False,
            x_min=self._space_settings[CoordSpace.X_MIN] - Defaults.BUFFER_SPACE,
            y_min=self._space_settings[CoordSpace.Y_MIN] - Defaults.BUFFER_SPACE,
        )

    def save_device_activation_times(self) -> None:
        """
        Extract the activation and deactivation times of the devices.
        """
        logger.debug("Extracting activation and deactivation times for vehicles.")
        for vehicle_id, vehicle in self._vehicles.items():
            start_times = vehicle.get_activation_times()
            end_times = vehicle.get_deactivation_times()
            logger.debug(
                f"Vehicle {vehicle_id} has activation times {start_times} "
                f"and deactivation times {end_times}."
            )
            self._vehicle_activation_times[vehicle_id].update(start_times)
            self._vehicle_deactivation_times[vehicle_id].update(end_times)

        logger.debug("Extracting activation and deactivation times for roadside units.")
        for roadside_unit_id, roadside_unit in self._roadside_units.items():
            start_times = roadside_unit.get_activation_times()
            end_times = roadside_unit.get_deactivation_times()
            logger.debug(
                f"Roadside unit {roadside_unit_id} has activation times {start_times} "
                f"and deactivation times {end_times}."
            )
            self._roadside_unit_activation_times[roadside_unit_id].update(start_times)
            self._roadside_unit_deactivation_times[roadside_unit_id].update(end_times)

        logger.debug("Extracting activation and deactivation times for base stations.")
        for base_station_id, base_station in self._base_stations.items():
            start_times = base_station.get_activation_times()
            end_times = base_station.get_deactivation_times()
            logger.debug(
                f"Base station {base_station_id} has activation times {start_times}"
                f" and deactivation times {end_times}."
            )
            self._base_station_activation_times[base_station_id].update(start_times)
            self._base_station_deactivation_times[base_station_id].update(end_times)

        logger.debug("Extracting activation and deactivation times for controllers.")
        for controller_id, controller in self._controllers.items():
            start_times = controller.get_activation_times()
            end_times = controller.get_deactivation_times()
            logger.debug(
                f"Controller {controller_id} has activation times {start_times} "
                f"and deactivation times {end_times}."
            )
            self._controller_activation_times[controller_id].update(start_times)
            self._controller_deactivation_times[controller_id].update(end_times)

    def _add_orchestrators_to_scheduler(self) -> None:
        """
        Add the orchestrators to the scheduler.
        """
        self._edge_orchestrator.model = self
        self._cloud_orchestrator.model = self

        self.schedule.add(self._edge_orchestrator)
        self.schedule.add(self._cloud_orchestrator)

    def _create_data_collector(self) -> None:
        """
        Create the data collector.
        """
        self.data_collector = DataCollector(
            model_reporters={
                "active_vehicles": self._edge_orchestrator.active_vehicle_count,
                "active_base_stations": self._edge_orchestrator.active_base_station_count,
                "total_data": self._cloud_orchestrator.get_total_data_at_controllers,
                "visible_vehicles": self._cloud_orchestrator.get_visible_vehicles,
                "side_link_data": self._edge_orchestrator.get_total_sidelink_data_size,
                "data_sizes_by_type": self._cloud_orchestrator.get_data_sizes_by_type,
                "data_counts_by_type": self._cloud_orchestrator.get_data_counts_by_type,
            },
            agent_reporters={
                "vehicle_data": lambda v: v.data_generated_at_device
                if v.type == DeviceName.VEHICLES
                else None,
                "vehicles_in_range": lambda b: b.vehicles_in_range
                if b.type != DeviceName.CLOUD_ORCHESTRATOR
                and b.type != DeviceName.EDGE_ORCHESTRATOR
                else None,
                "agent_type": lambda a: a.type,
            },
        )

    def _save_activation_data(
        self,
        activate_time: ndarray[int],
        deactivate_time: ndarray[int],
        device_id: int,
        device_type: str,
    ) -> None:
        """
        Update the activation time of the device.
        """
        for i in range(len(activate_time)):
            start_time_stamp = activate_time[i]
            if start_time_stamp not in self._activation_times[device_type]:
                self._activation_times[device_type][start_time_stamp] = {device_id}
            else:
                self._activation_times[device_type][start_time_stamp].add(device_id)

            end_time_stamp = deactivate_time[i]
            if end_time_stamp not in self._deactivation_times[device_type]:
                self._deactivation_times[device_type][end_time_stamp] = {device_id}
            else:
                self._deactivation_times[device_type][end_time_stamp].add(device_id)

    def step(self) -> None:
        """
        Step through the simulation model.
        """
        logger.info(f"Running step {self._current_time}")
        logger.debug(
            f"Active vehicles: {self._edge_orchestrator.active_vehicle_count()}"
        )
        logger.debug(
            f"Active base stations: {self._edge_orchestrator.active_base_station_count()}"
        )
        logger.debug(
            f"Active controllers: {self._cloud_orchestrator.active_controller_count()}"
        )

        # Collect data from the previous time step
        self.data_collector.collect(self)

        # Activate the devices, if any
        self._do_device_activations()

        # Step through the schedule object
        self.schedule.step()

        # Deactivate the devices, if any
        self._do_device_deactivations()

    def update_vehicles(self, vehicles: dict[int, Vehicle]) -> None:
        """
        Update the vehicles in the model.

        Parameters
        ----------
        vehicles : dict[int, Vehicle]
            The vehicles to update.
        """
        for vehicle_id, vehicle in vehicles.items():
            if vehicle_id in self._vehicles:
                self._vehicles[vehicle_id] = vehicle
                self._vehicles[vehicle_id].model = self

    def append_new_roadside_units(
        self, roadside_units: dict[int, RoadsideUnit]
    ) -> None:
        """
        Appends the given roadside units to those in the model.

        Parameters
        ----------
        roadside_units : dict[int, RoadsideUnit]
            The roadside units to update.
        """
        for roadside_unit_id, roadside_unit in roadside_units.items():
            if roadside_unit_id not in self._roadside_units:
                self._roadside_units[roadside_unit_id] = roadside_unit
                self._roadside_units[roadside_unit_id].model = self

    def append_new_base_stations(self, base_stations: dict[int, BaseStation]) -> None:
        """
        Appends the given base stations to those in the model.

        Parameters
        ----------
        base_stations : dict[int, BaseStation]
            The base stations to update.
        """
        for base_station_id, base_station in base_stations.items():
            if base_station_id not in self._base_stations:
                self._base_stations[base_station_id] = base_station
                self._base_stations[base_station_id].model = self

    def append_new_controllers(self, controllers: dict[int, CentralController]) -> None:
        """
        Appends the given controllers to those in the model.

        Parameters
        ----------
        controllers : dict[int, CentralController]
            The controllers to update.
        """
        for controller_id, controller in controllers.items():
            if controller_id not in self._controllers:
                self._controllers[controller_id] = controller
                self._controllers[controller_id].model = self

    def _do_device_activations(self) -> None:
        """
        Activate the devices in the current time step.
        """
        if self.current_time in self._vehicle_activation_times:
            self._activate_vehicles()
        if self.current_time in self._roadside_unit_activation_times:
            self._activate_roadside_units()
        if self.current_time in self._base_station_activation_times:
            self._activate_base_stations()
        if self.current_time in self._controller_activation_times:
            self._activate_controllers()

    def _do_device_deactivations(self) -> None:
        """
        Deactivate the devices in the current time step.
        """
        if self.current_time in self._vehicle_deactivation_times:
            self._deactivate_vehicles()
        if self.current_time in self._roadside_unit_deactivation_times:
            self._deactivate_roadside_units()
        if self.current_time in self._base_station_deactivation_times:
            self._deactivate_base_stations()
        if self.current_time in self._controller_deactivation_times:
            self._deactivate_controllers()

    def _activate_vehicles(self) -> None:
        """
        Activate the vehicles in the current time step.
        """
        vehicles_to_activate = self._vehicle_activation_times[self.current_time]
        logger.debug(
            f"Activating vehicles {vehicles_to_activate} at time {self.current_time}"
        )

        for vehicle_id in vehicles_to_activate:
            vehicle = self._vehicles[vehicle_id]
            vehicle.activate_vehicle(self.current_time)

            # Add to the schedule and edge orchestrator
            self.schedule.add(vehicle)
            self._edge_orchestrator.add_vehicle(vehicle)

    def _deactivate_vehicles(self) -> None:
        """
        Deactivate the vehicles in the current time step.
        """
        vehicles_to_deactivate = self._vehicle_deactivation_times[self.current_time]
        logger.debug(
            f"Deactivating vehicles {vehicles_to_deactivate} at time {self.current_time}"
        )

        for vehicle_id in vehicles_to_deactivate:
            vehicle = self._vehicles[vehicle_id]
            vehicle.deactivate_vehicle(self.current_time)

            # Remove from the schedule and edge orchestrator
            self.schedule.remove(vehicle)
            self._edge_orchestrator.remove_vehicle(vehicle_id)

    def _activate_roadside_units(self) -> None:
        """
        Activate the roadside units in the current time step.
        """
        rsus_to_activate = self._roadside_unit_activation_times[self.current_time]
        logger.debug(
            f"Activating roadside units {rsus_to_activate}"
            f" at time {self.current_time}"
        )

        for roadside_unit_id in rsus_to_activate:
            roadside_unit = self._roadside_units[roadside_unit_id]
            roadside_unit.activate_roadside_unit(self.current_time)

            # Add to the schedule and edge orchestrator
            self.schedule.add(roadside_unit)
            self._edge_orchestrator.add_roadside_unit(roadside_unit)

    def _deactivate_roadside_units(self) -> None:
        """
        Deactivate the roadside units in the current time step.
        """
        rsus_to_deactivate = self._roadside_unit_deactivation_times[self.current_time]
        logger.debug(
            f"Deactivating roadside units {rsus_to_deactivate}"
            f" at time {self.current_time}"
        )

        for roadside_unit_id in rsus_to_deactivate:
            roadside_unit = self._roadside_units[roadside_unit_id]
            roadside_unit.deactivate_roadside_unit(self.current_time)

            # Remove from the schedule and edge orchestrator
            self.schedule.remove(roadside_unit)
            self._edge_orchestrator.remove_roadside_unit(roadside_unit_id)

    def _activate_base_stations(self) -> None:
        """
        Activate the base stations in the current time step.
        """
        base_stations_to_activate = self._base_station_activation_times[
            self.current_time
        ]
        logger.debug(
            f"Activating base stations {base_stations_to_activate}"
            f" at time {self.current_time}"
        )

        for base_station_id in base_stations_to_activate:
            base_station = self._base_stations[base_station_id]
            base_station.activate_base_station(self.current_time)

            # Add to the schedule and both orchestrators
            self.schedule.add(base_station)
            self._edge_orchestrator.add_base_station(base_station)
            self._cloud_orchestrator.add_base_station(base_station)

    def _deactivate_base_stations(self) -> None:
        """
        Deactivate the base stations in the current time step.
        """
        stations_to_deactivate = self._base_station_deactivation_times[
            self.current_time
        ]
        logger.debug(
            f"Deactivating base stations {stations_to_deactivate}"
            f" at time {self.current_time}"
        )

        for base_station_id in stations_to_deactivate:
            base_station = self._base_stations[base_station_id]
            base_station.deactivate_base_station(self.current_time)

            # Remove from the schedule and both the orchestrators
            self.schedule.remove(base_station)
            self._edge_orchestrator.remove_base_station(base_station_id)
            self._cloud_orchestrator.remove_base_station(base_station_id)

    def _activate_controllers(self) -> None:
        """
        Activate the controllers in the current time step.
        """
        controllers_to_activate = self._controller_activation_times[self.current_time]
        logger.debug(
            f"Activating controllers {controllers_to_activate}"
            f" at time {self.current_time}"
        )

        for controller_id in controllers_to_activate:
            controller = self._controllers[controller_id]
            controller.activate_controller(self.current_time)

            # Add to the schedule and to cloud orchestrator
            self.schedule.add(controller)
            self._cloud_orchestrator.add_controller(controller)

    def _deactivate_controllers(self) -> None:
        """
        Deactivate the controllers in the current time step.
        """
        controllers_to_deactivate = self._controller_deactivation_times[
            self.current_time
        ]
        logger.debug(
            f"Deactivating controllers {controllers_to_deactivate}"
            f" at time {self.current_time}"
        )

        for controller_id in controllers_to_deactivate:
            controller = self._controllers[controller_id]
            controller.deactivate_controller(self.current_time)

            # Remove from the schedule and cloud orchestrator
            self.schedule.remove(controller)
            self._cloud_orchestrator.remove_controller(controller_id)
