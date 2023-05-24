from src.device.AStaticMobility import StaticMobility
from src.device.ATraceMobility import TraceMobility


class AgentMobilityFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_mobility(positions: dict):
        """
        Create a mobility model from the given parameters.

        Parameters
        ----------
        positions : dict
            Dictionary containing all the positions.
        """
        if len(positions) == 1:
            return StaticMobility(positions)
        else:
            return TraceMobility(positions)

    @staticmethod
    def create_neighbor_model():
        """
        Create a neighbor model from the given parameters.
        """
        return
