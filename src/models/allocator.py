import logging
import random

from core.constants import ModelParam, ModelType
from core.exceptions import InvalidStrategyError
from mesa import Agent
from numpy import array, empty, ndarray
from pandas import DataFrame

from src.core.common_constants import Column, DeviceId, TraceTimes

logger = logging.getLogger(__name__)


def _validate_strategy(strategy: str) -> None:
    """
    Validate the strategy for allocators.

    Parameters
    ----------
    strategy : str
        The strategy to validate.
    """
    valid_strategies = [ModelType.RANDOM, ModelType.NEAREST]
    if strategy not in valid_strategies:
        raise InvalidStrategyError(strategy, valid_strategies)


class V2BAllocator(Agent):
    def __init__(self, v2b_links_df: DataFrame, strategy_data: dict):
        """
        Initialize the v2b allocator.
        """
        super().__init__(0, None)
        self._v2b_links_df: DataFrame = v2b_links_df

        self._v2b_links_data: dict = {}
        self._base_station_distances: dict = {}

        self._filtered_v2b_links_data: dict = {}
        self.current_time: int = -1

        self._strategy_name: str = strategy_data[ModelParam.MODEL_NAME]
        _validate_strategy(self._strategy_name)

        self._create_v2b_links_data()

    def _create_v2b_links_data(self) -> None:
        """
        Create the v2b links data.
        """
        # Convert the v2b links df to dictionary
        self._v2b_links_data = (
            self._v2b_links_df.groupby(TraceTimes.TIME_STEP)
            .apply(
                lambda row: dict(
                    zip(
                        row[DeviceId.VEHICLE],
                        zip(
                            row[Column.BASE_STATIONS_STR],
                            row[Column.DISTANCES_STR],
                        ),
                    )
                )
            )
            .to_dict()
        )

        del self._v2b_links_df

    def update_v2b_links(self, v2b_links_df: DataFrame) -> None:
        """
        Update the base station links.
        """
        self._v2b_links_df = v2b_links_df
        self._create_v2b_links_data()

    def step(self) -> None:
        """
        Step through the v2b allocator.
        """
        self._filtered_v2b_links_data.clear()
        if self.current_time not in self._v2b_links_data:
            return

        self._filtered_v2b_links_data = self._v2b_links_data[self.current_time]

    def get_basestation_for_vehicle(self, vehicle_id: int) -> ndarray[int]:
        """
        Select base station for the vehicle.
        """
        logger.debug(f"Looking up base stations for vehicle {vehicle_id}")

        if len(self._filtered_v2b_links_data) == 0:
            return empty(0, dtype=int)

        base_stations: str = self._filtered_v2b_links_data[vehicle_id][0]
        base_stations: ndarray[int] = array(base_stations.split(" ")).astype(int)

        match self._strategy_name:
            case ModelType.NEAREST:
                return base_stations[0]
            case ModelType.RANDOM:
                return base_stations[random.randint(0, len(base_stations) - 1)]


