import pandas as pd

from src.channel.DInfiniteBandwidthUEChannel import InfiniteBandwidthUEChannel
from src.channel.DInfiniteBandwidthControllerChannel import InfiniteBandwidthControllerChannel
from src.channel.DInfiniteBandwidthCellTowerChannel import InfiniteBandwidthCellTowerChannel
from src.models.DStaticMobility import StaticMobility
from src.models.DTraceCoverage import AgentTraceCoverage
from src.models.DTraceMobility import TraceMobility


class DeviceModelFactory:
    def __init__(self):
        """
        Initialize the device model factory.
        """
        pass

    @staticmethod
    def create_agent_channel(channel_model_data: dict) -> InfiniteBandwidthUEChannel:
        """
        Create the agent models.
        """
        if channel_model_data['name'] == 'infinite_bandwidth':
            return InfiniteBandwidthUEChannel()
        else:
            raise NotImplementedError(f"Agent channel model {channel_model_data['name']} is not implemented.")

    @staticmethod
    def create_controller_channel(channel_model_data: dict, controller_links: pd.DataFrame) -> InfiniteBandwidthControllerChannel:
        """
        Create the controller models.
        """
        if channel_model_data['name'] == 'infinite_bandwidth':
            return InfiniteBandwidthControllerChannel(controller_links)
        else:
            raise NotImplementedError(f"Controller channel model {channel_model_data['name']} is not implemented.")

    @staticmethod
    def create_node_channel(node_model_data: dict) -> InfiniteBandwidthCellTowerChannel:
        """
        Create the node models.
        """
        if node_model_data['name'] == 'infinite_bandwidth':
            return InfiniteBandwidthCellTowerChannel()
        else:
            raise NotImplementedError(f"Node channel model {node_model_data['name']} is not implemented.")

    @staticmethod
    def create_coverage(coverage_data: pd.DataFrame) -> AgentTraceCoverage:
        """
        Creates a coverage model.
        """
        if coverage_data is not None and len(coverage_data) > 0:
            return AgentTraceCoverage(coverage_data)
        else:
            raise NotImplementedError("Other coverage models are not implemented.")

    @staticmethod
    def create_mobility(positions: dict) -> StaticMobility | TraceMobility:
        """
        Create a mobility model from the given parameters.

        Parameters
        ----------
        positions : dict
            Dictionary containing all the positions.
        """
        if len(positions) == 1:
            return StaticMobility(positions)
        elif len(positions) > 1:
            return TraceMobility(positions)
        else:
            raise NotImplementedError("Other mobility models are not implemented.")
