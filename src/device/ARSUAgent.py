from mesa import Model
from src.device.AAgent import AgentBase


class RSUAgent(AgentBase):
    def __init__(self, params: dict, sensors: dict):
        """
        Initialize the RSU agent.
        """
        super().__init__(params, sensors)

    def step(self):
        pass
