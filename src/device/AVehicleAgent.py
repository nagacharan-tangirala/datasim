from src.device.AAgent import AgentBase

from src.sensor.MSensor import SensorModel
from src.device.MMobility import MobilityModel


class VehicleAgent(AgentBase):
    def __init__(self, params: dict, sensor_params: dict):
        """
        Initialize the vehicle agent.
        """
        super().__init__(params, sensor_params)

    def step(self):
        """
        Step function for the agent.
        """
        # Check if the agent is active
        if not self.active:
            return

        # Step through the models
        self.sensor_model.step()
        self.mobility_model.step()

        # Update the data collected by the sensors
        self.total_data = self.sensor_model.get_collected_data_size()

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
        self.coverage_model = CoverageModel(self.positions)
        self.coverage_model.activate()

    def _deactivate_models(self):
        """
        Deactivate the models related to this agent.
        """
        # Deactivate the sensor model
        self.sensor_model.deactivate()

        # Deactivate the mobility model
        self.mobility_model.deactivate()
