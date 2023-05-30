from mesa import Model
from src.device.BAgent import AgentBase


class RSUAgent(AgentBase):
    def _initiate_models(self):
        pass

    def _deactivate_models(self):
        pass

    def __init__(self, params: dict, sensors: dict):
        """
        Initialize the RSU agent.
        """
        super().__init__(params, sensors)

    def step(self):
        pass
