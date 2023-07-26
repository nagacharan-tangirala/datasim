import logging
from random import choices

from numpy import asarray, ndarray
from pandas import DataFrame, Series

from src.application.ApplicationSettings import ApplicationSettings
from src.core.CommonConstants import *
from src.core.Constants import *
from src.device.ActivationSettings import ActivationSettings
from src.device.BaseStation import BaseStation
from src.device.CentralController import CentralController
from src.device.ComputingHardware import ComputingHardware
from src.device.NetworkHardware import NetworkHardware
from src.device.VehicleUE import VehicleUE

logger = logging.getLogger(__name__)


class DeviceFactory:
    def __init__(self,
                 applications_data: dict,
                 vehicle_activations_data: DataFrame,
                 base_station_activations_data: DataFrame,
                 controller_activations_data: DataFrame):
        """
        Initialize the device factory object.
        """
        # Store the activations data
        self._vehicle_activations_data: DataFrame = vehicle_activations_data
        self._base_station_activations_data: DataFrame = base_station_activations_data
        self._controller_activations_data: DataFrame = controller_activations_data

        # Create the dictionaries to store the devices in the simulation
        self._vehicles: dict[int, VehicleUE] = {}
        self._base_stations: dict[int, BaseStation] = {}
        self._controllers: dict[int, CentralController] = {}

        self._applications: list[ApplicationSettings] = []
        self._create_applications(applications_data)

    @property
    def vehicles(self) -> dict[int, VehicleUE]:
        """ Get the vehicles in the simulation. """
        return self._vehicles

    @property
    def base_stations(self) -> dict[int, BaseStation]:
        """ Get the base stations in the simulation. """
        return self._base_stations

    @property
    def controllers(self) -> dict[int, CentralController]:
        """ Get the controllers in the simulation. """
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

    def _create_applications(self, application_data: dict) -> None:
        """
        Create the applications.
        """
        logger.debug("Creating the applications.")
        self._applications = [ApplicationSettings(application) for application in application_data.values()]

    def create_vehicles(self,
                        vehicle_trace_data: DataFrame,
                        vehicle_models: dict) -> None:
        """
        Create the vehicles in the simulation.

        Parameters
        ----------
        vehicle_trace_data : DataFrame
            The trace data of the vehicles.
        vehicle_models : dict
            The model data of the vehicles.
        """
        # Get the list of vehicles in the simulation.
        vehicle_ids = vehicle_trace_data[CC_VEHICLE_ID].unique()

        logger.debug(f'Creating {len(vehicle_ids)} vehicles.')
        # Get the weights of the ue types.
        vehicle_weights = [ue_data[C_VEHICLE_RATIO] for ue_data in vehicle_models.values()]
        vehicle_types = list(vehicle_models.keys())

        logger.debug(f'Vehicle Weights: {vehicle_weights}')
        logger.debug(f'Vehicle Types: {vehicle_types}')

        # Create the vehicles.
        for vehicle_id in vehicle_ids:
            logger.debug(f'Creating vehicle {vehicle_id}')
            # Randomly select the type of the vehicle and get the respective model set.
            vehicle_type_choice = choices(vehicle_types, weights=vehicle_weights, k=1)[0]
            selected_vehicle_models = vehicle_models[vehicle_type_choice].copy()

            # Create activation settings from the activation data.
            this_activation_data: Series = \
                self._vehicle_activations_data[self._vehicle_activations_data[CC_VEHICLE_ID] == vehicle_id]

            this_activation_settings = ActivationSettings(this_activation_data[CC_START_TIME].values,
                                                          this_activation_data[CC_END_TIME].values)

            # Create the vehicle.

            self._vehicles[vehicle_id] = self._create_vehicle(vehicle_id,
                                                              this_activation_settings,
                                                              selected_vehicle_models)

            # Update the vehicle trace data.
            this_vehicle_trace: DataFrame = vehicle_trace_data[vehicle_trace_data[CC_VEHICLE_ID] == vehicle_id]
            self._vehicles[vehicle_id].update_mobility_data(this_vehicle_trace)

            logger.debug(f'Created vehicle {vehicle_id} of type {vehicle_type_choice}')

    def _create_vehicle(self,
                        vehicle_id: int,
                        activation_settings: ActivationSettings,
                        vehicle_models: dict) -> VehicleUE:
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
        VehicleUE
            The created vehicle.
        """
        # Create the computing hardware.
        computing_hardware = DeviceFactory._create_computing_hardware(vehicle_models[C_COMPUTING_HARDWARE])

        # Create the networking hardware.
        wireless_hardware = DeviceFactory._create_networking_hardware(vehicle_models[C_NETWORKING_HARDWARE])

        return VehicleUE(vehicle_id,
                         computing_hardware,
                         wireless_hardware,
                         activation_settings,
                         self._applications,
                         vehicle_models)

    def create_base_stations(self, base_station_data: DataFrame, base_station_models_data: dict) -> None:
        """
        Create the base stations in the simulation.
        """
        # Get the list of base stations in the simulation.
        base_station_ids = base_station_data[CC_BASE_STATION_ID].unique()

        for base_station_id in base_station_ids:
            logger.debug(f'Creating base station {base_station_id}')
            # Get the base station position.
            base_station_position: ndarray = \
                base_station_data[base_station_data[CC_BASE_STATION_ID] == base_station_id][[CC_X, CC_Y]].values

            # Create the base station.
            self._base_stations[base_station_id] = self._create_base_station(base_station_id,
                                                                             base_station_position,
                                                                             base_station_models_data)

    @staticmethod
    def _create_base_station(base_station_id: int, base_station_position: list[float], base_station_models_data: dict):
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
        """
        # Create the computing hardware.
        computing_hardware = DeviceFactory._create_computing_hardware(base_station_models_data[C_COMPUTING_HARDWARE])

        # Create wired hardware.
        wired_hardware = DeviceFactory._create_networking_hardware(
            base_station_models_data[C_NETWORKING_HARDWARE][C_WIRED])

        # Create wireless hardware.
        wireless_hardware = DeviceFactory._create_networking_hardware(
            base_station_models_data[C_NETWORKING_HARDWARE][C_WIRELESS])

        # Create activation settings from the activation data.
        this_activation_settings = ActivationSettings(asarray([]), asarray([]))

        # Create the base station.
        return BaseStation(base_station_id,
                           base_station_position,
                           computing_hardware,
                           wireless_hardware,
                           wired_hardware,
                           this_activation_settings,
                           base_station_models_data)

    def create_controllers(self, controller_data: DataFrame, controller_models_data: dict) -> None:
        """
        Create the controllers in the simulation.
        """
        # Get the list of controllers in the simulation.
        controller_list = controller_data[CC_CONTROLLER_ID].unique()

        # Create the controllers.
        for controller_id in controller_list:
            # Get the controller position.
            controller_position: list[float, float] = \
                controller_data[controller_data[CC_CONTROLLER_ID] == controller_id][[CC_X, CC_Y]].values.tolist()

            # Create the controller.
            self._controllers[controller_id] = self._create_controller(controller_id,
                                                                       controller_position,
                                                                       controller_models_data)

    @staticmethod
    def _create_controller(controller_id, position, controller_models_data) -> CentralController:
        """
        Create a controller from the given parameters.

        Parameters
        ----------
        controller_id : int
            The ID of the controller.
        position : list[float]
            The position of the controller.
        """
        # Create the computing hardware.
        computing_hardware = DeviceFactory._create_computing_hardware(controller_models_data[C_COMPUTING_HARDWARE])

        # Create wired hardware.
        wired_hardware = DeviceFactory._create_networking_hardware(controller_models_data[C_NETWORKING_HARDWARE])

        # Create activation settings from the activation data.
        this_activation_settings = ActivationSettings(asarray([]), asarray([]))

        # Create the controller.
        return CentralController(controller_id,
                                 position,
                                 computing_hardware,
                                 wired_hardware,
                                 this_activation_settings,
                                 controller_models_data)

    def create_new_vehicles(self, vehicle_trace_data: DataFrame, vehicle_models: dict) -> None:
        """
        Update the vehicles based on the new trace data.
        """
        ue_list = vehicle_trace_data[CC_VEHICLE_ID].unique()

        # Get the weights of the vehicle types.
        vehicle_weights = [float(ue_data[C_VEHICLE_RATIO]) for ue_data in vehicle_models.values()]
        vehicle_types = list(vehicle_models.keys())

        for vehicle_id in ue_list:
            this_vehicle_trace: DataFrame = vehicle_trace_data[vehicle_trace_data[CC_VEHICLE_ID] == vehicle_id]
            if vehicle_id in self._vehicles:
                # Already exists, update the trace data and continue
                self._vehicles[vehicle_id].update_mobility_data(this_vehicle_trace)
                continue

            # Randomly select the type of the vehicle and get the respective model set.
            vehicle_type_choice = choices(vehicle_types, weights=vehicle_weights, k=1)[0]
            selected_vehicle_models = vehicle_models[vehicle_type_choice].copy()

            # Create the activation settings.
            this_activation_settings = \
                self._vehicle_activations_data[self._vehicle_activations_data[CC_VEHICLE_ID] == vehicle_id].iloc[0]

            # Create the vehicle and update the trace data.
            self._vehicles[vehicle_id] = self._create_vehicle(vehicle_id,
                                                              this_activation_settings,
                                                              selected_vehicle_models)

            self._vehicles[vehicle_id].update_mobility_data(this_vehicle_trace)

    def create_new_base_stations(self, base_station_data: DataFrame, base_station_models_data: dict) -> None:
        """
        Update the base stations based on the new trace data.
        """
        # Get the list of base stations in the simulation.
        base_station_list = base_station_data[CC_BASE_STATION_ID].unique()

        for base_station_id in base_station_list:
            if base_station_id in self._base_stations:
                # TODO: Update the base station if there is any requirement to do so.
                #  Currently, there is no requirement. All the base station data is static in the simulation.
                continue

            # Get the base station position.
            base_station_position: list[float, float] = \
                base_station_data[base_station_data[CC_BASE_STATION_ID] == base_station_data][
                    [CC_X, CC_Y]].values.tolist()

            # Create the base station.
            self._base_stations[base_station_id] = self._create_base_station(base_station_id,
                                                                             base_station_position,
                                                                             base_station_models_data)

    def create_new_controllers(self, controller_data: DataFrame, controller_models_data: dict) -> None:
        """
        Update the controllers based on the new trace data.
        """
        # Get the list of controllers in the simulation.
        controller_list = controller_data[CC_CONTROLLER_ID].unique()

        for controller_id in controller_list:
            if controller_id in self._controllers:
                # TODO: Update the controller if there is any requirement to do so.
                #  Currently, there is no requirement. All the controller data is static in the simulation.
                continue

            # Get the controller position.
            controller_position: list[float, float] = \
                controller_data[controller_data[CC_CONTROLLER_ID] == controller_id][[CC_X, CC_Y]].values.tolist()

            # Create the controller.
            self._controllers[controller_id] = self._create_controller(controller_id,
                                                                       controller_position,
                                                                       controller_models_data)