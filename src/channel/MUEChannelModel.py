from mesa import Model
from mesa.time import BaseScheduler

from src.channel.BUEChannel import BaseUEChannel
from src.device.BCellTower import BaseCellTower


class UEChannelModel(Model):
    def __init__(self, cell_towers: dict[int, BaseCellTower]):
        """
        Initialize the ue channel model.
        """
        super().__init__()

        self.cell_towers: dict = cell_towers
        self.schedule: BaseScheduler = BaseScheduler(self)

    def step(self, *args, **kwargs) -> None:
        """
        Step through the ue channel model.
        """
        self.schedule.step()

    def add_channel(self, channel: BaseUEChannel) -> None:
        """
        Add the channel to the model.
        """
        # Add cell towers to the channel
        channel.assign_cell_towers(self.cell_towers)

        # Add the channel to the scheduler
        self.schedule.add(channel)
