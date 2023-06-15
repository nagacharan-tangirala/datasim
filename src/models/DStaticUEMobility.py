from src.models.BUEMobility import UEMobility


class StaticUEMobility(UEMobility):
    def __init__(self, positions: dict):
        """
        Initialize the static mobility model.

        Parameters
        ----------
        positions : dict
            Dictionary of positions for the ue with the time as key.
        """
        super().__init__(positions)

    def step(self):
        """
        Step through the model.
        """
        # Location is static, so just set the current location to the first position
        self.current_location = self.positions[self.index]
