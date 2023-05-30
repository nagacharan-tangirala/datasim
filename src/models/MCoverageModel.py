from mesa import Model
from mesa.time import BaseScheduler

from src.models.SCoverageFactory import AgentCoverageFactory


class CoverageModel(Model):
    def __init__(self, agent_id, coverage_file: str = None):
        """
        Initialize the coverage model to update the nodes and agents that are in each other's coverage.
        """
        super().__init__()
        self.agent_id = agent_id
        self.coverage_file = coverage_file

        self.coverage = None

    def activate(self):
        """
        Activate the model.
        """
        # Override the scheduler
        self.schedule = BaseScheduler(self)

        # Create mobility factory and the mobility model
        coverage_factory = AgentCoverageFactory()
        self.coverage = coverage_factory.create_coverage(self.agent_id, self.coverage_file)

        # Add the mobility model to the schedule
        if self.coverage is not None:
            self.schedule.add(self.coverage)

    def deactivate(self):
        """
        Deactivate the model by removing the coverage model from the schedule.
        """
        if len(self.schedule.agents) == 0:
            return
        self.schedule.remove(self.coverage)

    def step(self, *args, **kwargs):
        """
        Update the coverage of the nodes and agents.
        """
        # Check if the coverage model is active
        if len(self.schedule.agents) == 0:
            return

        # Get the time step from args
        current_time = int(args[0])
        self.coverage.current_time = current_time

        self.schedule.step()

    def get_agents_in_coverage(self) -> list[int]:
        """
        Get the neighbors of the agent.
        """
        if self.coverage is None:
            return []
        return self.coverage.get_agents_in_coverage()

