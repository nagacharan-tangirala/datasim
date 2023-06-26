from pandas import Series

from src.device.BCellTower import CellTowerBase


class IntermediateCellTower(CellTowerBase):
    def __init__(self, cell_tower_id: int, cell_tower_data: Series, cell_tower_models_data: dict):
        """
        Initialize the intermediate cell_tower.

        Parameters
        ----------
        cell_tower_data : Series
            Series containing all the parameters for the intermediate cell tower.
        """
        super().__init__(cell_tower_id, cell_tower_data, cell_tower_models_data)

        self.in_range_cell_towers = []
        self.cell_towers_data = 0

    def get_collected_data_size(self) -> int:
        """
        Get the collected data size.

        Returns
        ----------
        int
            The collected data size.
        """
        return self.cell_towers_data

    def step(self):
        pass

    def receive_data(self, ue_id, data: float):
        pass

    def update_cell_tower(self, time: int):
        """
        Update the cell tower. This includes collecting data from all the agents which are in range.

        Parameters
        ----------
        time : int
            The current time.
        """
        # Get the data collected by the cell_towers associated with the intermediate cell tower.
        self.cell_towers_data = 0
        for cell_tower in self.in_range_cell_towers:
            self.cell_towers_data = self.cell_towers_data + cell_tower.get_collected_data_size(time)
