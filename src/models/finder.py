from mesa import Agent
from pandas import DataFrame

import src.core.common_constants as cc

__all__ = ["NearestNBaseStationFinder", "TraceVehicleNeighbourFinder"]


class NearestNBaseStationFinder(Agent):
    def __init__(self, tower_links_df: DataFrame):
        """
        Initialize the nearest tower look up model.
        """
        super().__init__(0, None)
        self._base_station_links_df: DataFrame = tower_links_df

        self._filtered_base_station_links_df: DataFrame = DataFrame()
        self.current_time: int = -1

    def step(self) -> None:
        """
        Step through the tower finder.
        """
        # Filter the tower links df to only include the current time step
        self._filtered_base_station_links_df = self._base_station_links_df[
            self._base_station_links_df[cc.TIME_STEP] == self.current_time
        ]

    def update_base_station_links(self, tower_links_df: DataFrame) -> None:
        """
        Update the base station links.
        """
        self._base_station_links_df = tower_links_df

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
                [
                    int(x)
                    for x in vehicle_base_stations[cc.BASE_STATIONS].iloc[0].split(" ")
                ],
                [
                    float(x)
                    for x in vehicle_base_stations[cc.DISTANCES].iloc[0].split(" ")
                ],
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


class TraceVehicleNeighbourFinder(Agent):
    def __init__(self, v2v_links_df: DataFrame):
        """
        Initialize the vehicle neighbour finder.
        """
        super().__init__(0, None)
        self._v2v_links_df: DataFrame = v2v_links_df

        self._filtered_v2v_links_df: DataFrame = DataFrame()
        self.current_time: int = -1

    def step(self) -> None:
        """
        Step through the neighbour finder.
        """
        # Filter the tower links df to only include the current time step
        self._filtered_v2v_links_df = self._v2v_links_df[
            self._v2v_links_df[cc.TIME_STEP] == self.current_time
        ]

    def update_base_station_links(self, v2v_links: DataFrame) -> None:
        """
        Update the base station links.
        """
        self._v2v_links_df = v2v_links

    def find_vehicles(self, vehicle_id: int) -> list[int]:
        """
        Find vehicles that are neighbour for the given vehicle.
        """
        # It is possible that there are no v2v links for the current time step.
        if self._filtered_v2v_links_df.empty:
            return []

        # Get the neighbours for the vehicle.
        neighbour_vehicles = self._filtered_v2v_links_df[
            self._filtered_v2v_links_df[cc.VEHICLE_ID] == vehicle_id
        ]

        # If there are no neighbours, return an empty list.
        if neighbour_vehicles.empty:
            return []

        # Create a dictionary of vehicles and their distances from the selected vehicle.
        neighbour_distances = {
            veh_id: distance
            for veh_id, distance in zip(
                [int(x) for x in neighbour_vehicles[cc.BASE_STATIONS]],
                [float(x) for x in neighbour_vehicles[cc.DISTANCES]],
            )
        }

        # Sort the vehicle distances dictionary by distance.
        sorted_tower_distances = {
            veh_id: distance
            for veh_id, distance in sorted(
                neighbour_distances.items(), key=lambda item: item[1]
            )
        }

        # Return all the neighbours.
        return list(sorted_tower_distances.keys())
