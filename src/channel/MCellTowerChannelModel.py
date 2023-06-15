from mesa import Model
from mesa.time import BaseScheduler

from src.device.BCellTower import BaseCellTower


class CellTowerChannelModel(Model):
    def __init__(self, nodes: dict[int, BaseCellTower]):
        """
        Initialize the node channel model.
        """
        super().__init__()

        self.nodes = nodes
        self.schedule: BaseScheduler = BaseScheduler(self)

    def add_channel(self, channel):
        """
        Add the channel to the model.
        """
        self.schedule.add(channel)

    def step(self, *args, **kwargs):
        """
        Step through the node channel model.
        """
        current_time = args[0]
        self.schedule.step()
