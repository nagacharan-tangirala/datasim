import logging
from random import choices

from numpy import asarray
from pandas import DataFrame, Series

from src.core.common_constants import CoordSpace, DeviceId, TraceTimes
from src.core.constants import HardwareKey, ModelParam
from src.device.activation import ActivationSettings
from src.device.base_station import BaseStation
from src.device.controller import CentralController
from src.device.hardware import ComputingHardware, NetworkHardware
from src.device.vehicle import Vehicle

logger = logging.getLogger(__name__)


class DeviceFactory:
    def __init__(
        self,
        vehicle_activations_data: DataFrame,
        base_station_activations_data: DataFrame,
        controller_activations_data: DataFrame,
        sim_start_time: int,
        sim_end_time: int,
    ):
        """
        Initialize the device factory object.
        """
        self._veh_activations: DataFrame = vehicle_activations_data
        self._bs_activations: DataFrame = base_station_activations_data
        self._controller_activations: DataFrame = controller_activations_data

        self._sim_start_time: int = sim_start_time
        self._sim_end_time: int = sim_end_time

        self._vehicles: dict[int, Vehicle] = {}
        self._base_stations: dict[int, BaseStation] = {}
        self._controllers: dict[int, CentralController] = {}

    @property
    def vehicles(self) -> dict[int, Vehicle]:
        """Get the vehicles in the simulation."""
        return self._vehicles

    @property
    def base_stations(self) -> dict[int, BaseStation]:
        """Get the base stations in the simulation."""
        return self._base_stations

    @property
    def controllers(self) -> dict[int, CentralController]:
        """Get the controllers in the simulation."""
        return self._controllers

    @staticmethod
    def _create_computing_hardware(computing_hardware_data: dict) -> ComputingHardware:
        """
        Create the computing hardware.
        """
        return ComputingHardware(computing_hardware_data)

    @staticmethod
    def _create_networking_hardware(networking_hardware: dict) -> NetworkHardware:
        """
        Create the networking hardware.
        """
        return NetworkHardware(networking_hardware)

    def create_vehicles(
        self, vehicle_trace_data: DataFrame, vehicle_models: dict
    ) -> None:
        """
        Create the vehicles in the simulation.

        Parameters
        ----------
        vehicle_trace_data : DataFrame
            The trace data of the vehicles.
        vehicle_models : dict
            The model data of the vehicles.
        """
        vehicle_ids = vehicle_trace_data[DeviceId.VEHICLE].unique()
        logger.debug(f"Creating {len(vehicle_ids)} vehicles.")
        veh_weights = [
            ue_data[ModelParam.VEHICLE_RATIO] for ue_data in vehicle_models.values()
        ]
        vehicle_types = list(vehicle_models.keys())

        logger.debug(f"Vehicle Weights: {veh_weights}")
        logger.debug(f"Vehicle Types: {vehicle_types}")

        for vehicle_id in vehicle_ids:
            logger.debug(f"Creating vehicle {vehicle_id}")
            # Randomly select the type of the vehicle and get the respective model set.
            veh_choice = choices(vehicle_types, weights=veh_weights, k=1)[0]
            selected_vehicle_models = vehicle_models[veh_choice].copy()

            this_activation_data: Series = self._veh_activations[
                self._veh_activations[DeviceId.DEVICE] == vehicle_id
            ]
            this_activation_settings = ActivationSettings(
                this_activation_data[TraceTimes.START_TIME].values,
                this_activation_data[TraceTimes.END_TIME].values,
                self._sim_start_time,
                self._sim_end_time,
            )

            self._vehicles[vehicle_id] = self._create_vehicle(
                vehicle_id, this_activation_settings, selected_vehicle_models
            )
            this_vehicle_trace: DataFrame = vehicle_trace_data[
                vehicle_trace_data[DeviceId.VEHICLE] == vehicle_id
            ]
            self._vehicles[vehicle_id].update_mobility_data(this_vehicle_trace)

            logger.debug(f"Created vehicle {vehicle_id} of type {veh_choice}")

    @staticmethod
    def _create_vehicle(
        vehicle_id: int,
        activation_settings: ActivationSettings,
        vehicle_models: dict,
    ) -> Vehicle:
        """
        Create a vehicle from the given parameters.

        Parameters
        ----------
        vehicle_id : int
            The ID of the vehicle.
        activation_settings : ActivationSettings
            The activation settings of the vehicle.
        vehicle_models : dict
            The model data of the vehicle.

        Returns
        -------
        Vehicle
            The created vehicle.
        """
        computing_hardware = DeviceFactory._create_computing_hardware(
            vehicle_models[HardwareKey.COMPUTING]
        )
        wireless_hardware = DeviceFactory._create_networking_hardware(
            vehicle_models[HardwareKey.NETWORKING]
        )

        return Vehicle(
            vehicle_id,
            computing_hardware,
            wireless_hardware,
            activation_settings,
            vehicle_models,
        )

    def create_base_stations(
        self, base_station_data: DataFrame, base_station_models_data: dict
    ) -> None:
        """
        Create the base stations in the simulation.
        """
        base_station_ids = base_station_data[DeviceId.BASE_STATION].unique()

        for base_station_id in base_station_ids:
            logger.debug(f"Creating base station {base_station_id}")
            this_station_data = base_station_data[
                base_station_data[DeviceId.BASE_STATION] == base_station_id
            ][[CoordSpace.X, CoordSpace.Y]]

            base_station_position: list[float] = this_station_data.values[0].tolist()

            self._base_stations[base_station_id] = self._create_base_station(
                base_station_id, base_station_position, base_station_models_data
            )

    def _create_base_station(
        self,
        base_station_id: int,
        base_station_position: list[float],
        base_station_models_data: dict,
    ) -> BaseStation:
        """
        Create a base station from the given parameters.

        Parameters
        ----------
        base_station_id : int
            The ID of the base station.
        base_station_position : list[float]
            The position of the base station.
        base_station_models_data : dict
            The model data of the base station.

        Returns
        -------
        BaseStation
            The created base station.
        """
        computing_hardware = DeviceFactory._create_computing_hardware(
            base_station_models_data[HardwareKey.COMPUTING]
        )
        wired_hardware = DeviceFactory._create_networking_hardware(
            base_station_models_data[HardwareKey.NETWORKING][HardwareKey.WIRED]
        )
        wireless_hardware = DeviceFactory._create_networking_hardware(
            base_station_models_data[HardwareKey.NETWORKING][HardwareKey.WIRELESS]
        )
        this_activation_settings = ActivationSettings(
            asarray([]),
            asarray([]),
            self._sim_start_time,
            self._sim_end_time,
            is_always_on=True,
        )

        return BaseStation(
            base_station_id,
            base_station_position,
            computing_hardware,
            wireless_hardware,
            wired_hardware,
            this_activation_settings,
            base_station_models_data,
        )

    def create_controllers(
        self, controller_data: DataFrame, controller_models_data: dict
    ) -> None:
        """
        Create the controllers in the simulation.
        """
        controller_list = controller_data[DeviceId.CONTROLLER].unique()

        for controller_id in controller_list:
            # Get the controller position.
            this_controller_data = controller_data[
                controller_data[DeviceId.CONTROLLER] == controller_id
            ][[CoordSpace.X, CoordSpace.Y]]

            controller_position: list[float] = this_controller_data.values[0].tolist()

            # Create the controller.
            self._controllers[controller_id] = self._create_controller(
                controller_id, controller_position, controller_models_data
            )

    def _create_controller(
        self, controller_id, position: list[float], controller_models_data
    ) -> CentralController:
        """
        Create a controller from the given parameters.

        Parameters
        ----------
        controller_id : int
            The ID of the controller.
        position : list[float]
            The position of the controller.
        """
        computing_hardware = DeviceFactory._create_computing_hardware(
            controller_models_data[HardwareKey.COMPUTING]
        )
        wired_hardware = DeviceFactory._create_networking_hardware(
            controller_models_data[HardwareKey.NETWORKING]
        )

        this_activation_settings = ActivationSettings(
            asarray([]),
            asarray([]),
            self._sim_start_time,
            self._sim_end_time,
            is_always_on=True,
        )
        return CentralController(
            controller_id,
            position,
            computing_hardware,
            wired_hardware,
            this_activation_settings,
            controller_models_data,
        )

    def create_rsus(self, rsu_data: DataFrame, rsu_models: dict):
        pass

    def create_new_vehicles(
        self, vehicle_trace_data: DataFrame, vehicle_models: dict
    ) -> None:
        """
        Update the vehicles based on the new trace data.
        """
        ue_list = vehicle_trace_data[DeviceId.VEHICLE].unique()
        vehicle_weights = [
            float(ue_data[ModelParam.VEHICLE_RATIO])
            for ue_data in vehicle_models.values()
        ]
        vehicle_types = list(vehicle_models.keys())

        for vehicle_id in ue_list:
            this_vehicle_trace: DataFrame = vehicle_trace_data[
                vehicle_trace_data[DeviceId.VEHICLE] == vehicle_id
            ]
            if vehicle_id in self._vehicles:
                self._vehicles[vehicle_id].update_mobility_data(this_vehicle_trace)
                continue

            type_choice = choices(vehicle_types, weights=vehicle_weights, k=1)[0]
            selected_vehicle_models = vehicle_models[type_choice].copy()
            this_activation_data: Series = self._veh_activations[
                self._veh_activations[DeviceId.DEVICE] == vehicle_id
            ]

            this_activation_settings = ActivationSettings(
                this_activation_data[TraceTimes.START_TIME].values,
                this_activation_data[TraceTimes.END_TIME].values,
                self._sim_start_time,
                self._sim_end_time,
            )

            self._vehicles[vehicle_id] = self._create_vehicle(
                vehicle_id, this_activation_settings, selected_vehicle_models
            )
            self._vehicles[vehicle_id].update_mobility_data(this_vehicle_trace)

    def create_new_base_stations(
        self, base_station_data: DataFrame, base_station_models_data: dict
    ) -> None:
        """
        Update the base stations based on the new trace data.
        """
        base_station_list = base_station_data[DeviceId.BASE_STATION].unique()

        for base_station_id in base_station_list:
            if base_station_id in self._base_stations:
                # TODO: Update the base station if there is any requirement to do so.
                #  Currently, there is no requirement. All the base station data is
                #  static in the simulation.
                continue

            this_station_data = base_station_data[
                base_station_data[DeviceId.BASE_STATION] == base_station_id
            ][[CoordSpace.X, CoordSpace.Y]]

            base_station_position: list[float] = this_station_data.values[0].tolist()
            self._base_stations[base_station_id] = self._create_base_station(
                base_station_id, base_station_position, base_station_models_data
            )

    def create_new_controllers(
        self, controller_data: DataFrame, controller_models_data: dict
    ) -> None:
        """
        Update the controllers based on the new trace data.
        """
        controller_list = controller_data[DeviceId.CONTROLLER].unique()
        for controller_id in controller_list:
            if controller_id in self._controllers:
                continue

            this_controller_data = controller_data[
                controller_data[DeviceId.CONTROLLER] == controller_id
            ][[CoordSpace.X, CoordSpace.Y]]

            controller_position: list[float] = this_controller_data.values[0].tolist()

            self._controllers[controller_id] = self._create_controller(
                controller_id, controller_position, controller_models_data
            )
