import logging
from random import choices

from device.road_side_unit import RoadsideUnit
from numpy import asarray
from pandas import DataFrame, Series

from src.core.common_constants import (
    Column,
    CoordSpace,
    DeviceId,
    DeviceName,
    TraceTimes,
)
from src.core.constants import HardwareKey, ModelName, ModelParam
from src.device.activation import ActivationSettings
from src.device.base_station import BaseStation
from src.device.controller import CentralController
from src.device.hardware import ComputingHardware, NetworkHardware
from src.device.vehicle import Vehicle

logger = logging.getLogger(__name__)


def _create_computing_hardware(computing_hardware_data: dict) -> ComputingHardware:
    """
    Create the computing hardware.
    """
    return ComputingHardware(computing_hardware_data)


def _create_networking_hardware(networking_hardware: dict) -> NetworkHardware:
    """
    Create the networking hardware.
    """
    return NetworkHardware(networking_hardware)


class DeviceFactory:
    def __init__(
        self,
        vehicle_activations_data: DataFrame,
        base_station_activations_data: DataFrame,
        controller_activations_data: DataFrame,
        rsu_activations_data: DataFrame,
        data_source_config: dict,
        sim_start_time: int,
        sim_end_time: int,
    ):
        """
        Initialize the device factory object.

        Parameters
        ----------
        vehicle_activations_data : DataFrame
            The activation data of the vehicles.
        base_station_activations_data : DataFrame
            The activation data of the base stations.
        controller_activations_data : DataFrame
            The activation data of the controllers.
        rsu_activations_data : DataFrame
            The activation data of the RSUs.
        data_source_config : dict
            The data source configuration.
        sim_start_time : int
            The start time of the simulation.
        sim_end_time : int
            The end time of the simulation.
        """
        self._veh_activations: DataFrame = vehicle_activations_data
        self._bs_activations: DataFrame = base_station_activations_data
        self._controller_activations: DataFrame = controller_activations_data
        self._rsu_activations: DataFrame = rsu_activations_data

        self._vehicle_sources: dict = data_source_config[DeviceName.VEHICLES][
            ModelParam.DATA_SOURCE
        ]
        self._rsu_sources: dict = data_source_config[DeviceName.ROADSIDE_UNITS][
            ModelParam.DATA_SOURCE
        ]

        self._sim_start_time: int = sim_start_time
        self._sim_end_time: int = sim_end_time

        self._vehicles: dict[int, Vehicle] = {}
        self._base_stations: dict[int, BaseStation] = {}
        self._controllers: dict[int, CentralController] = {}
        self._roadside_units: dict[int, RoadsideUnit] = {}

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

    @property
    def roadside_units(self) -> dict[int, RoadsideUnit]:
        """Get the roadside units in the simulation."""
        return self._roadside_units

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
        veh_weights = [
            ue_data[ModelParam.VEHICLE_RATIO] for ue_data in vehicle_models.values()
        ]
        vehicle_types = list(vehicle_models.keys())

        vehicle_trace_dict = (
            vehicle_trace_data.groupby(DeviceId.VEHICLE)[
                [TraceTimes.TIME_STEP, CoordSpace.X, CoordSpace.Y, Column.VELOCITY]
            ]
            .apply(lambda x: x.to_dict(orient="list"))
            .to_dict()
        )

        logger.debug(f"Vehicle Weights: {veh_weights}")
        logger.debug(f"Vehicle Types: {vehicle_types}")

        for vehicle_id, vehicle_trace in vehicle_trace_dict.items():
            logger.debug(f"Creating vehicle {vehicle_id}")
            # Randomly select the type of the vehicle and get the respective model set.
            veh_choice = choices(vehicle_types, weights=veh_weights, k=1)[0]
            selected_vehicle_models = vehicle_models[veh_choice].copy()

            # Append data source configuration to the composer model.
            data_source_ids = selected_vehicle_models[ModelName.DATA_COMPOSER][
                ModelParam.DATA_SOURCE_LIST
            ]
            selected_vehicle_models[ModelName.DATA_COMPOSER][ModelParam.DATA_SOURCE] = [
                self._vehicle_sources[ds_id] for ds_id in data_source_ids
            ]

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
            self._vehicles[vehicle_id].update_mobility_data(vehicle_trace)

            logger.debug(f"Created vehicle {vehicle_id} of type {veh_choice}")

    def create_new_vehicles(
        self, vehicle_trace_data: DataFrame, vehicle_models: dict
    ) -> None:
        """
        Creates new vehicles based on the newly streamed data.

        Parameters
        ----------
        vehicle_trace_data : DataFrame
            The trace data of the vehicles.
        vehicle_models : dict
            The model data of the vehicles.
        """
        vehicle_trace_dict = (
            vehicle_trace_data.groupby(DeviceId.VEHICLE)[
                [TraceTimes.TIME_STEP, CoordSpace.X, CoordSpace.Y, Column.VELOCITY]
            ]
            .apply(lambda x: x.to_dict(orient="list"))
            .to_dict()
        )

        vehicle_weights = [
            float(ue_data[ModelParam.VEHICLE_RATIO])
            for ue_data in vehicle_models.values()
        ]
        vehicle_types = list(vehicle_models.keys())

        for vehicle_id, vehicle_trace in vehicle_trace_dict.items():
            if vehicle_id in self._vehicles:
                self._vehicles[vehicle_id].update_mobility_data(vehicle_trace)
                continue

            type_choice = choices(vehicle_types, weights=vehicle_weights, k=1)[0]
            selected_vehicle_models = vehicle_models[type_choice].copy()

            # Append data source configuration to the composer model.
            data_source_ids = selected_vehicle_models[ModelName.DATA_COMPOSER][
                ModelParam.DATA_SOURCE_LIST
            ]
            selected_vehicle_models[ModelName.DATA_COMPOSER][ModelParam.DATA_SOURCE] = [
                self._vehicle_sources[ds_id] for ds_id in data_source_ids
            ]
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
            self._vehicles[vehicle_id].update_mobility_data(vehicle_trace)

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
        computing_hardware = _create_computing_hardware(
            vehicle_models[HardwareKey.COMPUTING]
        )
        wireless_hardware = _create_networking_hardware(
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
        base_station_dict = (
            base_station_data.groupby(DeviceId.BASE_STATION)[
                [CoordSpace.X, CoordSpace.Y]
            ]
            .apply(lambda x: x.to_dict(orient="list"))
            .to_dict()
        )

        for station_id, station_data in base_station_dict.items():
            logger.debug(f"Creating base station {station_id}")
            station_position: list[float] = [pos[0] for pos in station_data.values()]
            self._base_stations[station_id] = self._create_base_station(
                station_id, base_station_models_data
            )
            self._base_stations[station_id].update_mobility_data(station_position)

    def create_new_base_stations(
        self, base_station_data: DataFrame, base_station_models_data: dict
    ) -> None:
        """
        Creates new base stations based on the newly streamed data.

        Parameters
        ----------
        base_station_data : DataFrame
            The position data of the base stations.
        base_station_models_data : dict
            The model data of the base stations.
        """
        base_station_dict = (
            base_station_data.groupby(DeviceId.BASE_STATION)[
                [CoordSpace.X, CoordSpace.Y]
            ]
            .apply(lambda x: x.to_dict(orient="list"))
            .to_dict()
        )

        for station_id, station_data in base_station_dict.items():
            if station_id in self._base_stations:
                continue
            station_position: list[float] = [pos[0] for pos in station_data.values()]
            self._base_stations[station_id] = self._create_base_station(
                station_id, base_station_models_data
            )

            self._base_stations[station_id].update_mobility_data(station_position)

    def _create_base_station(
        self,
        base_station_id: int,
        base_station_models_data: dict,
    ) -> BaseStation:
        """
        Create a base station from the given parameters.

        Parameters
        ----------
        base_station_id : int
            The ID of the base station.
        base_station_models_data : dict
            The model data of the base station.

        Returns
        -------
        BaseStation
            The created base station.
        """
        computing_hardware = _create_computing_hardware(
            base_station_models_data[HardwareKey.COMPUTING]
        )
        wired_hardware = _create_networking_hardware(
            base_station_models_data[HardwareKey.NETWORKING][HardwareKey.WIRED]
        )
        wireless_hardware = _create_networking_hardware(
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
        controller_dict = (
            controller_data.groupby(DeviceId.CONTROLLER)[[CoordSpace.X, CoordSpace.Y]]
            .apply(lambda x: x.to_dict(orient="list"))
            .to_dict()
        )

        for controller_id, controller_info in controller_dict.items():
            controller_position: list[float] = [
                pos[0] for pos in controller_info.values()
            ]
            self._controllers[controller_id] = self._create_controller(
                controller_id, controller_models_data
            )
            self._controllers[controller_id].update_mobility_data(controller_position)

    def create_new_controllers(
        self, controller_data: DataFrame, controller_models_data: dict
    ) -> None:
        """
        Creates new controllers based on the newly streamed data.

        Parameters
        ----------
        controller_data : DataFrame
            The position data of the controllers.
        controller_models_data : dict
            The model data of the controllers.
        """
        controller_dict = (
            controller_data.groupby(DeviceId.CONTROLLER)[[CoordSpace.X, CoordSpace.Y]]
            .apply(lambda x: x.to_dict(orient="list"))
            .to_dict()
        )

        for controller_id, controller_info in controller_dict.items():
            if controller_id in self._controllers:
                continue
            controller_position: list[float] = [
                pos[0] for pos in controller_info.values()
            ]
            self._controllers[controller_id] = self._create_controller(
                controller_id, controller_models_data
            )
            self._controllers[controller_id].update_mobility_data(controller_position)

    def _create_controller(
        self, controller_id, controller_models_data
    ) -> CentralController:
        """
        Create a controller from the given parameters.

        Parameters
        ----------
        controller_id : int
            The ID of the controller.
        controller_models_data : dict
            The model data of the controller.
        """
        computing_hardware = _create_computing_hardware(
            controller_models_data[HardwareKey.COMPUTING]
        )
        wired_hardware = _create_networking_hardware(
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
            computing_hardware,
            wired_hardware,
            this_activation_settings,
            controller_models_data,
        )

    def create_roadside_units(self, rsu_data: DataFrame, rsu_models: dict):
        """
        Create the RSUs in the simulation.

        Parameters
        ----------
        rsu_data : DataFrame
            The position data of the RSUs.
        rsu_models : dict
            The model data of the RSUs.
        """
        rsu_dict = (
            rsu_data.groupby(DeviceId.RSU)[[CoordSpace.X, CoordSpace.Y]]
            .apply(lambda x: x.to_dict(orient="list"))
            .to_dict()
        )

        for rsu_id, rsu_info in rsu_dict.items():
            rsu_position: list[float] = [pos[0] for pos in rsu_info.values()]

            if len(rsu_models) == 1:
                rsu_models = next(iter(rsu_models.values()))

            # Append data source configuration to the composer model.
            data_source_ids = rsu_models[ModelName.DATA_COMPOSER][
                ModelParam.DATA_SOURCE_LIST
            ]
            rsu_models[ModelName.DATA_COMPOSER][ModelParam.DATA_SOURCE] = [
                self._rsu_sources[ds_id] for ds_id in data_source_ids
            ]

            self._roadside_units[rsu_id] = self._create_roadside_unit(
                rsu_id, rsu_models
            )
            self._roadside_units[rsu_id].update_mobility_data(rsu_position)

    def create_new_roadside_units(self, rsu_data: DataFrame, rsu_models: dict) -> None:
        """
        Creates new RSUs based on the newly streamed data.

        Parameters
        ----------
        rsu_data : DataFrame
            The position data of the RSUs.
        rsu_models : dict
            The model data of the RSUs.
        """
        rsu_dict = (
            rsu_data.groupby(DeviceId.RSU)[[CoordSpace.X, CoordSpace.Y]]
            .apply(lambda x: x.to_dict(orient="list"))
            .to_dict()
        )

        for rsu_id, rsu_info in rsu_dict.items():
            if rsu_id in self._roadside_units:
                continue
            rsu_position: list[float] = [pos[0] for pos in rsu_info.values()]

            if len(rsu_models) == 1:
                rsu_models = next(iter(rsu_models.values()))

            # Append data source configuration to the composer model.
            data_source_ids = rsu_models[ModelName.DATA_COMPOSER][
                ModelParam.DATA_SOURCE_LIST
            ]
            rsu_models[ModelName.DATA_COMPOSER][ModelParam.DATA_SOURCE] = [
                self._rsu_sources[ds_id] for ds_id in data_source_ids
            ]

            self._roadside_units[rsu_id] = self._create_roadside_unit(
                rsu_id, rsu_models
            )
            self._roadside_units[rsu_id].update_mobility_data(rsu_position)

    def _create_roadside_unit(self, rsu_id, rsu_models: dict):
        """
        Create an RSU from the given parameters.

        Parameters
        ----------
        rsu_id : int
            The ID of the RSU.
        rsu_models : dict
            The model data of the RSU.

        Returns
        -------
        RoadsideUnit
            The created RSU.
        """
        computing_hardware = _create_computing_hardware(
            rsu_models[HardwareKey.COMPUTING]
        )
        wireless_hardware = _create_networking_hardware(
            rsu_models[HardwareKey.NETWORKING]
        )

        this_activation_settings = ActivationSettings(
            asarray([]),
            asarray([]),
            self._sim_start_time,
            self._sim_end_time,
            is_always_on=True,
        )
        return RoadsideUnit(
            rsu_id,
            computing_hardware,
            wireless_hardware,
            this_activation_settings,
            rsu_models,
        )
