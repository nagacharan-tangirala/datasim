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
        super().__init__()
        self.positions = positions

    def step(self):
        """
        Step through the model.
        """
        # Location is static, so just set the current location to the first position
        self.current_location = self.positions.iloc[0].values.tolist()

    def get_type(self) -> str:
        """
        Get the type of the model.

        Returns
        ----------
        str
            The type of the model.
        """
        return "static"

    def update_positions(self, positions: DataFrame) -> None:
        """
        Update the positions of the ue. We will skip this for the static model.

        Parameters
        ----------
        positions : DataFrame
            The positions of the ue.
        """
        pass
