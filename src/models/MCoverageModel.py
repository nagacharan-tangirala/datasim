import pandas as pd
from mesa import Model
from mesa.time import BaseScheduler

from src.setup.SDeviceModelFactory import DeviceModelFactory
from src.models.BCoverage import AgentCoverage


class CoverageModel(Model):
    def __init__(self, agent_id, coverage_data: pd.DataFrame):
        """
        Initialize the coverage model to update the nodes and agents that are in each other's coverage.
        """
        super().__init__()
        self.agent_id = agent_id
        self.coverage_data = coverage_data

        self.schedule: BaseScheduler = BaseScheduler(self)
        self.coverage: AgentCoverage | None = None

    def activate(self) -> None:
        """
        Activate the model.
        """
        # Create coverage factory and the coverage model
        model_factory = DeviceModelFactory()
        self.coverage = model_factory.create_coverage(self.agent_id, self.coverage_data)

        # Add the coverage model to the schedule
        if self.coverage is not None:
            self.schedule.add(self.coverage)

    def deactivate(self) -> None:
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
        self.coverage.set_current_time(current_time)

        # Step through the coverage model
        self.schedule.step()

    def get_agents_in_coverage(self) -> list[int]:
        """
        Get the neighbors of the agent.
        """
        if self.coverage is None:
            return []
        return self.coverage.get_agents_in_coverage()
