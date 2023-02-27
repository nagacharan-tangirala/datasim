from src.device.DStaticMobilityModel import StaticMobilityModel
from src.device.DTraceMobilityModel import TraceMobilityModel


class EntityModelFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_mobility_model(positions: dict):
        """
        Create a mobility model from the given parameters.

        Parameters
        ----------
        positions : dict
            Dictionary containing all the positions.
        """
        if len(positions) == 1:
            return StaticMobilityModel(positions)
        else:
            return TraceMobilityModel(positions)
