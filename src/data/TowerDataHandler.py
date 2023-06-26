from collections import namedtuple

from mesa import Agent


class TowerDataHandler(Agent):
    def __init__(self, tower_id: int, model_data: dict):
        """
        Initialize the tower data.
        """
        super().__init__(tower_id, None)

        self._tower_id: int = tower_id

        self._time_stamp: int = -1
        self._data_from_ues: dict[int, namedtuple] = {}
        # self._data_from_ues: namedtuple = namedtuple('tower_data', ['ts', 'data_size', 'ue_ids'])
        self._data_from_controller: dict[int, dict[int, namedtuple]] = {}

    @property
    def tower_id(self) -> int:
        """Get the tower id."""
        return self._tower_id

    @property
    def time_stamp(self) -> int:
        """Get the time stamp."""
        return self._time_stamp

    def step(self) -> None:
        """
        Step the data handler.
        """
        # Take the data received from the controler

    def collect_ue_data(self, ue_id: int, ue_data: namedtuple) -> None:
        """
        Collect UE data.
        """
        self._ue_incoming_data[ue_id] = ue_data
