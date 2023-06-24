from pandas import DataFrame

from src.models.BUEMobility import UEMobility


class TraceUEMobility(UEMobility):
    def __init__(self):
        """
        Initialize the trace mobility model.
        """
        super().__init__()

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

    def get_type(self) -> str:
        """
        Get the type of the model.

        Returns
        ----------
        str
            The type of the model.
        """
        return "trace"

    def update_positions(self, positions: DataFrame) -> None:
        """
        Update the positions of the ue.

        Parameters
        ----------
        positions : DataFrame
            The positions of the ue.
        """
        self.positions = positions
