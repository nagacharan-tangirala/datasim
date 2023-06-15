import pandas as pd
from mesa import Model
from mesa.time import BaseScheduler

from src.channel.BCellTowerChannel import BaseCellTowerChannel
from src.device.BCellTower import BaseCellTower
from src.setup.SDeviceModelFactory import DeviceModelFactory


class CellTowerModel(Model):
    def __init__(self, nodes: dict[int, BaseCellTower], node_link_data: pd.DataFrame, node_model_data: dict):
        """
        Initialize the node model.
        """
        super().__init__()

        self.nodes: dict[int, BaseCellTower] = nodes
        self.node_link_data: pd.DataFrame = node_link_data

        # All models are defined here
        self.node_channel: BaseCellTowerChannel | None = None

        self.schedule: BaseScheduler = BaseScheduler(self)
        self._create_models(node_model_data)
        self._add_nodes_to_scheduler()

    def get_node_channel(self) -> BaseCellTowerChannel:
        """
        Get the node channel.
        """
        return self.node_channel

    def _add_nodes_to_scheduler(self) -> None:
        """
        Add the nodes to the scheduler.
        """
        for node in self.nodes.values():
            self.schedule.add(node)

    def _create_models(self, node_model_data: dict) -> None:
        """
        Create all the models for the nodes.
        """
        # Iterate through the models and create them
        model_factory = DeviceModelFactory()
        for model_id, model_data in node_model_data.items():
            if model_data['type'] == 'channel':
                self.node_channel = model_factory.create_node_channel(model_data)
            else:
                raise ValueError(f"Unknown model type {model_data['type']}")

    def step(self) -> None:
        """
        Step function for the model. This function is called every time step.
        """
        # Step the scheduler
        self.schedule.step()
