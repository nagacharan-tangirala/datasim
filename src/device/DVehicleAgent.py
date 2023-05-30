from src.device.BAgent import AgentBase

from src.device.MSensorModel import SensorModel
from src.models.MMobilityModel import MobilityModel
from src.models.MCoverageModel import CoverageModel


class VehicleAgent(AgentBase):
    def __init__(self, params: dict, sensor_params: dict):
        """
        Initialize the vehicle agent.
        """
        super().__init__(params, sensor_params)
        self.coverage_file = params.get('coverage_file', None)

    def step(self):
        """
        Step function for the agent.
        """
        # Check if the agent is active
        if not self.active:
            return

        # Step through the mobility model
        self.mobility_model.step()

        # Collect the data from the sensors
        self.sensor_model.step()
        vehicle_data = self.sensor_model.get_collected_data_size()

        # Step through the coverage model
        self.coverage_model.step(self.sim_model.current_time)

        # Get the neighbours
        neighbors = self.coverage_model.get_agents_in_coverage()

        # Collect the data from the agents within the coverage area
        neighbor_data = 0
        for neighbor in neighbors:
            if neighbor == self.unique_id:
                continue
            neighbor_data += self.sim_model.agents[neighbor].get_cached_data()

        # Update the data collected by the agent
        self.total_data += vehicle_data + neighbor_data

    def _initiate_models(self):
        """
        Initiate the models related to this agent.
        """
        # Create sensor model
        self.sensor_model = SensorModel(self.sensor_params, self.sim_model.time_step)
        self.sensor_model.activate()

        # Create mobility model
        self.mobility_model = MobilityModel(self.positions)
        self.mobility_model.activate()

        # Create the coverage model
        self.coverage_model = CoverageModel(self.unique_id, self.coverage_file)
        self.coverage_model.activate()

    def _deactivate_models(self):
        """
        Deactivate the models related to this agent.
        """
        # Deactivate the sensor model
        self.sensor_model.deactivate()

        # Deactivate the mobility model
        self.mobility_model.deactivate()

        # Deactivate the coverage model
        self.coverage_model.deactivate()
