import pandas as pd

from src.models.BCoverage import AgentCoverage


class AgentTraceCoverage(AgentCoverage):
    def __init__(self, coverage_data: pd.DataFrame):
        """
        Initialize the trace coverage model.
        """
        super().__init__()
        self.coverage_data = coverage_data

    def step(self):
        """
        Step through the model.
        """
        # Check if the coverage data is empty
        if self.coverage_data is None or len(self.coverage_data) == 0:
            self.coverage_data = []

        # Get the agents in the coverage
        self.coverage_data = self.coverage_data[self.coverage_data["time"] == self.current_time].tolist()
