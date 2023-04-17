from mesa import Model
from src.device.BAgent import BAgent


class VehicleAgent(BAgent):
    def __init__(self, params: dict, sensors: dict):
        """
        Initialize the vehicle agent.
        """
        super().__init__(params, sensors)

