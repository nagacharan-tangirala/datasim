from src.models.BCoverage import AgentCoverage


class AgentCoverageFactory:
    def __init__(self):
        """
        Initialize the coverage factory.
        """
        pass

    @staticmethod
    def create_coverage(agent_id, coverage_file: str = None):
        """
        Creates a coverage model.
        """
        if coverage_file is None:
            return None
        return AgentCoverage(agent_id, coverage_file)
