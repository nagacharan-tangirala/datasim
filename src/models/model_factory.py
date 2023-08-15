import logging

from pandas import DataFrame

import src.core.constants as constants
from src.core.exceptions import ModelTypeNotImplementedError
from src.models.collector import ControllerCollector, VehicleCollector
from src.models.composer import *
from src.models.finder import *
from src.models.mobility import *
from src.models.simplifier import *

logger = logging.getLogger(__name__)


class ModelFactory:
    def __init__(self):
        """
        Initialize the model factory.
        """
        pass

    @staticmethod
    def create_mobility_model(
        model_data: dict,
    ) -> StaticMobilityModel | TraceMobilityModel:
        """
        Create a mobility model from the given parameters.

        Parameters
        ----------
        model_data : dict
            Dictionary containing all the mobility model data.
        """
        model_name = model_data[constants.MODEL_NAME]
        match model_name:
            case constants.STATIC_MOBILITY:
                logger.debug(
                    f"Creating static mobility model with position {model_data[constants.POSITION]}."
                )
                return StaticMobilityModel(model_data[constants.POSITION])
            case constants.TRACE_MOBILITY:
                logger.debug("Creating trace mobility model.")
                return TraceMobilityModel()
            case _:
                raise NotImplementedError("Other mobility models are not implemented.")

    @staticmethod
    def create_vehicle_data_composer(data_composer_data: dict) -> VehicleDataComposer:
        """
        Create the data composer model.
        """
        match data_composer_data[constants.MODEL_NAME]:
            case constants.SIMPLE_VEHICLE_DATA_COMPOSER:
                return VehicleDataComposer(data_composer_data)
            case _:
                raise ModelTypeNotImplementedError(
                    constants.DATA_COMPOSER,
                    data_composer_data[constants.MODEL_NAME],
                )

    @staticmethod
    def create_vehicle_data_simplifier(
        data_simplifier_data: dict,
    ) -> VehicleDataSimplifier:
        """
        Create the data simplifier model.
        """
        match data_simplifier_data[constants.MODEL_NAME]:
            case constants.SIMPLE_VEHICLE_DATA_SIMPLIFIER:
                return VehicleDataSimplifier(data_simplifier_data)
            case _:
                raise ModelTypeNotImplementedError(
                    constants.DATA_SIMPLIFIER,
                    data_simplifier_data[constants.MODEL_NAME],
                )

    @staticmethod
    def create_base_station_data_composer(
        data_composer_data: dict,
    ) -> BaseStationDataComposer:
        """
        Create the data composer model.
        """
        match data_composer_data[constants.MODEL_NAME]:
            case constants.SIMPLE_BASE_STATION_DATA_COMPOSER:
                return BaseStationDataComposer(data_composer_data)
            case _:
                raise ModelTypeNotImplementedError(
                    constants.DATA_COMPOSER,
                    data_composer_data[constants.MODEL_NAME],
                )

    @staticmethod
    def create_base_station_data_simplifier(
        data_simplifier_data: dict,
    ) -> BaseStationDataSimplifier:
        """
        Create the data simplifier model.
        """
        match data_simplifier_data[constants.MODEL_NAME]:
            case constants.SIMPLE_BASE_STATION_DATA_SIMPLIFIER:
                return BaseStationDataSimplifier(data_simplifier_data)
            case _:
                raise ModelTypeNotImplementedError(
                    constants.DATA_SIMPLIFIER,
                    data_simplifier_data[constants.MODEL_NAME],
                )

    @staticmethod
    def create_controller_data_composer(
        data_composer_data: dict,
    ) -> ControllerDataComposer:
        """
        Create the data composer model.
        """
        match data_composer_data[constants.MODEL_NAME]:
            case constants.SIMPLE_CONTROLLER_DATA_COMPOSER:
                return ControllerDataComposer(data_composer_data)
            case _:
                raise ModelTypeNotImplementedError(
                    constants.DATA_COMPOSER,
                    data_composer_data[constants.MODEL_NAME],
                )

    @staticmethod
    def create_controller_collector(
        controller_collector_data: dict,
    ) -> ControllerCollector:
        """
        Create the controller collector model.
        """
        match controller_collector_data[constants.MODEL_NAME]:
            case constants.SIMPLE_CONTROLLER_DATA_COLLECTOR:
                return ControllerCollector()
            case _:
                raise ModelTypeNotImplementedError(
                    constants.DATA_COLLECTOR,
                    controller_collector_data[constants.MODEL_NAME],
                )

    @staticmethod
    def create_basestation_finder(
        base_station_links_df: DataFrame, model_data: dict
    ) -> NearestNBaseStationFinder:
        """
        Create the base station finder.
        """
        match model_data[constants.MODEL_NAME]:
            case constants.NEAREST_V2B:
                logger.debug(f"Creating nearest base station finder.")
                return NearestNBaseStationFinder(base_station_links_df)
            case _:
                raise ModelTypeNotImplementedError(
                    constants.BASE_STATION_FINDER, model_data[constants.MODEL_NAME]
                )

    @staticmethod
    def create_vehicle_data_collector(
        vehicle_data_collector_data: dict,
    ) -> VehicleCollector:
        """
        Create the vehicle data collector model.
        """
        match vehicle_data_collector_data[constants.MODEL_NAME]:
            case constants.SIMPLE_VEHICLE_DATA_COLLECTOR:
                return VehicleCollector()
            case _:
                raise ModelTypeNotImplementedError(
                    constants.DATA_COLLECTOR,
                    vehicle_data_collector_data[constants.MODEL_NAME],
                )

    @staticmethod
    def create_vehicle_neighbour_finder(
        v2v_links: DataFrame,
        vehicle_neighbour_finder_data: dict,
    ) -> TraceVehicleNeighbourFinder:
        """
        Create the vehicle neighbour finder model.
        """
        match vehicle_neighbour_finder_data[constants.MODEL_NAME]:
            case constants.TRACE_V2V:
                return TraceVehicleNeighbourFinder(v2v_links)
            case _:
                raise ModelTypeNotImplementedError(
                    constants.NEIGHBOUR_FINDER,
                    vehicle_neighbour_finder_data[constants.MODEL_NAME],
                )
