from abc import abstractmethod

from mesa import Agent


class AgentCoverage(Agent):
    def __init__(self):
        """
        Initialize the coverage model.
        """
        super().__init__(0, None)

        self.current_time: int = 0
        self.agents_in_coverage = []

    def set_current_time(self, current_time: int) -> None:
        """
        Set the current time for the coverage model.

        Parameters
        ----------
        current_time : int
            The current time.
        """
        self.current_time = current_time

    def get_agents_in_coverage(self) -> list[int]:
        """
        Get the neighbors of the agent.
        """
        return self.agents_in_coverage

    @abstractmethod
    def step(self):
        """
        Step through the model, should be implemented by the child class.
        """
        pass
