import pandas as pd

from src.device.BCellTower import BaseCellTower


class IntermediateCellTower(BaseCellTower):
    def step(self):
        pass

    def receive_data(self, data: float):
        pass

    def __init__(self, node_id: int, node_data: pd.Series):
        """
        Initialize the intermediate node.

        Parameters
        ----------
        node_data : pd.Series
            Series containing all the parameters for the intermediate node.
        """
        super().__init__(node_id, node_data)

        self.in_range_nodes = []
        self.nodes_data = 0

    def get_collected_data_size(self) -> int:
        """
        Get the collected data size.

        Returns
        ----------
        int
            The collected data size.
        """
        return self.nodes_data

    def update_node(self, time: int):
        """
        Update the node. This includes collecting data from all the agents which are in range.

        Parameters
        ----------
        time : int
            The current time.
        """
        # Get the data collected by the nodes associated with the intermediate node.
        self.nodes_data = 0
        for node in self.in_range_nodes:
            self.nodes_data = self.nodes_data + node.get_collected_data_size(time)
