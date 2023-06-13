import pandas as pd
from mesa import Model
from mesa.time import BaseScheduler

from src.channel.BNodeChannel import NodeChannelBase
from src.device.BNode import NodeBase


class NodeModel(Model):
    def __init__(self, nodes: dict[int, NodeBase], node_link_data: pd.DataFrame):
        """
        Initialize the node model.
        """
        super().__init__()

        self.nodes: dict[int, NodeBase] = nodes
        self.node_link_data: pd.DataFrame = node_link_data

        self.node_channel: NodeChannelBase | None = None

        self.schedule: BaseScheduler = BaseScheduler(self)

    def get_node_channel(self) -> NodeChannelBase:
        """
        Get the node channel.
        """
        return self.node_channel

    def step(self) -> None:
        """
        Step function for the model. This function is called every time step.
        """
        # Step the scheduler
        self.schedule.step()
