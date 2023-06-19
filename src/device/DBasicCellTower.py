from pandas import Series

from src.device.BCellTower import BaseCellTower
from src.device.DManytoOneData import ManytoOneData
from src.device.DOnetoOneData import OnetoOneData


class BasicCellTower(BaseCellTower):
    def __init__(self, cell_tower_id, cell_tower_data: Series):
        """
        Initialize the base station.

        Parameters
        ----------
        cell_tower_data : Series
            Series containing all the parameters for the base station.
        """
        super().__init__(cell_tower_id, cell_tower_data)

        self.incoming_ues_data: dict[int, OnetoOneData] = {}

    def step(self):
        """
        Step function for the ue.
        """
        # Compute the total data received from the ues.
        total_data = 0
        agent_ids = []
        for data in self.incoming_ues_data.values():
            total_data = total_data + data.get_size_in_bits()
            agent_ids.append(data.get_origin())

        # Get the current time from the first ue.
        current_time = self.incoming_ues_data[list(self.incoming_ues_data.keys())[0]].get_time_stamp()

        # Clear the incoming data.
        self.incoming_ues_data.clear()

        # Create a single data unit representing the total data received from the ues.
        self.ues_data = ManytoOneData(current_time, total_data, agent_ids, self.get_id())

    def receive_data(self, ue_id: int, data: OnetoOneData):
        """
        Receive data from the ues.
        """
        self.incoming_ues_data[ue_id] = data
