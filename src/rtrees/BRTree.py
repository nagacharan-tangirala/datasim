import geopandas as gpd
from geopandas import GeoSeries


class BRTree:
    def __init__(self, positions):
        """
        Initialize the RTree with the given positions. The positions are stored in a GeoPandas GeoSeries.

        Parameters
        ----------
        positions : list
            List of positions.
        """
        self.positions = GeoSeries(positions)
        self.tree = self.positions.sindex

