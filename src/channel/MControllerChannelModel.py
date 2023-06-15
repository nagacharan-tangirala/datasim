from mesa import Model
from mesa.time import BaseScheduler

from src.device.BCellTower import BaseCellTower


class ControllerChannelModel(Model):
    def __init__(self, nodes: dict[int, BaseCellTower]):
        """
        Initialize the controller channel model.
        """
        super().__init__()
        self.schedule: BaseScheduler = BaseScheduler(self)

        self.nodes = nodes

    def add_channel(self, channel):
        """
        Add the channel to the model.
        """
        # Add nodes to the channel
        channel.assign_nodes(self.nodes)

        self.schedule.add(channel)

    def step(self):
        """
        Step through the controller channel model.
        """
        self.schedule.step()
