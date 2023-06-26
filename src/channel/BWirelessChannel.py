from abc import abstractmethod

from mesa import Agent
from pandas import DataFrame

from src.device.BCellTower import CellTowerBase
from src.device.BUE import UEBase, UEData


class WirelessChannelBase(Agent):
    def __init__(self, cell_towers: dict, ue_links_df: DataFrame, tower_links_df: DataFrame):
        """
        Initialize the wireless channel.
        """
        super().__init__(0, None)

        self._ues: dict[int, UEBase] = {}
        self._cell_towers: dict[int, CellTowerBase] = cell_towers

        self._ue_links: DataFrame = ue_links_df
        self._tower_links: DataFrame = tower_links_df

        self.data_from_ues: dict[int, UEData] = {}
        self.processed_ue_data: dict[int, UEData] = {}
        self.data_to_towers: dict[int, dict[int, UEData]] = {}
        self.data_from_controller: dict[dict[int, UEData]] = {}

        self._current_time: int = -1

    @property
    def current_time(self) -> int:
        """Get the time stamp."""
        return self._current_time

    @current_time.setter
    def current_time(self, value: int) -> None:
        """ Set the current time."""
        self._current_time = value

    @abstractmethod
    def step(self) -> None:
        """
        Step through the ue channel.
        """
        pass

    def add_ue(self, ue: UEBase) -> None:
        """
        Add an ue to the channel.
        """
        self._ues[ue.unique_id] = ue

    def remove_ue(self, ue: UEBase) -> None:
        """
        Remove an ue from the channel.
        """
        self._ues.pop(ue.unique_id)
