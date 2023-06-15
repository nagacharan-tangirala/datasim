from abc import abstractmethod

from mesa import Agent


class UEMobility(Agent):
    def __init__(self, positions):
        """
        Initialize the mobility model.
        """
        super().__init__(0, None)
        self.positions = positions
        self.index = 0
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

    def activate(self):
        """
        Activate the mobility model.
        """
        self.model.schedule.add(self)
