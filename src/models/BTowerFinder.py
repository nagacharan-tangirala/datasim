from abc import abstractmethod

from mesa import Agent

from src.core.CustomExceptions import NearestTowerNotAssignedError


class TowerFinderBase(Agent):
    def __init__(self):
        """
        Initialize the tower finder.
        """
        super().__init__(0, None)

        self.current_time: int = 0
        self.nearest_tower: int = -1

    def get_nearest_tower(self) -> int:
        """
        Get the nearest tower.

        Returns
        ----------
        int
            The nearest tower.
        """
        if self.nearest_tower == -1:
            raise NearestTowerNotAssignedError

        return self.nearest_tower

    def set_current_time(self, current_time: int) -> None:
        """
        Set the current time for the tower finder.

        Parameters
        ----------
        current_time : int
            The current time.
        """
        self.current_time = current_time

    @abstractmethod
    def step(self) -> None:
        """
        Execute the step.
        """
        pass
