from collections import namedtuple

from pandas import Series

from src.data.MTowerDataHandlerModel import TowerDataHandlerModel
from src.data.UEDataHandler import UEDataHandler
from src.device.BCellTower import CellTowerBase


class BasicCellTower(CellTowerBase):
    def __init__(self, cell_tower_id, cell_tower_data: Series, cell_tower_models_data: dict):
        """
        Initialize the base station.

        Parameters
        ----------
        cell_tower_data : Series
            Series containing all the parameters for the base station.
        """
        super().__init__(cell_tower_id, cell_tower_data)

        self._create_models(cell_tower_models_data)

    def _create_models(self, cell_tower_models_data: dict) -> None:
        self._data_handler_model: TowerDataHandlerModel = TowerDataHandlerModel(self.unique_id, cell_tower_models_data['data'])

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
        self.ues_data = UEDataHandler(current_time, total_data, agent_ids, self.get_id())

    def receive_data(self, ue_id: int, ue_data: namedtuple):
        """
        Receive data from the ues.
        """
        self.incoming_ues_data[ue_id] = data

    def _create_data_handler(self) -> TowerDataHandlerModel:
        """
        Create the data handler model.
        """
        return
