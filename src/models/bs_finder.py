from mesa import Agent
from pandas import DataFrame

import src.core.common_constants as cc


class NearestNBaseStationFinder(Agent):
    def __init__(self, base_stations: dict, tower_links_df: DataFrame):
        """
        Initialize the nearest tower look up model.
        """
        super().__init__(0, None)
        self._base_stations: dict = base_stations
        self._base_station_links_df: DataFrame = tower_links_df

        self._filtered_base_station_links_df: DataFrame = DataFrame()

        self._current_time: int = -1

    @property
    def current_time(self) -> int:
        """Get the current time."""
        return self._current_time

    @current_time.setter
    def current_time(self, value: int) -> None:
        """Set the current time."""
        self._current_time = value

    def step(self) -> None:
        """
        Step through the tower finder.
        """
        # Filter the tower links df to only include the current time step
        self._filtered_base_station_links_df = self._base_station_links_df[
            self._base_station_links_df[cc.TIME_STEP] == self._current_time
        ]

    def select_n_base_stations_for_vehicle(self, vehicle_id: int, n: int) -> list[int]:
        """
        Select base stations for the vehicle.
        """
        # Get the base stations for the vehicle.
        vehicle_base_stations = self._filtered_base_station_links_df[
            self._filtered_base_station_links_df[cc.VEHICLE_ID] == vehicle_id
        ]

        # Create a dictionary of base stations and their distances from the vehicle base stations df.
        tower_distances = {
            tower_id: distance
            for tower_id, distance in zip(
                [int(x) for x in vehicle_base_stations[cc.BASE_STATIONS]],
                [float(x) for x in vehicle_base_stations[cc.DISTANCES]],
            )
        }

        # Sort the tower distances dictionary by distance.
        sorted_tower_distances = {
            tower_id: distance
            for tower_id, distance in sorted(
                tower_distances.items(), key=lambda item: item[1]
            )
        }

        # Return the n nearest base stations.
        if len(sorted_tower_distances) < n:
            return list(sorted_tower_distances.keys())
        return list(sorted_tower_distances.keys())[:n]
