from abc import abstractmethod

from mesa import Agent, Model


class AgentCoverage(Agent):
    def __init__(self):
        """
        Initialize the coverage model.
        """
        super().__init__(0, None)

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
        self.index = 0
        self.model.schedule.add(self)