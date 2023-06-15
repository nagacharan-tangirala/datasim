from abc import abstractmethod

from pandas import Series
from mesa import Agent


class BaseCellTower(Agent):
    def __init__(self, cell_tower_id: int, cell_tower_data: Series, sim_model=None):
        """
        Initialize the cell tower class.

        Parameters
        ----------
        cell_tower_data : Series
            Series containing all the parameters for the cell tower.
        """
        super().__init__(cell_tower_id, sim_model)
        self.location = [cell_tower_data['x'], cell_tower_data['y']]

        self.total_incoming_data = 0

    def get_id(self) -> int:
        """
        Get the ID of the node.

        Returns
        ----------
        int
            The ID of the cell tower.
        """
        return self.unique_id

    def get_incoming_data(self) -> float:
        """
        Get the total incoming data from the agents.
        """
        return self.total_incoming_data

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

    @abstractmethod
    def receive_data(self, ue_id: int, data: float):
        """
        Receive data from the ues.
        """
        pass
