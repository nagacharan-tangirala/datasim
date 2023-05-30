from src.models.BMobility import AgentMobility


class StaticMobility(AgentMobility):
    def __init__(self, positions: dict):
        """
        Initialize the static mobility model.

        Parameters
        ----------
        positions : dict
            Dictionary of positions for the agent with the time as key.
        """
        super().__init__(positions)

    def step(self):
        """
        Step through the model.
        """
        # Location is static, so just set the current location to the first position
        self.current_location = self.positions[self.index]
