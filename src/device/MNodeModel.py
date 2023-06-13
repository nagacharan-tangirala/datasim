import pandas as pd
from mesa import Model
from mesa.time import BaseScheduler

from src.channel.BNodeChannel import NodeChannelBase
from src.device.BNode import NodeBase
from src.setup.SDeviceModelFactory import DeviceModelFactory


class NodeModel(Model):
    def __init__(self, nodes: dict[int, NodeBase], node_link_data: pd.DataFrame, node_model_data: dict):
        """
        Initialize the node model.
        """
        super().__init__()

        self.nodes: dict[int, NodeBase] = nodes
        self.node_link_data: pd.DataFrame = node_link_data

        # All models are defined here
        self.node_channel: NodeChannelBase | None = None

        self.schedule: BaseScheduler = BaseScheduler(self)
        self._create_models(node_model_data)

    def get_node_channel(self) -> NodeChannelBase:
        """
        Get the node channel.
        """
        return self.node_channel

    def _create_models(self, node_model_data: dict) -> None:
        """
        Create all the models for the nodes.
        """
        # Create the node channel model
        model_factory = DeviceModelFactory()
        self.node_channel = model_factory.create_node_channel(node_model_data['channel'])

    def step(self) -> None:
        """
        Step function for the model. This function is called every time step.
        """
        # Step the scheduler
        self.schedule.step()
