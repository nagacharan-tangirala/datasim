import logging

from mesa import Agent
from numpy import array, empty, ndarray
from pandas import DataFrame

import src.core.common_constants as cc

__all__ = ["NearestNBaseStationFinder", "TraceVehicleNeighbourFinder"]

logger = logging.getLogger(__name__)


class NearestNBaseStationFinder(Agent):
    def __init__(self, v2b_links_df: DataFrame):
        """
        Initialize the nearest base station look up model.
        """
        super().__init__(0, None)
        self._v2b_links_df: DataFrame = v2b_links_df

        self._v2b_links_data: dict = {}
        self._base_station_distances: dict = {}

        self._filtered_v2b_links_data: dict = {}
        self._filtered_base_station_distances: dict = {}
        self.current_time: int = -1

        self._create_v2b_links_data()

    def _create_v2b_links_data(self) -> None:
        """
        Create the v2b links data.
        """
        # Convert the v2b links df to dictionary
        self._v2b_links_data = (
            self._v2b_links_df.groupby(cc.TIME_STEP)
            .apply(lambda x: dict(zip(x[cc.VEHICLE_ID], x[cc.BASE_STATIONS])))
            .to_dict()
        )

        self._base_station_distances = (
            self._v2b_links_df.groupby(cc.TIME_STEP)
            .apply(lambda x: dict(zip(x[cc.VEHICLE_ID], x[cc.DISTANCES])))
            .to_dict()
        )

        del self._v2b_links_df

    def update_base_station_links(self, v2b_links_df: DataFrame) -> None:
        """
        Update the base station links.
        """
        self._v2b_links_df = v2b_links_df
        self._create_v2b_links_data()

    def step(self) -> None:
        """
        Step through the base station finder.
        """
        self._filtered_v2b_links_data.clear()
        if self.current_time not in self._v2b_links_data:
            return

        self._filtered_v2b_links_data = self._v2b_links_data[self.current_time]
        self._filtered_base_station_distances = self._base_station_distances[
            self.current_time
        ]

    def select_n_stations_for_vehicle(self, vehicle_id: int, n: int) -> ndarray[int]:
        """
        Select base stations for the vehicle.
        """
        logger.debug(f"Looking up base stations for vehicle {vehicle_id}")

        if len(self._filtered_v2b_links_data) == 0:
            return empty(0, dtype=int)

        # Get the base stations for the vehicle.
        base_stations: str = self._filtered_v2b_links_data[vehicle_id]

        # Split the base stations string into a numpy array of integers.
        base_stations: ndarray[int] = array(base_stations.split(" ")).astype(int)

        # Return the n nearest base stations.
        if len(base_stations) < n:
            return base_stations
        return base_stations[:n]


class TraceVehicleNeighbourFinder(Agent):
    def __init__(self, v2v_links_df: DataFrame):
        """
        Initialize the vehicle neighbour finder.
        """
        super().__init__(0, None)
        self._v2v_links_df: DataFrame = v2v_links_df

        self._v2v_links_data: dict = {}
        self._neighbour_distances: dict = {}

        self._filtered_v2v_links_data: dict = {}
        self._filtered_neighbour_distances: dict = {}
        self.current_time: int = -1

        self._create_v2v_links_data()

    def _create_v2v_links_data(self) -> None:
        """
        Create the v2b links data.
        """
        # Convert the v2b links df to dictionary
        self._v2v_links_data = (
            self._v2v_links_df.groupby(cc.TIME_STEP)
            .apply(lambda x: dict(zip(x[cc.VEHICLE_ID], x[cc.NEIGHBOURS])))
            .to_dict()
        )

        self._neighbour_distances = (
            self._v2v_links_df.groupby(cc.TIME_STEP)
            .apply(lambda x: dict(zip(x[cc.VEHICLE_ID], x[cc.DISTANCES])))
            .to_dict()
        )

        del self._v2v_links_df

    def update_base_station_links(self, v2v_links: DataFrame) -> None:
        """
        Update the vehicle neighbour links.
        """
        self._v2v_links_df = v2v_links
        self._create_v2v_links_data()

    def step(self) -> None:
        """
        Step through the neighbour finder.
        """
        self._filtered_v2v_links_data.clear()
        if self.current_time not in self._v2v_links_data:
            return

        self._filtered_v2v_links_data = self._v2v_links_data[self.current_time]
        self._filtered_neighbour_distances = self._neighbour_distances[
            self.current_time
        ]

    def find_vehicles(self, vehicle_id: int) -> ndarray[int]:
        """
        Find vehicles that are neighbour for the given vehicle.
        """
        logger.debug(f"Looking up neighbours for vehicle {vehicle_id}")

        if len(self._filtered_v2v_links_data) == 0:
            return empty(0, dtype=int)

        if vehicle_id not in self._filtered_v2v_links_data:
            return empty(0, dtype=int)

        # Get the neighbours for the vehicle.
        neighbours: str = self._filtered_v2v_links_data[vehicle_id]

        # Split the neighbours string into a numpy array of integers.
        neighbours: ndarray[int] = array(neighbours.split(" ")).astype(int)

        return neighbours
