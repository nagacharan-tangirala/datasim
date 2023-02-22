from src.device.BEntityMobilityModel import MobilityModelBase


class StaticMobilityModel(MobilityModelBase):
    def __init__(self, positions: dict):
        """
        Initialize the static mobility model.

        Parameters
        ----------
        positions : dict
            Dictionary of positions for the entity with the time as key.
        """
        super().__init__(positions)
        self.current_location = positions.get(0)

    def update_location(self, time):
        """
        Update the location of the entity.

        Parameters
        ----------
        time : int
            The current time.
        """
        # Location is static, no need to update
        pass
