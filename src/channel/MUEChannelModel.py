from mesa import Model
from mesa.time import BaseScheduler

from src.channel.BUEChannel import BaseUEChannel
from src.device.BCellTower import BaseCellTower


class UEChannelModel(Model):
    def __init__(self, nodes: dict[int, BaseCellTower]):
        """
        Initialize the agent channel model.
        """
        super().__init__()

        self.nodes: dict = nodes
        self.schedule: BaseScheduler = BaseScheduler(self)

    def step(self, *args, **kwargs) -> None:
        """
        Step through the agent channel model.
        """
        # Set the current time for the agents
        self.schedule.step()

    def add_channel(self, channel: BaseUEChannel) -> None:
        """
        Add the channel to the model.
        """
        # Add nodes to the channel
        channel.assign_nodes(self.nodes)

        # Add the channel to the scheduler
        self.schedule.add(channel)
