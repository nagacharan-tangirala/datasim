from pandas import DataFrame

from src.models.BUEMobility import UEMobility


class TraceMobility(UEMobility):
    def __init__(self, positions: DataFrame):
        """
        Initialize the trace mobility model.

        Parameters
        ----------
        positions : DataFrame
            Dataframe of positions for the ue.
        """
        super().__init__(positions)

    def step(self):
        """
        Step through the model.
        """
        # Check if the current time is in the positions dataframe
        if self.current_time in self.positions["time"].values:
            self.current_location = self.positions[self.positions["time"] == self.current_time].iloc[0].values[1:]
        else:
            # If not, then the ue is not moving
            self.current_location = self.current_location
