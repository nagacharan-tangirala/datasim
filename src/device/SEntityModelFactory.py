from src.device.DStaticMobilityModel import StaticMobilityModel
from src.device.DTraceMobilityModel import TraceMobilityModel


class EntityModelFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_mobility_model(positions: dict, start_time: int):
        """
        Create a mobility model from the given parameters.

        Parameters
        ----------
        positions : dict
            Dictionary containing all the positions.
        start_time : int
            The start time of the entity.
        """
        if len(positions) == 1:
            return StaticMobilityModel(positions, start_time)
        else:
            return TraceMobilityModel(positions, start_time)
