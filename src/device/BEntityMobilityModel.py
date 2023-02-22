from abc import ABCMeta, abstractmethod


class MobilityModelBase(metaclass=ABCMeta):
    """Base class for all mobility model classes."""

    def __init__(self, positions):
        """
        Initialize the mobility model.
        """
        self.positions = positions
        self.current_location = [0.0, 0.0]

    def get_current_location(self) -> list[float]:
        """
        Get the current location of the entity.

        Returns
        ----------
        list
            The current location of the entity.
        """
        return self.current_location

    @abstractmethod
    def update_location(self, time):
        """
        Update the location of the entity.

        Parameters
        ----------
        time : int
            The current time.
        """
        pass