class V2VAllocator(Agent):
    def __init__(self, v2v_links_df: DataFrame, strategy_data: dict):
        """
        Initialize the v2v allocator.

        Parameters
        ----------
        v2v_links_df : DataFrame
            The v2v links dataframe.
        strategy_data : dict
            The parameters related to the strategy.
        """
        super().__init__(0, None)
        self._v2v_links_df: DataFrame = v2v_links_df

        self._v2v_links_data: dict = {}
        self._neighbour_distances: dict = {}

        self._filtered_v2v_links_data: dict = {}
        self._filtered_neighbour_distances: dict = {}
        self.current_time: int = -1

        self._strategy_name: str = strategy_data[ModelParam.MODEL_NAME]
        self._vehicle_count: int = strategy_data[ModelParam.VEHICLE_COUNT]
        _validate_strategy(self._strategy_name)

        self._create_v2v_links_data()

    def _create_v2v_links_data(self) -> None:
        """
        Create the v2b links data.
        """
        # Convert the v2v links df to dictionary
        self._v2v_links_data = (
            self._v2v_links_df.groupby(TraceTimes.TIME_STEP)
            .apply(
                lambda row: dict(
                    zip(
                        row[DeviceId.VEHICLE],
                        zip(row[Column.VEHICLES_STR], row[Column.DISTANCES_STR]),
                    )
                )
            )
            .to_dict()
        )

        del self._v2v_links_df

    def update_v2v_links(self, v2v_links: DataFrame) -> None:
        """
        Update the vehicle neighbour links.
        """
        self._v2v_links_df = v2v_links
        self._create_v2v_links_data()

    def step(self) -> None:
        """
        Step through the v2v allocator.
        """
        self._filtered_v2v_links_data.clear()
        if self.current_time not in self._v2v_links_data:
            return

        self._filtered_v2v_links_data = self._v2v_links_data[self.current_time]

    def get_neighbours_for_vehicle(self, vehicle_id: int) -> ndarray[int]:
        """
        Find vehicles that are neighbours for the given vehicle.
        """
        logger.debug(f"Looking up neighbours for vehicle {vehicle_id}")

        if len(self._filtered_v2v_links_data) == 0:
            return empty(0, dtype=int)

        if vehicle_id not in self._filtered_v2v_links_data:
            return empty(0, dtype=int)

        neighbours_str: str = self._filtered_v2v_links_data[vehicle_id][0]
        v2v_vehicles: ndarray[int] = array(neighbours_str.split(" ")).astype(int)

        match self._strategy_name:
            case ModelType.NEAREST:
                if self._vehicle_count == 0:
                    return empty(0, dtype=int)
                return v2v_vehicles[: self._vehicle_count]

            case ModelType.RANDOM:
                if self._vehicle_count == 0:
                    return empty(0, dtype=int)
                return v2v_vehicles[
                    random.sample(range(len(v2v_vehicles)), self._vehicle_count)
                ]


class V2RAllocator(Agent):
    def __init__(self, v2r_links_df: DataFrame, strategy_data: dict):
        """
        Initialize the v2r allocator.
        """
        super().__init__(0, None)
        self._v2r_links_df: DataFrame = v2r_links_df

        self._v2r_links_data: dict = {}
        self._rsu_distances: dict = {}

        self._filtered_v2r_links_data: dict = {}
        self.current_time: int = -1

        self._strategy_name: str = strategy_data[ModelParam.MODEL_NAME]
        _validate_strategy(self._strategy_name)

        self._create_v2r_links_data()

    def _create_v2r_links_data(self) -> None:
        """
        Create the v2r links data.
        """
        # Convert the v2r links df to dictionary
        self._v2r_links_data = (
            self._v2r_links_df.groupby(TraceTimes.TIME_STEP)
            .apply(
                lambda row: dict(
                    zip(
                        row[DeviceId.VEHICLE],
                        zip(
                            row[Column.ROADSIDE_UNITS_STR],
                            row[Column.DISTANCES_STR],
                        ),
                    )
                )
            )
            .to_dict()
        )

        del self._v2r_links_df

    def update_v2r_links(self, v2r_links_df: DataFrame) -> None:
        """
        Update the v2r links.
        """
        self._v2r_links_df = v2r_links_df
        self._create_v2r_links_data()

    def step(self) -> None:
        """
        Step through the v2r allocator.
        """
        self._filtered_v2r_links_data.clear()
        if self.current_time not in self._v2r_links_data:
            return

        self._filtered_v2r_links_data = self._v2r_links_data[self.current_time]

    def get_rsu_for_vehicle(self, vehicle_id: int) -> int:
        """
        Get the roadside unit for the vehicle.

        Parameters
        ----------
        vehicle_id : int
            The vehicle id.

        Returns
        -------
        int
            The roadside unit id.
        """
        logger.debug(f"Looking up RSUs for vehicle {vehicle_id}")

        if len(self._filtered_v2r_links_data) == 0:
            return -1

        # Get the RSUs for the vehicle.
        roadside_units: str = self._filtered_v2r_links_data[vehicle_id][0]
        roadside_units: ndarray[int] = array(roadside_units.split(" ")).astype(int)

        if len(roadside_units) == 0:
            return -1

        match self._strategy_name:
            case ModelType.NEAREST:
                return roadside_units[0]
            case ModelType.RANDOM:
                return roadside_units[random.randint(0, len(roadside_units) - 1)]
