import logging

from models.static_links import B2CAllocator, R2BAllocator, R2RAllocator
from pandas import DataFrame

from src.core.constants import ModelName, ModelParam, ModelType
from src.core.exceptions import ModelTypeNotImplementedError
from src.models.allocator import (
    V2BAllocator,
    V2RAllocator,
    V2VAllocator,
)
from src.models.collector import ControllerCollector, RSUCollector, VehicleCollector
from src.models.composer import (
    BaseStationDataComposer,
    ControllerDataComposer,
    RSUDataComposer,
    VehicleDataComposer,
)
from src.models.mobility import StaticMobilityModel, TraceMobilityModel
from src.models.simplifier import (
    BaseStationDataSimplifier,
    RSUDataSimplifier,
    VehicleDataSimplifier,
)

logger = logging.getLogger(__name__)


def create_mobility_model(model_data: dict) -> StaticMobilityModel | TraceMobilityModel:
    """
    Create a mobility model from the given parameters.

    Parameters
    ----------
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    StaticMobilityModel | TraceMobilityModel
        The mobility model.
    """
    model_name = model_data[ModelParam.MODEL_NAME]
    match model_name:
        case ModelType.STATIC:
            return StaticMobilityModel()
        case ModelType.SIMPLE:
            logger.debug("Creating simple mobility model.")
            return TraceMobilityModel()
        case _:
            raise NotImplementedError(f"Mobility model {model_name} not implemented.")


def create_vehicle_data_composer(model_data: dict) -> VehicleDataComposer:
    """
    Create the vehicle data composer model.

    Parameters
    ----------
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    VehicleDataComposer
        The vehicle data composer model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.SIMPLE:
            return VehicleDataComposer(model_data)
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.DATA_COMPOSER,
                model_data[ModelParam.MODEL_NAME],
            )


def create_rsu_data_composer(model_data: dict) -> RSUDataComposer:
    """
    Create the rsu data composer model.

    Parameters
    ----------
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    RSUDataComposer
        The rsu data composer model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.SIMPLE:
            return RSUDataComposer(model_data)
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.DATA_COMPOSER,
                model_data[ModelParam.MODEL_NAME],
            )


def create_base_station_data_composer(model_data: dict) -> BaseStationDataComposer:
    """
    Create the base station data composer model.

    Parameters
    ----------
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    BaseStationDataComposer
        The base station data composer model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.SIMPLE:
            return BaseStationDataComposer(model_data)
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.DATA_COMPOSER,
                model_data[ModelParam.MODEL_NAME],
            )


def create_controller_data_composer(model_data: dict) -> ControllerDataComposer:
    """
    Create the controller data composer model.

    Parameters
    ----------
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    ControllerDataComposer
        The controller data composer model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.SIMPLE:
            return ControllerDataComposer(model_data)
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.DATA_COMPOSER,
                model_data[ModelParam.MODEL_NAME],
            )


def create_vehicle_data_simplifier(model_data: dict) -> VehicleDataSimplifier:
    """
    Create the vehicle data simplifier model.

    Parameters
    ----------
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    VehicleDataSimplifier
        The vehicle data simplifier model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.SIMPLE:
            return VehicleDataSimplifier(model_data)
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.DATA_SIMPLIFIER,
                model_data[ModelParam.MODEL_NAME],
            )


def create_rsu_data_simplifier(model_data: dict) -> RSUDataSimplifier:
    """
    Create the rsu data simplifier model.

    Parameters
    ----------
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    RSUDataSimplifier
        The rsu data simplifier model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.SIMPLE:
            return RSUDataSimplifier(model_data)
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.DATA_SIMPLIFIER,
                model_data[ModelParam.MODEL_NAME],
            )


def create_base_station_data_simplifier(model_data: dict) -> BaseStationDataSimplifier:
    """
    Create the base station data simplifier model.

    Parameters
    ----------
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    BaseStationDataSimplifier
        The base station data simplifier model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.SIMPLE:
            return BaseStationDataSimplifier(model_data)
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.DATA_SIMPLIFIER,
                model_data[ModelParam.MODEL_NAME],
            )


def create_vehicle_data_collector(model_data: dict) -> VehicleCollector:
    """
    Create the vehicle data collector model.

    Parameters
    ----------
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    VehicleCollector
        The vehicle data collector model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.SIMPLE:
            return VehicleCollector()
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.DATA_COLLECTOR,
                model_data[ModelParam.MODEL_NAME],
            )


