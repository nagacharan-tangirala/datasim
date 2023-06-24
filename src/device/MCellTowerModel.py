from mesa import Model
from mesa.time import BaseScheduler

from src.device.BCellTower import BaseCellTower


class CellTowerModel(Model):
    def __init__(self, cell_towers: dict[int, BaseCellTower]):
        """
        Initialize the cell tower model.
        """
        super().__init__()

        self.cell_towers: dict[int, BaseCellTower] = cell_towers

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
