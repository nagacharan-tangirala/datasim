from abc import abstractmethod

import pandas as pd
from mesa import Agent


class BaseCellTower(Agent):
    def __init__(self, node_id: int, node_data: pd.Series, sim_model=None):
        """
        Initialize the node class.

        Parameters
        ----------
        node_data : pd.Series
            Series containing all the parameters for the node.
        """
        super().__init__(node_id, sim_model)
        self.location = [node_data['x'], node_data['y']]

    def get_id(self) -> int:
        """
        Get the ID of the node.

        Returns
        ----------
        int
            The ID of the ndoe.
        """
        return self.unique_id

    def get_position(self) -> list[float]:
        """
        Get the location of the node.

        Returns
        ----------
        tuple
            Tuple containing the x and y coordinates of the node.
        """
        return self.location

    @abstractmethod
    def step(self):
        """
        Step function for the agent.
        """
        pass

    @abstractmethod
    def receive_data(self, agent_id: int, data: float):
        """
        Receive data from the agents.
        """
        pass
