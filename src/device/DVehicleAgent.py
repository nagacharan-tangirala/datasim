import pandas as pd

from src.device.BAgent import AgentBase
from src.models.MCoverageModel import CoverageModel
from src.models.MMobilityModel import MobilityModel


class VehicleAgent(AgentBase):
    def __init__(self, agent_id: int):
        """
        Initialize the vehicle agent.
        """
        super().__init__(agent_id)
        self.coverage: pd.DataFrame | None = None

        self.neighbour_data: dict[int, float] = {}

    def set_mobility_data(self, positions: pd.DataFrame) -> None:
        """
        Set the mobility data for the agent.
        """
        self.start_time = positions["time"].min()
        self.end_time = positions["time"].max()

        # Store x and y positions
        self.positions = positions[["x", "y"]].values.tolist()

    def set_coverage_data(self, coverage: pd.DataFrame):
        """
        Set the coverage data for the agent.
        """
        self.coverage = coverage.reset_index(drop=True)

    def _initiate_models(self) -> None:
        """
        Initiate the models related to this agent.
        """
        # Create mobility model
        self.mobility_model = MobilityModel(self.positions)
        self.mobility_model.activate()

        # Create the coverage model
        self.coverage_model = CoverageModel(self.coverage)
        self.coverage_model.activate()

    def _deactivate_models(self) -> None:
        """
        Deactivate the models related to this agent.
        """
        # Deactivate the mobility model
        self.mobility_model.deactivate()

        # Deactivate the coverage model
        self.coverage_model.deactivate()

    def step(self) -> None:
        """
        Step function for the agent.
        """
        # Check if the agent is active
        if not self.active:
            return

        # Update the current position
        self.current_position = self.mobility_model.get_location()

        # Step through the mobility model and coverage model.
        self.mobility_model.step()
        self.coverage_model.step(self.sim_model.current_time)

        self._generate_data()
        self._collect_neighbours_data()

    def _collect_neighbours_data(self) -> None:
        """
        Collect data from the neighbors.
        """
        # Get the neighbours
        neighbours = self.coverage_model.get_agents_in_coverage()

        # Clear the neighbour data
        self.neighbour_data.clear()

        # Collect the data from the agents within the coverage area
        for neighbour in neighbours:
            if neighbour is not self.unique_id and self.sim_model.agents[neighbour].get_data_transmit_status():
                self.neighbour_data[neighbour] = self.sim_model.agents[neighbour].get_cached_data()

    def get_neighbour_data(self) -> dict[int, float]:
        """
        Get the data from the neighbours.
        """
        return self.neighbour_data

    def _generate_data(self) -> None:
        """
        Generate data for the agent.
        """
        #
        self.agent_data_cache.appendleft(self.agent_data)

        # Generate new data
        self.agent_data = 2.0
