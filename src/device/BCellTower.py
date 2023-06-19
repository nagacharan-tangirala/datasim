from abc import abstractmethod

from mesa import Agent
from pandas import Series

from src.device.DManytoOneData import ManytoOneData
from src.device.DOnetoOneData import OnetoOneData


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

        self.ues_data: ManytoOneData | None = None
        self.controller_data: OnetoOneData | None = None

    def get_id(self) -> int:
        """
        Get the ID of the node.

        Returns
        ----------
        int
            The ID of the cell tower.
        """
        return self.unique_id

    def get_data_from_ues(self) -> ManytoOneData:
        """
        Get the data received from the ues.
        """
        return self.ues_data

    def get_data_from_controller(self) -> OnetoOneData:
        """
        Get the data received from the controller.
        """
        return self.controller_data

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
    def receive_data(self, ue_id: int, data: ManytoOneData):
        """
        Receive data from the ues.
        """
        pass
