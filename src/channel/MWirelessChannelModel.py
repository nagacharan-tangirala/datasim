from mesa import Model
from mesa.time import BaseScheduler
from pandas import DataFrame

from src.channel.BWirelessChannel import WirelessChannelBase
from src.channel.DBasicWirelessChannel import BasicWirelessChannel


class WirelessChannelModel(Model):
    def __init__(self, cell_towers: dict, ue_links_df: DataFrame, tower_links_df: DataFrame, model_data: dict):
        """
        Initialize the wireless channel model.
        """
        super().__init__()

        self._model_data: dict = model_data
        self.schedule: BaseScheduler = BaseScheduler(self)

        self._wireless_channel: WirelessChannelBase = self._create_wireless_channel(cell_towers, ue_links_df, tower_links_df, model_data)

    def step(self, *args, **kwargs) -> None:
        """
        Step through the wireless channel model.
        """
        # Get the current time
        self._wireless_channel.current_time = int(args[0])
        self.schedule.step()

    def _create_wireless_channel(self, cell_towers: dict, ue_links_df: DataFrame, tower_links_df: DataFrame, model_data: dict) -> BasicWirelessChannel:
        """
        Create the wireless channel using the model data.
        """
        if self._model_data['name'] == "basic":
            return BasicWirelessChannel(cell_towers, ue_links_df, tower_links_df, model_data['models'])

        self.schedule.add(self._wireless_channel)
