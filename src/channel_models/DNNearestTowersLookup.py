from pandas import DataFrame

from src.channel_models.BTowerLookup import TowerLookupBase


class NNearestTowerLookup(TowerLookupBase):
    def __init__(self, cell_towers: dict, tower_links_df: DataFrame):
        """
        Initialize the nearest tower look up model.
        """
        super().__init__(cell_towers, tower_links_df)

    def select_n_towers_for_ue(self, ue_id: int, n: int) -> list[int]:
        """
        Select towers for the ue.
        """
        # Get the towers for the ue.
        ue_towers = self._current_ts_tower_links_df[self._current_ts_tower_links_df['ue_id'] == ue_id]

        # Create a dictionary of towers and their distances from the ue towers df.
        tower_distances = {tower_id: distance for tower_id, distance in zip(ue_towers['nearest_towers'], ue_towers['tower_distances'])}

        # Sort the tower distances dictionary by distance.
        sorted_tower_distances = {tower_id: distance for tower_id, distance in sorted(tower_distances.items(), key=lambda item: item[1])}

        # Return the n nearest towers.
        if len(sorted_tower_distances) < n:
            return list(sorted_tower_distances.keys())
        return list(sorted_tower_distances.keys())[:n]

    def step(self) -> None:
        """
        Step through the tower look up model.
        """
        # Filter the tower links df to only include the current time step
        self._current_ts_tower_links_df = self._tower_links_df[self._tower_links_df['time'] == self._current_time]
