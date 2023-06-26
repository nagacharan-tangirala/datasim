from abc import abstractmethod

from pandas import DataFrame


class TowerLookupBase:
    def __init__(self, cell_towers: dict, tower_links_df: DataFrame):
        """
        Initialize the tower look up model.
        """
        super().__init__(0, None)

        self._cell_towers: dict = cell_towers
        self._tower_links_df: DataFrame = tower_links_df

        self._current_ts_tower_links_df: DataFrame = DataFrame()

        self._current_time: int = -1

    @property
    def current_time(self) -> int:
        """ Get the current time."""
        return self._current_time

    @current_time.setter
    def current_time(self, value: int) -> None:
        """ Set the current time."""
        self._current_time = value

    @abstractmethod
    def step(self) -> None:
        """
        Step through the tower look up model.
        """
        pass

    @abstractmethod
    def select_tower_for_ue(self, ue_id: int) -> int:
        """
        Select towers for the ue.
        """
        pass
