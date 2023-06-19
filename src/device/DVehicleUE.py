from pandas import DataFrame

from src.device.BUE import BaseUE
from src.device.DOnetoOneData import OnetoOneData
from src.models.MUECoverageModel import CoverageModel
from src.models.MUEMobilityModel import MobilityModel


class VehicleUE(BaseUE):
    def __init__(self, ue_id: int, ue_settings: dict):
        """
        Initialize the vehicle ue.
        """
        super().__init__(ue_id, ue_settings)
        self.coverage: DataFrame | None = None

        self.neighbour_data: dict[int, float] = {}

    def set_mobility_data(self, positions: DataFrame) -> None:
        """
        Set the mobility data for the ue.
        """
        self.start_time = positions["time"].min()
        self.end_time = positions["time"].max()

        # Store x and y positions
        self.positions = positions[["x", "y"]].values.tolist()

    def set_coverage_data(self, coverage: DataFrame):
        """
        Set the coverage data for the ue.
        """
        self.coverage = coverage.reset_index(drop=True)

    def _initiate_models(self) -> None:
        """
        Initiate the models related to this ue.
        """
        # Create mobility model
        self.mobility_model = MobilityModel(self.positions)
        self.mobility_model.activate()

        # Create the coverage model
        self.coverage_model = CoverageModel(self.coverage)
        self.coverage_model.activate()

    def _deactivate_models(self) -> None:
        """
        Deactivate the models related to this ue.
        """
        # Deactivate the mobility model
        self.mobility_model.deactivate()

        # Deactivate the coverage model
        self.coverage_model.deactivate()

    def step(self) -> None:
        """
        Step function for the ue.
        """
        # Check if the ue is active
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
        neighbours = self.coverage_model.get_ues_in_coverage()

        # Clear the neighbour data
        self.neighbour_data.clear()

        # Collect the data from the ues within the coverage area
        for neighbour in neighbours:
            if neighbour is not self.unique_id and self.sim_model.ues[neighbour].get_data_transmit_status():
                self.neighbour_data[neighbour] = self.sim_model.ues[neighbour].get_cached_data()

    def get_neighbour_data(self) -> dict[int, float]:
        """
        Get the data from the neighbours.
        """
        return self.neighbour_data

    def _generate_data(self) -> None:
        """
        Generate data for the ue.
        """
        # Update the data cache
        if self.ue_data is not None:
            self.ue_data_cache.appendleft(self.ue_data)

        # Generate new data
        # TODO - find the nearest node ID.
        self.ue_data = OnetoOneData(self.sim_model.current_time, self.ue_data_rate, self.unique_id, node_id)
