from src.device.AAgentMobility import AgentMobility


class TraceMobility(AgentMobility):
    def __init__(self, positions: dict):
        """
        Initialize the trace mobility model.

        Parameters
        ----------
        positions : dict
            Dictionary of positions for the entity with the time as key.
        """
        super().__init__(positions)

    def step(self):
        """
        Step through the model.
        """
        self.current_location = self.positions[self.index]
        self.index = self.index + 1
