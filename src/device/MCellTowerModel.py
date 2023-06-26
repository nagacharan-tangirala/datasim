from mesa import Model
from mesa.time import BaseScheduler

from src.core.CustomExceptions import DuplicateDeviceFoundError
from src.device.BCellTower import CellTowerBase


class CellTowerModel(Model):
    def __init__(self, cell_towers: dict[int, CellTowerBase]):
        """
        Initialize the cell tower model.
        """
        super().__init__()

        self.cell_towers: dict[int, CellTowerBase] = cell_towers

        self.schedule: BaseScheduler = BaseScheduler(self)
        self._add_cell_towers_to_scheduler()

    def _add_cell_towers_to_scheduler(self) -> None:
        """
        Add the cell_towers to the scheduler.
        """
        for cell_tower in self.cell_towers.values():
            self.schedule.add(cell_tower)

    def step(self) -> None:
        """
        Step function for the model. This function is called every time step.
        """
        # Step the scheduler
        self.schedule.step()

    def update_cell_towers(self, new_cell_towers):
        """
        Update the cell towers.
        """
        for cell_tower_id, cell_tower in new_cell_towers:
            if cell_tower_id in self.cell_towers:
                raise DuplicateDeviceFoundError(cell_tower_id, 'cell tower')
            self.cell_towers[cell_tower_id] = cell_tower
