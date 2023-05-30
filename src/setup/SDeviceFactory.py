from src.device.DVehicleAgent import VehicleAgent
from src.device.DRSUAgent import RSUAgent


class DeviceFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_agent(params: dict, sensors: dict):
        """
        Create an agent from the given parameters.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the agent.
        sensors : dict
            Dictionary containing all the sensors for the agent.
        model : Model
            The model to which the agent belongs.
        """
        agent_type = params.get('type', None)
        if agent_type == 'vehicle':
            return VehicleAgent(params, sensors)
        elif agent_type == 'rsu':
            return RSUAgent(params, sensors)
        else:
            raise ValueError("Agent type not supported.")
