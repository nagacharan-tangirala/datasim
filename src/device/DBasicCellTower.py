from pandas import Series

from src.device.BCellTower import BaseCellTower


class BasicCellTower(BaseCellTower):
    """
    Base station class designed to mimic the behavior of base stations.
    """

    def __init__(self, cell_tower_id, cell_tower_data: Series):
        """
        Initialize the base station.

        Parameters
        ----------
        cell_tower_data : Series
            Series containing all the parameters for the base station.
        """
        super().__init__(cell_tower_id, cell_tower_data)

        self.incoming_ues_data = {}

    def step(self):
        """
        Step function for the ue.
        """
        # Compute the total data received from the ues.
        total_data = 0
        for ue_id, data in self.incoming_ues_data.items():
            total_data = total_data + data

        self.incoming_ues_data.clear()
        self.total_incoming_data = total_data

    def receive_data(self, ue_id: int, data: float):
        """
        Receive data from the ues.
        """
        self.incoming_ues_data[ue_id] = data
