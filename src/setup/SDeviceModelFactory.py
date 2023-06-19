from pandas import DataFrame

from src.channel.DInfiniteBandwidthCellTowerChannel import InfiniteBandwidthCellTowerChannel
from src.channel.DInfiniteBandwidthControllerChannel import InfiniteBandwidthControllerChannel
from src.channel.DInfiniteBandwidthUEChannel import InfiniteBandwidthUEChannel
from src.models.DStaticUEMobility import StaticUEMobility
from src.models.DTraceTowerFinder import TraceTowerFinder
from src.models.DTraceUECoverage import TraceUECoverage
from src.models.DTraceUEMobility import TraceMobility


class DeviceModelFactory:
    def __init__(self):
        """
        Initialize the device model factory.
        """
        pass

    @staticmethod
    def create_ue_channel(channel_model_data: dict) -> InfiniteBandwidthUEChannel:
        """
        Create the ue models.
        """
        if channel_model_data['name'] == 'infinite_bandwidth':
            return InfiniteBandwidthUEChannel()
        else:
            raise NotImplementedError(f"UE channel model {channel_model_data['name']} is not implemented.")

    @staticmethod
    def create_controller_channel(channel_model_data: dict, controller_links: DataFrame) -> InfiniteBandwidthControllerChannel:
        """
        Create the controller models.
        """
        if channel_model_data['name'] == 'infinite_bandwidth':
            return InfiniteBandwidthControllerChannel(controller_links)
        else:
            raise NotImplementedError(f"Controller channel model {channel_model_data['name']} is not implemented.")

    @staticmethod
    def create_cell_tower_channel(cell_tower_model_data: dict) -> InfiniteBandwidthCellTowerChannel:
        """
        Create the cell tower models.
        """
        if cell_tower_model_data['name'] == 'infinite_bandwidth':
            return InfiniteBandwidthCellTowerChannel()
        else:
            raise NotImplementedError(f"Cell tower channel model {cell_tower_model_data['name']} is not implemented.")

    @staticmethod
    def create_coverage(coverage_data: DataFrame) -> TraceUECoverage:
        """
        Creates a coverage model.
        """
        if coverage_data is not None and len(coverage_data) > 0:
            return TraceUECoverage(coverage_data)
        else:
            raise NotImplementedError("Other coverage models are not implemented.")

    @staticmethod
    def create_mobility(positions: DataFrame) -> StaticUEMobility | TraceMobility:
        """
        Create a mobility model from the given parameters.

        Parameters
        ----------
        positions : dict
            Dictionary containing all the positions.
        """
        if len(positions) == 1:
            return StaticUEMobility(positions)
        elif len(positions) > 1:
            return TraceMobility(positions)
        else:
            raise NotImplementedError("Other mobility models are not implemented.")

    @staticmethod
    def create_tower_finder(nearest_towers_df: DataFrame) -> TraceTowerFinder:
        """
        Creates a tower finder model.

        Parameters
        ----------
        nearest_towers_df : DataFrame
            DataFrame containing the nearest towers.
        """
        if len(nearest_towers_df) > 0:
            return TraceTowerFinder(nearest_towers_df)
        else:
            raise NotImplementedError("Other tower finder models are not implemented.")
