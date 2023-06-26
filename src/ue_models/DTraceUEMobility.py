from pandas import DataFrame, concat

from src.ue_models.BUEMobility import UEMobilityBase


class TraceUEMobility(UEMobilityBase):
    def __init__(self, positions: DataFrame):
        """
        Initialize the trace mobility model.
        """
        super().__init__(positions)
        self._type = 'trace'

    def get_start_and_end_time(self) -> tuple[int, int]:
        """
        Get the start and end time of the ue.

        Returns
        ----------
        tuple[int, int]
            The start and end time of the ue.
        """
        return self._positions["time"].min(), self._positions["time"].max()

    def update_positions(self, positions: DataFrame) -> None:
        """
        Update the positions of the ue.

        Parameters
        ----------
        positions : DataFrame
            The positions of the ue.
        """
        self._positions = concat([self._positions, positions], ignore_index=True)

    def step(self):
        """
        Step through the model.
        """
        # Check if the current time is in the positions dataframe
        if self.current_time in self._positions["time"].values:
            self._current_location = self._positions[self._positions["time"] == self.current_time].iloc[0].values[1:]
        else:
            # If not, then the ue is not moving
            self._current_location = self._current_location
