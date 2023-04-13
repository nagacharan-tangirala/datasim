from src.device.BEntityMobilityModel import MobilityModelBase


class TraceMobilityModel(MobilityModelBase):
    def __init__(self, positions: dict, start_time: int):
        """
        Initialize the trace mobility model.

        Parameters
        ----------
        positions : dict
            Dictionary of positions for the entity with the time as key.
        """
        super().__init__(positions, start_time)

    def update_location(self, time):
        """
        Update the location of the entity.

        Parameters
        ----------
        time : int
            The current time.
        """
        # Convert time to index
        index = time - self.start_time

        # Check if the index is less than the length of the positions
        if index < len(self.positions):
            self.current_location = self.positions[index]
