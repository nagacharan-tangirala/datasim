from abc import abstractmethod

from mesa import Agent
from pandas import Series


class BaseCellTower(Agent):
    def __init__(self, cell_tower_id: int, cell_tower_data: Series, cell_tower_model_data: dict, sim_model=None):
        """
        Initialize the cell tower class.

        Parameters
        ----------
        cell_tower_data : Series
            Series containing all the parameters for the cell tower.
        """
        super().__init__(cell_tower_id, sim_model)
        self.location = [cell_tower_data['x'], cell_tower_data['y']]

        self.cell_tower_model_data = cell_tower_model_data

    def get_id(self) -> int:
        """
        Get the ID of the node.

        Returns
        ----------
        int
            The ID of the cell tower.
        """
        return self.unique_id

    def get_position(self) -> list[float]:
        """
        Get the location of the cell tower.

        Returns
        ----------
        tuple
            Tuple containing the x and y coordinates of the cell tower.
        """
        return self.location

    @abstractmethod
    def step(self):
        """
        Step function for the cell tower
        """
        pass
