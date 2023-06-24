from pandas import DataFrame

from src.channel.DInfiniteBandwidthCellTowerChannel import InfiniteBandwidthCellTowerChannel
from src.channel.DInfiniteBandwidthControllerChannel import InfiniteBandwidthControllerChannel
from src.channel.DInfiniteBandwidthUEChannel import InfiniteBandwidthUEChannel


class ChannelFactory:
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
