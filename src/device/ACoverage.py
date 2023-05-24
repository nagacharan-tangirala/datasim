import h5py

from mesa import Agent


class AgentCoverage(Agent):
    def __init__(self, agent_id, coverage_file: str):
        """
        Initialize the coverage model.
        """
        super().__init__(0, None)
        self.agent_id = agent_id

        # Open the coverage file
        self.coverage_file = h5py.File(coverage_file, 'r')

        # Open the agent id group
        self.agent_group = self.coverage_file['agents'][str(self.agent_id)]

        self.current_time = None
        self.coverage = None

    def step(self):
        """
        Step through the model, should be implemented by the child class.
        """
        # Check if the current time is in the coverage file
        if str(self.current_time) in self.agent_group:
            # Open the coverage for the current time step
            coverage_group = self.agent_group[str(self.current_time)]

            # Get the coverage dataset
            self.coverage = coverage_group['coverage'][:]
        else:
            # Set the coverage to None
            self.coverage = None

    def get_agents_in_coverage(self) -> list[int]:
        """
        Get the neighbors of the agent.

        Returns
        ----------
        list
            The neighbors of the agent.
        """
        # Check if the coverage is None
        if self.coverage is None or len(self.coverage) == 0:
            return []

        # Get the agents in the coverage
        return self.coverage.tolist()