def create_rsu_data_collector(model_data: dict) -> RSUCollector:
    """
    Create the rsu data collector model.

    Parameters
    ----------
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    RSUCollector
        The rsu collector model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.SIMPLE:
            return RSUCollector()
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.DATA_COLLECTOR,
                model_data[ModelParam.MODEL_NAME],
            )


def create_controller_data_collector(model_data: dict) -> ControllerCollector:
    """
    Create the controller data collector model.

    Parameters
    ----------
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    ControllerCollector
        The controller collector model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.SIMPLE:
            return ControllerCollector()
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.DATA_COLLECTOR,
                model_data[ModelParam.MODEL_NAME],
            )


def create_v2b_allocator(v2b_links_df: DataFrame, model_data: dict) -> V2BAllocator:
    """
    Create the v2b allocator.

    Parameters
    ----------
    v2b_links_df : DataFrame
        The DataFrame containing the links between vehicles and base stations.
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    V2BAllocator
        The v2b allocator model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.NEAREST:
            logger.debug("Creating nearest base station finder.")
            return V2BAllocator(v2b_links_df, model_data[ModelParam.STRATEGY])
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.V2B_ALLOCATOR,
                model_data[ModelParam.MODEL_NAME],
            )


def create_v2r_allocator(v2r_links_df: DataFrame, model_data: dict) -> V2RAllocator:
    """
    Create the v2r allocator.

    Parameters
    ----------
    v2r_links_df : DataFrame
        The DataFrame containing the links between vehicles and RSUs.
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    V2RAllocator
        The v2r allocator model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.NEAREST:
            logger.debug("Creating nearest RSU finder.")
            return V2RAllocator(v2r_links_df, model_data[ModelParam.STRATEGY])
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.V2R_ALLOCATOR,
                model_data[ModelParam.MODEL_NAME],
            )


def create_v2v_allocator(v2v_links: DataFrame, model_data: dict) -> V2VAllocator:
    """
    Create the v2v allocator.

    Parameters
    ----------
    v2v_links : DataFrame
        The DataFrame containing the links between vehicles.
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    V2VAllocator
        The v2v allocator model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.SIMPLE:
            return V2VAllocator(v2v_links, model_data[ModelParam.STRATEGY])
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.V2V_ALLOCATOR,
                model_data[ModelParam.MODEL_NAME],
            )


def create_b2c_allocator(b2c_links: DataFrame, model_data: dict) -> B2CAllocator:
    """
    Create the b2c allocator.

    Parameters
    ----------
    b2c_links : DataFrame
        The DataFrame containing the links between base stations and controllers.
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    B2CAllocator
        The b2c allocator model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.STATIC:
            return B2CAllocator(b2c_links, model_data[ModelParam.STRATEGY])
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.B2C_ALLOCATOR,
                model_data[ModelParam.MODEL_NAME],
            )


def create_r2b_allocator(r2b_links: DataFrame, model_data: dict) -> R2BAllocator:
    """
    Create the r2b allocator.

    Parameters
    ----------
    r2b_links : DataFrame
        The DataFrame containing the links between RSUs and base stations.
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    R2BAllocator
        The r2b allocator model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.STATIC:
            return R2BAllocator(r2b_links, model_data[ModelParam.STRATEGY])
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.R2B_ALLOCATOR,
                model_data[ModelParam.MODEL_NAME],
            )


def create_r2r_allocator(r2r_links: DataFrame, model_data: dict) -> R2RAllocator:
    """
    Create the r2r allocator.

    Parameters
    ----------
    r2r_links : DataFrame
        The DataFrame containing the links between RSUs.
    model_data : dict
        Dictionary containing all the parameters of the model.

    Returns
    -------
    R2RAllocator
        The r2r allocator model.
    """
    match model_data[ModelParam.MODEL_NAME]:
        case ModelType.STATIC:
            return R2RAllocator(r2r_links, model_data[ModelParam.STRATEGY])
        case _:
            raise ModelTypeNotImplementedError(
                ModelName.R2R_ALLOCATOR,
                model_data[ModelParam.MODEL_NAME],
            )
