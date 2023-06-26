from abc import abstractmethod

from mesa import Agent
from pandas import DataFrame


class UEMobilityBase(Agent):
    def __init__(self, positions: DataFrame):
        """
        Initialize the mobility model.
        """
        super().__init__(0, None)

        self._positions: DataFrame = positions
        self._current_location: list[float] = []

        self.current_time: int = 0
        self._type: str = ''

    @property
    def type(self) -> str:
        """Get the type of the mobility model."""
        return self._type

    @property
    def current_location(self) -> list[float]:
        """Get the current location of the ue."""
        return self._current_location

    @abstractmethod
    def step(self):
        """
        Step through the model, should be implemented by the child class.
        """
        pass

    @abstractmethod
    def update_positions(self, positions: DataFrame) -> None:
        """
        Update the positions of the ue.

        Parameters
        ----------
        positions : DataFrame
            The positions of the ue.
        """
        pass

    def get_start_and_end_time(self) -> tuple[int, int]:
        """
        Get the start and end time of the ue.

        Returns
        ----------
        tuple
            The start and end time of the ue.
        """
        return self._positions["time"].min(), self._positions["time"].max()

    def activate(self):
        """
        Activate the mobility model.
        """
        self.model.schedule.add(self)
