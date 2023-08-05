import logging

from pandas import DataFrame

import src.core.constants as constants
from src.core.exceptions import ModelTypeNotImplementedError
from src.models.bs_finder import NearestNBaseStationFinder
from src.models.collector import ControllerCollector
from src.models.composer import (
    VehicleDataComposer,
    BaseStationDataComposer,
    ControllerDataComposer,
)
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
            case "static":
                logger.debug(
                    f"Creating static mobility model with position {model_data[constants.POSITION]}."
                )
                return StaticMobilityModel(model_data[constants.POSITION])
            case "trace":
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
            case "simple":
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
            case "simple":
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
            case "simple":
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
            case "simple":
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
            case "simple":
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
            case "simple":
                return ControllerCollector()
            case _:
                raise ModelTypeNotImplementedError(
                    constants.CONTROLLER_COLLECTOR,
                    controller_collector_data[constants.MODEL_NAME],
                )

    @staticmethod
    def create_basestation_finder(
        base_stations: dict, base_station_links_df: DataFrame, model_data: dict
    ) -> NearestNBaseStationFinder:
        """
        Create the base station finder.
        """
        match model_data[constants.MODEL_NAME]:
            case "nearest":
                logger.debug(f"Creating nearest base station finder.")
                return NearestNBaseStationFinder(base_stations, base_station_links_df)
            case _:
                raise ModelTypeNotImplementedError(
                    constants.BASE_STATION_FINDER, model_data[constants.MODEL_NAME]
                )
