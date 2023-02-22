from src.device.BEntityMobilityModel import MobilityModelBase


class TraceMobilityModel(MobilityModelBase):
    def __init__(self, positions: dict):
        """
        Initialize the trace mobility model.

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
        # Update the location of the entity if there is a position for the current time. Otherwise, keep the current location.
        if time in self.positions:
            self.current_location = self.positions.get(time)
