import pandas as pd

from src.models.BCoverage import AgentCoverage


class AgentCoverageFactory:
    def __init__(self):
        """
        Initialize the coverage factory.
        """
        pass

    @staticmethod
    def create_coverage(agent_id, coverage_data: pd.DataFrame):
        """
        Creates a coverage model.
        """
        return AgentCoverage(agent_id, coverage_data)
