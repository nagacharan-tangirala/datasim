from pandas import DataFrame

from src.ue_models.BUEMobility import UEMobilityBase


class StaticUEMobility(UEMobilityBase):
    def __init__(self, positions: DataFrame):
        """
        Initialize the static mobility model.

        Parameters
        ----------
        positions : DataFrame
            DataFrame of positions for the ue.
        """
        super().__init__(positions)
        self._type = 'static'

    def step(self):
        """
        Step through the model.
        """
        # Location is static, so just set the current location to the first position
        self._current_location = self._positions.iloc[0].values.tolist()

    def update_positions(self, positions: DataFrame) -> None:
        """
        Update the positions of the ue. We will skip this for the static model.

        Parameters
        ----------
        positions : DataFrame
            The positions of the ue.
        """
        self._positions = positions
