from mesa import Model
from mesa.time import BaseScheduler

from src.device.BNode import NodeBase


class NodeChannelModel(Model):
    def __init__(self, nodes: dict[int, NodeBase]):
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

    def step(self):
        """
        Step through the node channel model.
        """
        self.schedule.step()
