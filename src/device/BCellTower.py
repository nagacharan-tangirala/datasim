from abc import abstractmethod

from mesa import Agent
from pandas import Series


class CellTowerBase(Agent):
    def __init__(self, cell_tower_id: int, cell_tower_data: Series, sim_model=None):
        """
        Initialize the cell tower class.

        Parameters
        ----------
        cell_tower_data : Series
            Series containing all the parameters for the cell tower.
        """
        super().__init__(cell_tower_id, sim_model)
        self._location = [cell_tower_data['x'], cell_tower_data['y']]

    @property
    def location(self) -> list[float, float]:
        """ Get the location of the cell tower. """
        return self._location

    @abstractmethod
    def step(self):
        """
        Step function for the cell tower
        """
        pass
