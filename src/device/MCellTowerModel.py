from pandas import DataFrame
from mesa import Model
from mesa.time import BaseScheduler

from src.channel.BCellTowerChannel import BaseCellTowerChannel
from src.device.BCellTower import BaseCellTower
from src.setup.SDeviceModelFactory import DeviceModelFactory


class CellTowerModel(Model):
    def __init__(self, cell_towers: dict[int, BaseCellTower], cell_tower_link_data: DataFrame, cell_tower_model_data: dict):
        """
        Initialize the cell tower model.
        """
        super().__init__()

        self.cell_towers: dict[int, BaseCellTower] = cell_towers
        self.cell_tower_link_data: DataFrame = cell_tower_link_data

        # All models are defined here
        self.cell_tower_channel: BaseCellTowerChannel | None = None

        self.schedule: BaseScheduler = BaseScheduler(self)
        self._create_models(cell_tower_model_data)
        self._add_cell_towers_to_scheduler()

    def get_cell_tower_channel(self) -> BaseCellTowerChannel:
        """
        Get the cell tower channel.
        """
        return self.cell_tower_channel

    def _add_cell_towers_to_scheduler(self) -> None:
        """
        Add the cell_towers to the scheduler.
        """
        for cell_tower in self.cell_towers.values():
            self.schedule.add(cell_tower)

    def _create_models(self, cell_tower_model_data: dict) -> None:
        """
        Create all the models for the cell_towers.
        """
        # Iterate through the models and create them
        model_factory = DeviceModelFactory()
        for model_id, model_data in cell_tower_model_data.items():
            if model_data['type'] == 'channel':
                self.cell_tower_channel = model_factory.create_cell_tower_channel(model_data)
            else:
                raise ValueError(f"Unknown model type {model_data['type']}")

    def step(self) -> None:
        """
        Step function for the model. This function is called every time step.
        """
        # Step the scheduler
        self.schedule.step()
