import logging

from mesa import DataCollector, Model
from mesa.space import ContinuousSpace
from numpy import ndarray

import src.core.common_constants as cc
import src.core.constants as constants
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

        self._edge_orchestrator: EdgeOrchestrator = edge_orchestrator
        self._cloud_orchestrator: CloudOrchestrator = cloud_orchestrator

        self._activation_times: dict[str, dict[int, set[int]]] = {
            constants.VEHICLES: {},
            constants.BASE_STATIONS: {},
            constants.CONTROLLERS: {},
        }
        self._deactivation_times: dict[str, dict[int, set[int]]] = {
            constants.VEHICLES: {},
            constants.BASE_STATIONS: {},
            constants.CONTROLLERS: {},
        }

        self._space_settings: dict = space_settings
        self._start_time: int = start_time
        self._end_time: int = end_time
        self._current_time: int = -1

    @property
    def current_time(self) -> int:
        """Get the current time."""
        return self._current_time

    @current_time.setter
    def current_time(self, value: int) -> None:
        """Set the current time."""
        self._current_time = value

    def perform_final_setup(self) -> None:
        """
        Complete the simulation setup.
        """
        logger.debug("Reading activation and deactivation times for all the devices.")
        self.save_device_activation_times()

        logger.debug("Initializing the scheduler.")
        self._initialize_scheduler()

        logger.debug("Initializing the 2D space.")
        self._initialize_space()

        logger.debug("Add orchestrators to the scheduler.")
        self._add_orchestrators_to_scheduler()

        logger.debug("Assign simulation model to all the devices.")
        self._assign_sim_model_to_devices()

        logger.debug("Create data collector.")
        self._create_data_collector()

    def save_device_activation_times(self) -> None:
        """
        Extract the activation and deactivation times of the devices.
        """
        logger.debug("Extracting activation and deactivation times for vehicles.")
        for vehicle_id, vehicle in self._vehicles.items():
            start_times = vehicle.get_activation_times()
            end_times = vehicle.get_deactivation_times()
            logger.debug(
                f"Vehicle {vehicle_id} has activation times {start_times} and deactivation times {end_times}."
            )
            self._save_activation_data(
                start_times, end_times, vehicle_id, constants.VEHICLES
            )

        logger.debug("Extracting activation and deactivation times for base stations.")
        for base_station_id, base_station in self._base_stations.items():
            start_times = base_station.get_activation_times()
            end_times = base_station.get_deactivation_times()
            logger.debug(
                f"Base station {base_station_id} has activation times {start_times} and deactivation times {end_times}."
            )
            self._save_activation_data(
                start_times, end_times, base_station_id, constants.BASE_STATIONS
            )

        logger.debug("Extracting activation and deactivation times for controllers.")
        for controller_id, controller in self._controllers.items():
            start_times = controller.get_activation_times()
            end_times = controller.get_deactivation_times()
            logger.debug(
                f"Controller {controller_id} has activation times {start_times} and deactivation times {end_times}."
            )
            self._save_activation_data(
                start_times, end_times, controller_id, constants.CONTROLLERS
            )

    def _initialize_scheduler(self) -> None:
        """
        Initialize the scheduler.
        """
        # Prepare the type stage list.
        type_stage_list: list[TypeStage] = []

        # Add the vehicle type to the type stage list for the uplink stage.
        vehicle_type_stage = TypeStage(
            type=type(list(self._vehicles.values())[0]), stage="uplink_stage"
        )
        type_stage_list.append(vehicle_type_stage)

        # Add the edge orchestrator type to the type stage list for the uplink stage.
        edge_orchestrator_type_stage = TypeStage(
            type=type(self._edge_orchestrator), stage="uplink_stage"
        )
        type_stage_list.append(edge_orchestrator_type_stage)

        # Add the base station type to the type stage list for the uplink stage.
        base_station_type_stage = TypeStage(
            type=type(list(self._base_stations.values())[0]), stage="uplink_stage"
        )
        type_stage_list.append(base_station_type_stage)

        # Add the cloud orchestrator type to the type stage list for the uplink stage.
        cloud_orchestrator_type_stage = TypeStage(
            type=type(self._cloud_orchestrator), stage="uplink_stage"
        )
        type_stage_list.append(cloud_orchestrator_type_stage)

        # Add the controller type to the type stage list for the uplink stage.
        controller_type_stage = TypeStage(
            type=type(list(self._controllers.values())[0]), stage="uplink_stage"
        )
        type_stage_list.append(controller_type_stage)

        # Add the controller type to the type stage list for the downlink stage.
        controller_type_stage = TypeStage(
            type=type(list(self._controllers.values())[0]), stage="downlink_stage"
        )
        type_stage_list.append(controller_type_stage)

        # Add the cloud orchestrator type to the type stage list for the downlink stage.
        cloud_orchestrator_type_stage = TypeStage(
            type=type(self._cloud_orchestrator), stage="downlink_stage"
        )
        type_stage_list.append(cloud_orchestrator_type_stage)

        # Add the base station type to the type stage list for the downlink stage.
        base_station_type_stage = TypeStage(
            type=type(list(self._base_stations.values())[0]), stage="downlink_stage"
        )
        type_stage_list.append(base_station_type_stage)

        # Add the edge orchestrator type to the type stage list for the downlink stage.
        edge_orchestrator_type_stage = TypeStage(
            type=type(self._edge_orchestrator), stage="downlink_stage"
        )
        type_stage_list.append(edge_orchestrator_type_stage)

        # Add the vehicle type to the type stage list for the downlink stage.
        vehicle_type_stage = TypeStage(
            type=type(list(self._vehicles.values())[0]), stage="downlink_stage"
        )
        type_stage_list.append(vehicle_type_stage)

        self.schedule = OrderedMultiStageScheduler(self, type_stage_list, shuffle=True)

    def _initialize_space(self) -> None:
        """
        Initialize the space.
        """
        self.space = ContinuousSpace(
            x_max=self._space_settings[cc.SPACE_X_MAX] + constants.BUFFER_SPACE,
            y_max=self._space_settings[cc.SPACE_Y_MAX] + constants.BUFFER_SPACE,
            torus=False,
            x_min=self._space_settings[cc.SPACE_X_MIN] - constants.BUFFER_SPACE,
            y_min=self._space_settings[cc.SPACE_Y_MIN] - constants.BUFFER_SPACE,
        )

    def _add_orchestrators_to_scheduler(self) -> None:
        """
        Add the orchestrators to the scheduler.
        """
        self._edge_orchestrator.model = self
        self._cloud_orchestrator.model = self

        self.schedule.add(self._edge_orchestrator)
        self.schedule.add(self._cloud_orchestrator)

    def _assign_sim_model_to_devices(self) -> None:
        """
        Assign the simulation model to the devices.
        """
        for vehicle in self._vehicles.values():
            vehicle.model = self
        for base_station in self._base_stations.values():
            base_station.model = self
        for controller in self._controllers.values():
            controller.model = self

    def _create_data_collector(self) -> None:
        """
        Create the data collector.
        """
        self.data_collector = DataCollector(
            model_reporters={
                "active_vehicles": self._edge_orchestrator.active_vehicle_count,
                "active_base_stations": self._edge_orchestrator.active_base_station_count,
                "total_data": self._cloud_orchestrator.get_total_data_at_controllers,
                "visible_vehicles": self._cloud_orchestrator.get_visible_vehicles_at_controllers,
                "side_link_data": self._edge_orchestrator.get_total_sidelink_data_size,
                "data_sizes_by_type": self._cloud_orchestrator.get_data_sizes_by_type,
                "data_counts_by_type": self._cloud_orchestrator.get_data_counts_by_type,
            },
            agent_reporters={
                "vehicle_data": lambda v: v.data_generated_at_device
                if v.type == constants.VEHICLES
                else None,
                "vehicles_in_range": lambda b: b.vehicles_in_range
                if b.type != constants.CLOUD_ORCHESTRATOR
                and b.type != constants.EDGE_ORCHESTRATOR
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
        Prepare a dictionary with time step as the key and the respective vehicles to activate in that time step.
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

    def update_base_stations(self, base_stations: dict[int, BaseStation]) -> None:
        """
        Update the base stations in the model.

        Parameters
        ----------
        base_stations : dict[int, BaseStation]
            The base stations to update.
        """
        for base_station_id, base_station in base_stations.items():
            if base_station_id not in self._base_stations:
                self._base_stations[base_station_id] = base_station
                self._base_stations[base_station_id].model = self

    def update_controllers(self, controllers: dict[int, CentralController]) -> None:
        """
        Update the controllers in the model.

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
        if self._current_time in self._activation_times[constants.VEHICLES]:
            self._activate_vehicles()
        if self._current_time in self._activation_times[constants.BASE_STATIONS]:
            self._activate_base_stations()
        if self._current_time in self._activation_times[constants.CONTROLLERS]:
            self._activate_controllers()

    def _do_device_deactivations(self) -> None:
        """
        Deactivate the devices in the current time step.
        """
        if self._current_time in self._deactivation_times[constants.VEHICLES]:
            self._deactivate_vehicles()
        if self._current_time in self._deactivation_times[constants.BASE_STATIONS]:
            self._deactivate_base_stations()
        if self._current_time in self._deactivation_times[constants.CONTROLLERS]:
            self._deactivate_controllers()

    def _activate_vehicles(self) -> None:
        """
        Activate the vehicles in the current time step.
        """
        vehicles_to_activate = self._activation_times[constants.VEHICLES][
            self._current_time
        ]
        logger.debug(
            f"Activating vehicles {vehicles_to_activate} at time {self._current_time}"
        )

        for vehicle_id in vehicles_to_activate:
            vehicle = self._vehicles[vehicle_id]
            vehicle.activate_vehicle(self._current_time)

            # Add to the schedule and orchestrator and set the mesa model to this
            self.schedule.add(vehicle)
            self._edge_orchestrator.add_vehicle(vehicle)

    def _deactivate_vehicles(self) -> None:
        """
        Deactivate the vehicles in the current time step.
        """
        vehicles_to_deactivate = self._deactivation_times[constants.VEHICLES][
            self._current_time
        ]
        logger.debug(
            f"Deactivating vehicles {vehicles_to_deactivate} at time {self._current_time}"
        )

        for vehicle_id in vehicles_to_deactivate:
            vehicle = self._vehicles[vehicle_id]
            vehicle.deactivate_vehicle(self._current_time)

            # Remove from the schedule and orchestrator and set the mesa model to None
            self.schedule.remove(vehicle)
            self._edge_orchestrator.remove_vehicle(vehicle_id)

    def _activate_base_stations(self) -> None:
        """
        Activate the base stations in the current time step.
        """
        base_stations_to_activate = self._activation_times[constants.BASE_STATIONS][
            self._current_time
        ]
        logger.debug(
            f"Activating base stations {base_stations_to_activate} at time {self._current_time}"
        )

        for base_station_id in base_stations_to_activate:
            base_station = self._base_stations[base_station_id]
            base_station.activate_base_station(self._current_time)

            # Add to the schedule and orchestrator and set the mesa model to this
            self.schedule.add(base_station)
            self._edge_orchestrator.add_base_station(base_station)
            self._cloud_orchestrator.add_base_station(base_station)

    def _deactivate_base_stations(self) -> None:
        """
        Deactivate the base stations in the current time step.
        """
        base_stations_to_deactivate = self._deactivation_times[constants.BASE_STATIONS][
            self._current_time
        ]
        logger.debug(
            f"Deactivating base stations {base_stations_to_deactivate} at time {self._current_time}"
        )

        for base_station_id in base_stations_to_deactivate:
            base_station = self._base_stations[base_station_id]
            base_station.deactivate_base_station(self._current_time)

            # Remove from the schedule and orchestrator and set the mesa model to None
            self.schedule.remove(base_station)
            self._edge_orchestrator.remove_base_station(base_station_id)
            self._cloud_orchestrator.remove_base_station(base_station_id)

    def _activate_controllers(self) -> None:
        """
        Activate the controllers in the current time step.
        """
        controllers_to_activate = self._activation_times[constants.CONTROLLERS][
            self._current_time
        ]
        logger.debug(
            f"Activating controllers {controllers_to_activate} at time {self._current_time}"
        )

        for controller_id in controllers_to_activate:
            controller = self._controllers[controller_id]
            controller.activate_controller(self._current_time)

            # Add to the schedule and orchestrator and set the mesa model to this
            self.schedule.add(controller)
            self._cloud_orchestrator.add_controller(controller)

    def _deactivate_controllers(self) -> None:
        """
        Deactivate the controllers in the current time step.
        """
        controllers_to_deactivate = self._deactivation_times[constants.CONTROLLERS][
            self._current_time
        ]
        logger.debug(
            f"Deactivating controllers {controllers_to_deactivate} at time {self._current_time}"
        )

        for controller_id in controllers_to_deactivate:
            controller = self._controllers[controller_id]
            controller.deactivate_controller(self._current_time)

            # Remove from the schedule and orchestrator and set the mesa model to None
            self.schedule.remove(controller)
            self._cloud_orchestrator.remove_controller(controller_id)
