from pandas import DataFrame

from src.models.BUEMobility import UEMobility


class StaticUEMobility(UEMobility):
    def __init__(self, positions: DataFrame):
        """
        Initialize the static mobility model.

        Parameters
        ----------
        positions : DataFrame
            DataFrame of positions for the ue.
        """
        super().__init__(positions)

    def step(self):
        """
        Step through the model.
        """
        # Location is static, so just set the current location to the first position
        self.current_location = self.positions.iloc[0].values.tolist()
