import pandas as pd

from src.device.BNode import NodeBase


class BaseStation(NodeBase):
    def __init__(self, node_id, node_data: pd.Series):
        """
        Initialize the base station.

        Parameters
        ----------
        node_data : pd.Series
            Series containing all the parameters for the base station.
        """
        super().__init__(node_id, node_data)

        self.incoming_agents_data = {}

    def step(self):
        """
        Step function for the agent.
        """
        # Compute the total data received from the agents.
        total_data = 0
        for agent_id, data in self.incoming_agents_data.items():
            total_data = total_data + data

        self.incoming_agents_data.clear()
        self.total_incoming_data = total_data

    def receive_data(self, agent_id: int, data: float):
        """
        Receive data from the agents.
        """
        self.incoming_agents_data[agent_id] = data
