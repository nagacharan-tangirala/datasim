from abc import abstractmethod

from mesa import Agent
from pandas import DataFrame


class UEMobilityBase(Agent):
    def __init__(self, positions: DataFrame):
        """
        Initialize the mobility model.
        """
        super().__init__(0, None)

        self.positions: DataFrame = positions
        self.current_time: int = 0
        self.current_location: list[float] = []

    def get_current_location(self) -> list[float]:
        """
        Get the current location of the ue.

        Returns
        ----------
        list
            The current location of the ue.
        """
        return self.current_location

    @abstractmethod
    def step(self):
        """
        Step through the model, should be implemented by the child class.
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        Get the type of the model.

        Returns
        ----------
        str
            The type of the model.
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
        pass

    def activate(self):
        """
        Activate the mobility model.
        """
        self.model.schedule.add(self)

    def set_current_time(self, current_time: int) -> None:
        """
        Set the current time for the coverage model.

        Parameters
        ----------
        current_time : int
            The current time.
        """
        self.current_time = current_time
