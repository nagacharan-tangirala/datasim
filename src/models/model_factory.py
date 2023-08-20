import logging

from pandas import DataFrame

from src.core.constants import ModelName, ModelParam, ModelType
from src.core.exceptions import ModelTypeNotImplementedError
from src.models.collector import ControllerCollector, VehicleCollector
from src.models.composer import (
    BaseStationDataComposer,
    ControllerDataComposer,
    VehicleDataComposer,
)
from src.models.finder import NearestNBaseStationFinder, TraceVehicleNeighbourFinder
from src.models.mobility import StaticMobilityModel, TraceMobilityModel
from src.models.simplifier import BaseStationDataSimplifier, VehicleDataSimplifier

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
        model_name = model_data[ModelParam.MODEL_NAME]
        match model_name:
            case ModelType.STATIC:
                logger.debug(
                    f"Creating static mobility model with position "
                    f"{model_data[ModelParam.POSITION]}."
                )
                return StaticMobilityModel(model_data[ModelParam.POSITION])
            case ModelType.TRACE:
                logger.debug("Creating trace mobility model.")
                return TraceMobilityModel()
            case _:
                raise NotImplementedError("Other mobility models are not implemented.")

    @staticmethod
    def create_vehicle_data_composer(data_composer_data: dict) -> VehicleDataComposer:
        """
        Create the data composer model.
        """
        match data_composer_data[ModelParam.MODEL_NAME]:
            case ModelType.SIMPLE:
                return VehicleDataComposer(data_composer_data)
            case _:
                raise ModelTypeNotImplementedError(
                    ModelName.DATA_COMPOSER,
                    data_composer_data[ModelParam.MODEL_NAME],
                )

    @staticmethod
    def create_vehicle_data_simplifier(
        data_simplifier_data: dict,
    ) -> VehicleDataSimplifier:
        """
        Create the data simplifier model.
        """
        match data_simplifier_data[ModelParam.MODEL_NAME]:
            case ModelType.SIMPLE:
                return VehicleDataSimplifier(data_simplifier_data)
            case _:
                raise ModelTypeNotImplementedError(
                    ModelName.DATA_SIMPLIFIER,
                    data_simplifier_data[ModelParam.MODEL_NAME],
                )

    @staticmethod
    def create_base_station_data_composer(
        data_composer_data: dict,
    ) -> BaseStationDataComposer:
        """
        Create the data composer model.
        """
        match data_composer_data[ModelParam.MODEL_NAME]:
            case ModelType.SIMPLE:
                return BaseStationDataComposer(data_composer_data)
            case _:
                raise ModelTypeNotImplementedError(
                    ModelName.DATA_COMPOSER,
                    data_composer_data[ModelParam.MODEL_NAME],
                )

    @staticmethod
    def create_base_station_data_simplifier(
        data_simplifier_data: dict,
    ) -> BaseStationDataSimplifier:
        """
        Create the data simplifier model.
        """
        match data_simplifier_data[ModelParam.MODEL_NAME]:
            case ModelType.SIMPLE:
                return BaseStationDataSimplifier(data_simplifier_data)
            case _:
                raise ModelTypeNotImplementedError(
                    ModelName.DATA_SIMPLIFIER,
                    data_simplifier_data[ModelParam.MODEL_NAME],
                )

    @staticmethod
    def create_controller_data_composer(
        data_composer_data: dict,
    ) -> ControllerDataComposer:
        """
        Create the data composer model.
        """
        match data_composer_data[ModelParam.MODEL_NAME]:
            case ModelType.SIMPLE:
                return ControllerDataComposer(data_composer_data)
            case _:
                raise ModelTypeNotImplementedError(
                    ModelName.DATA_COMPOSER,
                    data_composer_data[ModelParam.MODEL_NAME],
                )

    @staticmethod
    def create_controller_collector(
        controller_collector_data: dict,
    ) -> ControllerCollector:
        """
        Create the controller collector model.
        """
        match controller_collector_data[ModelParam.MODEL_NAME]:
            case ModelType.SIMPLE:
                return ControllerCollector()
            case _:
                raise ModelTypeNotImplementedError(
                    ModelName.DATA_COLLECTOR,
                    controller_collector_data[ModelParam.MODEL_NAME],
                )

    @staticmethod
    def create_basestation_finder(
        base_station_links_df: DataFrame, model_data: dict
    ) -> NearestNBaseStationFinder:
        """
        Create the base station finder.
        """
        match model_data[ModelParam.MODEL_NAME]:
            case ModelType.NEAREST:
                logger.debug("Creating nearest base station finder.")
                return NearestNBaseStationFinder(base_station_links_df)
            case _:
                raise ModelTypeNotImplementedError(
                    ModelName.BASE_STATION_FINDER,
                    model_data[ModelParam.MODEL_NAME],
                )

    @staticmethod
    def create_vehicle_data_collector(
        vehicle_data_collector_data: dict,
    ) -> VehicleCollector:
        """
        Create the vehicle data collector model.
        """
        match vehicle_data_collector_data[ModelParam.MODEL_NAME]:
            case ModelType.SIMPLE:
                return VehicleCollector()
            case _:
                raise ModelTypeNotImplementedError(
                    ModelName.DATA_COLLECTOR,
                    vehicle_data_collector_data[ModelParam.MODEL_NAME],
                )

    @staticmethod
    def create_vehicle_neighbour_finder(
        v2v_links: DataFrame,
        vehicle_neighbour_finder_data: dict,
    ) -> TraceVehicleNeighbourFinder:
        """
        Create the vehicle neighbour finder model.
        """
        match vehicle_neighbour_finder_data[ModelParam.MODEL_NAME]:
            case ModelType.TRACE:
                return TraceVehicleNeighbourFinder(v2v_links)
            case _:
                raise ModelTypeNotImplementedError(
                    ModelName.NEIGHBOUR_FINDER,
                    vehicle_neighbour_finder_data[ModelParam.MODEL_NAME],
                )
