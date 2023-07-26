import logging

from pandas import DataFrame

from src.application.ApplicationSettings import ApplicationSettings
from src.application.BaseStationAppRunner import BaseStationAppRunner
from src.application.ControllerAppRunner import ControllerAppRunner
from src.application.VehicleAppRunner import VehicleAppRunner
from src.core.Constants import C_MODEL_NAME, C_DATA_PROCESSOR, C_POSITION, C_BASE_STATION_FINDER
from src.core.CustomExceptions import ModelTypeNotImplementedError
from src.device.ComputingHardware import ComputingHardware
from src.models.data_processor.BaseStationDataProcessor import BaseStationDataProcessor
from src.models.data_processor.ControllerDataProcessor import ControllerDataProcessor
from src.models.data_processor.VehicleDataProcessor import VehicleDataProcessor
from src.models.finder.BaseStationFinder import BaseStationFinder
from src.models.mobility.StaticMobilityModel import StaticMobilityModel
from src.models.mobility.TraceMobilityModel import TraceMobilityModel

logger = logging.getLogger(__name__)


class ModelFactory:
    def __init__(self):
        """
        Initialize the model factory.
        """
        pass

    @staticmethod
    def create_mobility_model(model_data: dict) -> StaticMobilityModel | TraceMobilityModel:
        """
        Create a mobility model from the given parameters.

        Parameters
        ----------
        model_data : dict
            Dictionary containing all the mobility model data.
        """
        model_name = model_data[C_MODEL_NAME]
        match model_name:
            case 'static':
                logger.debug(f"Creating static mobility model with position {model_data[C_POSITION]}.")
                return StaticMobilityModel(model_data[C_POSITION])
            case 'trace':
                logger.debug("Creating trace mobility model.")
                return TraceMobilityModel()
            case _:
                raise NotImplementedError("Other mobility models are not implemented.")

    @staticmethod
    def create_vehicle_app_runner(vehicle_id: int, application_settings: list[ApplicationSettings],
                                  computing_hardware: ComputingHardware) -> VehicleAppRunner:
        """
        Create a vehicle application runner.
        """
        logger.debug(f"Creating application runner for vehicle {vehicle_id}.")
        return VehicleAppRunner(vehicle_id, application_settings, computing_hardware)

    @staticmethod
    def create_basestation_app_runner(station_id: int, computing_hardware: ComputingHardware) -> BaseStationAppRunner:
        """
        Create a base station application runner.
        """
        logger.debug(f"Creating application runner for base station {station_id}.")
        return BaseStationAppRunner(station_id, computing_hardware)

    @staticmethod
    def create_controller_app_runner(controller_id: int, computing_hardware: ComputingHardware) -> ControllerAppRunner:
        """
        Create a controller application runner.
        """
        logger.debug(f"Creating application runner for controller {controller_id}.")
        return ControllerAppRunner(controller_id, computing_hardware)

    @staticmethod
    def create_basestation_finder(base_stations: dict, base_station_links_df: DataFrame,
                                  model_data: dict) -> BaseStationFinder:
        """
        Create the base station finder.
        """
        match model_data[C_MODEL_NAME]:
            case 'nearest':
                logger.debug(f"Creating nearest base station finder.")
                return BaseStationFinder(base_stations, base_station_links_df)
            case _:
                raise ModelTypeNotImplementedError(C_BASE_STATION_FINDER, model_data[C_MODEL_NAME])

    @staticmethod
    def create_vehicle_data_processor(data_processor_model_data: dict) -> VehicleDataProcessor:
        """
        Create the vehicle data processor model.
        """
        match data_processor_model_data[C_MODEL_NAME]:
            case "simple":
                return VehicleDataProcessor(data_processor_model_data)
            case _:
                raise ModelTypeNotImplementedError(C_DATA_PROCESSOR, data_processor_model_data[C_MODEL_NAME])

    @staticmethod
    def create_base_station_data_processor(data_processor_model_data: dict) -> BaseStationDataProcessor:
        """
        Create the base station data processor model.
        """
        match data_processor_model_data[C_MODEL_NAME]:
            case "simple":
                return BaseStationDataProcessor(data_processor_model_data)
            case _:
                raise ModelTypeNotImplementedError(C_DATA_PROCESSOR, data_processor_model_data[C_MODEL_NAME])

    @staticmethod
    def create_controller_data_processor(data_processor_model_data: dict) -> ControllerDataProcessor:
        """
        Create the controller data processor model.
        """
        match data_processor_model_data[C_MODEL_NAME]:
            case "simple":
                return ControllerDataProcessor(data_processor_model_data)
            case _:
                raise ModelTypeNotImplementedError(C_DATA_PROCESSOR, data_processor_model_data[C_MODEL_NAME])
