from collections import namedtuple

from mesa import Model

from src.data.TowerDataHandler import TowerDataHandler


class TowerDataHandlerModel(Model):
    def __init__(self, tower_id: int, model_data: dict):
        """
        Initialize the data handler model.
        """
        super().__init__()

        self._tower_id: int = tower_id
        self.current_time: int = 0

        self._data_handler = TowerDataHandler(self._tower_id, model_data)
        self._data_from_ues: dict[int, namedtuple] = {}

    def step(self, *args, **kwargs) -> None:
        """
        Step through the data handler model.
        """
        # Get the current time
        current_time: int = int(args[0])

        # Set the current time
        self._data_handler.current_time = current_time
