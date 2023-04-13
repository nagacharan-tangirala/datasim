import geopandas as gpd
from geopandas import GeoSeries


class GeoIndex:
    def __init__(self, positions):
        """
        Initialize the coverage index with the given positions.

        Parameters
        ----------
        positions : list
            List of positions.
        """
        # Convert positions to points and create the coverage index
        self.positions = GeoSeries([gpd.points_from_xy([p[0]], [p[1]])[0] for p in positions])
        self.tree = self.positions.sindex

    def get_nearest(self, position):
        """
        Get the nearest position to the given position.

        Parameters
        ----------
        position : tuple
            The position.

        Returns
        ----------
        tuple
            The nearest position.
        """
        return self.positions.iloc[self.tree.nearest(position)]
