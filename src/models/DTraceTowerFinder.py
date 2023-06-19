from pandas import DataFrame

from src.models.BTowerFinder import TowerFinderBase


class TraceTowerFinder(TowerFinderBase):
    def __init__(self, nearest_towers_df: DataFrame):
        """
        Initialize the tower finder.
        """
        super().__init__()

        self.nearest_towers_df: DataFrame = nearest_towers_df

    def step(self) -> None:
        """
        Execute the step.
        """
        # Get the towers that are in range in the current time
        towers_in_range = self.nearest_towers_df[self.nearest_towers_df["time"] == self.current_time]

        # Select the closest tower
        # TODO - More advanced selection method (e.g. based on signal strength) can be implemented here.
        self.nearest_tower = towers_in_range["tower_id"].iloc[0]
