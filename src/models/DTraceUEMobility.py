from src.models.BUEMobility import UEMobility


class TraceMobility(UEMobility):
    def __init__(self, positions: dict):
        """
        Initialize the trace mobility model.

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
        self.current_location = self.positions[self.index]
        self.index = self.index + 1
