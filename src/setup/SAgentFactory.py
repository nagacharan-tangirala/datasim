from src.device.DVehicleAgent import VehicleAgent


class AgentFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_agent(agent_id: int) -> VehicleAgent:
        """
        Create an agent from the given parameters.

        Parameters
        ----------
        agent_id : int
            The ID of the agent.
        """
        return VehicleAgent(agent_id)
