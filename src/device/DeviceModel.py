import logging

from mesa import Model

from src.core.Constants import *
from src.core.OrderedMultiStageScheduler import OrderedMultiStageScheduler, TypeStage
from src.device.BaseStation import BaseStation
from src.device.CentralController import CentralController
from src.device.VehicleUE import VehicleUE
from src.orchestrator.CloudOrchestrator import CloudOrchestrator
from src.orchestrator.EdgeOrchestrator import EdgeOrchestrator

logger = logging.getLogger(__name__)


class DeviceModel(Model):
    def __init__(self,
                 vehicles: dict[int, VehicleUE],
                 base_stations: dict[int, BaseStation],
                 controllers: dict[int, CentralController],
                 edge_orchestrator: EdgeOrchestrator,
                 cloud_orchestrator: CloudOrchestrator,
                 start_time: int,
                 end_time: int
                 ):
        """
        Initialize the device model.
        """
        super().__init__()
        self._vehicles: dict[int, VehicleUE] = vehicles
        self._base_stations: dict[int, BaseStation] = base_stations
        self._controllers: dict[int, CentralController] = controllers

        self._edge_orchestrator: EdgeOrchestrator = edge_orchestrator
        self._cloud_orchestrator: CloudOrchestrator = cloud_orchestrator

        self._agents_by_type: dict[str, list] = {
            C_VEHICLES: self._vehicles,
            C_BASE_STATIONS: self._base_stations,
            C_CONTROLLERS: self._controllers,
            C_EDGE_ORCHESTRATOR: [self._edge_orchestrator],
            C_CLOUD_ORCHESTRATOR: [self._cloud_orchestrator]
        }

        self._device_activation_times: dict[str, dict[int, list[int]]] = {
            C_VEHICLES: {},
            C_BASE_STATIONS: {},
            C_CONTROLLERS: {}
        }
        self._device_deactivation_times: dict[str, dict[int, list[int]]] = {
            C_VEHICLES: {},
            C_BASE_STATIONS: {},
            C_CONTROLLERS: {}
        }

        self._start_time: int = start_time
        self._end_time: int = end_time
        self._current_time: int = -1

    @property
    def current_time(self) -> int:
        """Get the current time."""
        return self._current_time

    @current_time.setter
    def current_time(self, value: int) -> None:
        """ Set the current time."""
        self._current_time = value

    def perform_final_setup(self) -> None:
        """
        Complete the simulation setup.
        """
        logger.debug("Preparing activation and deactivation times for all the devices.")
        self._prepare_device_activation_times()

        logger.debug("Initializing the scheduler.")
        self._initialize_scheduler()

        logger.debug("Add orchestrators to the scheduler.")
        self._add_orchestrators_to_scheduler()

    def _prepare_device_activation_times(self) -> None:
        """
        Extract the activation and deactivation times of the devices.
        """
        logger.debug("Extracting activation and deactivation times for vehicles.")
        for vehicle_id, vehicle in self._vehicles.items():
            start_time, end_time = vehicle.start_time, vehicle.end_time
            self._save_activation_time(start_time, vehicle_id, C_VEHICLES)
            self._save_deactivation_time(end_time, vehicle_id, C_VEHICLES)

        logger.debug("Extracting activation and deactivation times for base stations.")
        for base_station_id, base_station in self._base_stations.items():
            start_time, end_time = base_station.start_time, base_station.end_time
            self._save_activation_time(start_time, base_station_id, C_BASE_STATIONS)
            self._save_deactivation_time(end_time, base_station_id, C_BASE_STATIONS)

        logger.debug("Extracting activation and deactivation times for controllers.")
        for controller_id, controller in self._controllers.items():
            start_time, end_time = controller.start_time, controller.end_time
            self._save_activation_time(start_time, controller_id, C_CONTROLLERS)
            self._save_deactivation_time(end_time, controller_id, C_CONTROLLERS)

    def _initialize_scheduler(self) -> None:
        """
        Initialize the scheduler.
        """
        # Prepare the type stage list.
        type_stage_list: list[TypeStage] = []

        # Add the vehicle type to the type stage list for the uplink stage.
        vehicle_type_stage = TypeStage(type=type(list(self._vehicles.values())[0]), stage='uplink_stage')
        type_stage_list.append(vehicle_type_stage)

        # Add the edge orchestrator type to the type stage list for the uplink stage.
        edge_orchestrator_type_stage = TypeStage(type=type(self._edge_orchestrator), stage='uplink_stage')
        type_stage_list.append(edge_orchestrator_type_stage)

        # Add the base station type to the type stage list for the uplink stage.
        base_station_type_stage = TypeStage(type=type(list(self._base_stations.values())[0]), stage='uplink_stage')
        type_stage_list.append(base_station_type_stage)

        # Add the cloud orchestrator type to the type stage list for the uplink stage.
        cloud_orchestrator_type_stage = TypeStage(type=type(self._cloud_orchestrator), stage='uplink_stage')
        type_stage_list.append(cloud_orchestrator_type_stage)

        # Add the controller type to the type stage list for the uplink stage.
        controller_type_stage = TypeStage(type=type(list(self._controllers.values())[0]), stage='uplink_stage')
        type_stage_list.append(controller_type_stage)

        # Add the controller type to the type stage list for the downlink stage.
        controller_type_stage = TypeStage(type=type(list(self._controllers.values())[0]), stage='downlink_stage')
        type_stage_list.append(controller_type_stage)

        # Add the cloud orchestrator type to the type stage list for the downlink stage.
        cloud_orchestrator_type_stage = TypeStage(type=type(self._cloud_orchestrator), stage='downlink_stage')
        type_stage_list.append(cloud_orchestrator_type_stage)

        # Add the base station type to the type stage list for the downlink stage.
        base_station_type_stage = TypeStage(type=type(list(self._base_stations.values())[0]), stage='downlink_stage')
        type_stage_list.append(base_station_type_stage)

        # Add the edge orchestrator type to the type stage list for the downlink stage.
        edge_orchestrator_type_stage = TypeStage(type=type(self._edge_orchestrator), stage='downlink_stage')
        type_stage_list.append(edge_orchestrator_type_stage)

        # Add the vehicle type to the type stage list for the downlink stage.
        vehicle_type_stage = TypeStage(type=type(list(self._vehicles.values())[0]), stage='downlink_stage')
        type_stage_list.append(vehicle_type_stage)

        self.schedule = OrderedMultiStageScheduler(self, type_stage_list, shuffle=True)

    def _add_orchestrators_to_scheduler(self) -> None:
        """
        Add the orchestrators to the scheduler.
        """
        self.schedule.add(self._edge_orchestrator)
        self.schedule.add(self._cloud_orchestrator)
        self._edge_orchestrator.sim_model = self
        self._cloud_orchestrator.sim_model = self

    def _save_activation_time(self, time_stamp: int, device_id: int, device_type: str) -> None:
        """
        Update the activation time of the device.
        """
        if time_stamp < self._start_time:
            time_stamp = self._start_time

        if time_stamp not in self._device_activation_times[device_type]:
            self._device_activation_times[device_type][time_stamp] = [device_id]
        else:
            self._device_activation_times[device_type][time_stamp].append(device_id)

    def _save_deactivation_time(self, time_stamp: int, device_id: int, device_type: str) -> None:
        """
        Update the deactivation time of the device.
        """
        if time_stamp > self._end_time:
            time_stamp = self._end_time

        if time_stamp not in self._device_deactivation_times[device_type]:
            self._device_deactivation_times[device_type][time_stamp] = [device_id]
        else:
            self._device_deactivation_times[device_type][time_stamp].append(device_id)

    def step(self) -> None:
        """
        Prepare a dictionary with time step as the key and the respective vehicles to activate in that time step.
        """
        logger.info(f"Running step {self._current_time}.")
        logger.debug(f"Current time: {self._current_time}.")
        logger.debug(f"Active vehicles: {self._edge_orchestrator.active_vehicle_count()}.")
        logger.debug(f"Active base stations: {self._edge_orchestrator.active_base_station_count()}.")
        logger.debug(f"Active controllers: {self._cloud_orchestrator.active_controller_count()}.")

        # Refresh active devices at the current time step
        self._refresh_active_devices()

        # Step through the schedule object
        self.schedule.step()

    def update_vehicles(self, vehicles: dict[int, VehicleUE]) -> None:
        """
        Update the vehicles in the model.

        Parameters
        ----------
        vehicles : dict[int, VehicleUE]
            The vehicles to update.
        """
        for vehicle_id, vehicle in vehicles.items():
            if vehicle_id in self._vehicles:
                self._vehicles[vehicle_id] = vehicle

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

    def _refresh_active_devices(self) -> None:
        """
        If the start or end time of a device is equal to the current time step, activate or deactivate the device.
        """
        if self._current_time in self._device_activation_times[C_VEHICLES]:
            self._activate_vehicles()
        if self._current_time in self._device_deactivation_times[C_VEHICLES]:
            self._deactivate_vehicles()
        if self._current_time in self._device_activation_times[C_BASE_STATIONS]:
            self._activate_base_stations()
        if self._current_time in self._device_deactivation_times[C_BASE_STATIONS]:
            self._deactivate_base_stations()
        if self._current_time in self._device_activation_times[C_CONTROLLERS]:
            self._activate_controllers()
        if self._current_time in self._device_deactivation_times[C_CONTROLLERS]:
            self._deactivate_controllers()

    def _activate_vehicles(self) -> None:
        """
        Activate the vehicles in the current time step.
        """
        vehicles_to_activate = self._device_activation_times[C_VEHICLES][self._current_time]
        logger.debug(f"Activating vehicles {vehicles_to_activate} at time {self._current_time}")
        for vehicle_id in vehicles_to_activate:
            vehicle = self._vehicles[vehicle_id]
            vehicle.activate_vehicle(self._current_time)

            # Add to the schedule and orchestrator and set the mesa model to this
            self.schedule.add(vehicle)
            self._edge_orchestrator.add_vehicle(vehicle)
            vehicle.sim_model = self

    def _deactivate_vehicles(self) -> None:
        """
        Deactivate the vehicles in the current time step.
        """
        vehicles_to_deactivate = self._device_deactivation_times[C_VEHICLES][self._current_time]
        logger.debug(f"Deactivating vehicles {vehicles_to_deactivate} at time {self._current_time}")
        for vehicle_id in vehicles_to_deactivate:
            vehicle = self._vehicles[vehicle_id]
            vehicle.deactivate_vehicle(self._current_time)

            # Remove from the schedule and orchestrator and set the mesa model to None
            self.schedule.remove(vehicle)
            self._edge_orchestrator.remove_vehicle(vehicle_id)
            vehicle.sim_model = None

    def _activate_base_stations(self) -> None:
        """
        Activate the base stations in the current time step.
        """
        base_stations_to_activate = self._device_activation_times[C_BASE_STATIONS][self._current_time]
        logger.debug(f"Activating base stations {base_stations_to_activate} at time {self._current_time}")
        for base_station_id in base_stations_to_activate:
            base_station = self._base_stations[base_station_id]
            base_station.activate_base_station(self._current_time)

            # Add to the schedule and orchestrator and set the mesa model to this
            self.schedule.add(base_station)
            self._edge_orchestrator.add_base_station(base_station)
            self._cloud_orchestrator.add_base_station(base_station)
            base_station.sim_model = self

    def _deactivate_base_stations(self) -> None:
        """
        Deactivate the base stations in the current time step.
        """
        base_stations_to_deactivate = self._device_activation_times[C_BASE_STATIONS][self._current_time]
        logger.debug(f"Deactivating base stations {base_stations_to_deactivate} at time {self._current_time}")
        for base_station_id in base_stations_to_deactivate:
            base_station = self._base_stations[base_station_id]
            base_station.deactivate_base_station(self._current_time)

            # Remove from the schedule and orchestrator and set the mesa model to None
            self.schedule.remove(base_station)
            self._edge_orchestrator.remove_base_station(base_station_id)
            self._cloud_orchestrator.remove_base_station(base_station_id)
            base_station.sim_model = None

    def _activate_controllers(self) -> None:
        """
        Activate the controllers in the current time step.
        """
        controllers_to_activate = self._device_activation_times[C_CONTROLLERS][self._current_time]
        logger.debug(f"Activating controllers {controllers_to_activate} at time {self._current_time}")
        for controller_id in controllers_to_activate:
            controller = self._controllers[controller_id]
            controller.activate_controller(self._current_time)

            # Add to the schedule and orchestrator and set the mesa model to this
            self.schedule.add(controller)
            self._cloud_orchestrator.add_controller(controller)
            controller.sim_model = self

    def _deactivate_controllers(self) -> None:
        """
        Deactivate the controllers in the current time step.
        """
        controllers_to_deactivate = self._device_activation_times[C_CONTROLLERS][self._current_time]
        logger.debug(f"Deactivating controllers {controllers_to_deactivate} at time {self._current_time}")
        for controller_id in controllers_to_deactivate:
            controller = self._controllers[controller_id]
            controller.deactivate_controller(self._current_time)

            # Remove from the schedule and orchestrator and set the mesa model to None
            self.schedule.remove(controller)
            self._cloud_orchestrator.remove_controller(controller_id)
            controller.sim_model = None
