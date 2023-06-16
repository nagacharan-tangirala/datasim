from mesa import Model
from mesa.time import BaseScheduler

from src.device.BCellTower import BaseCellTower


class ControllerChannelModel(Model):
    def __init__(self, cell_towers: dict[int, BaseCellTower]):
        """
        Initialize the controller channel model.
        """
        super().__init__()
        self.schedule: BaseScheduler = BaseScheduler(self)

        self.cell_towers = cell_towers

    def add_channel(self, channel):
        """
        Add the channel to the model.
        """
        # Add cell towers to the channel
        channel.assign_cell_towers(self.cell_towers)

        self.schedule.add(channel)

    def step(self):
        """
        Step through the controller channel model.
        """
        self.schedule.step()
