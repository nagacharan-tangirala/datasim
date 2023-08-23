from random import choice

from core.common_constants import ColumnNames, DeviceId
from core.constants import ModelParam, ModelType
from models.allocator import _validate_strategy
from pandas import DataFrame


class B2CAllocator:
    def __init__(self, b2c_links_df: DataFrame, strategy_data: dict):
        """
        Initialize the b2c allocator.
        """
        self._b2c_links_df: DataFrame = b2c_links_df

        self._b2c_links_data: dict = {}
        self._strategy_name: str = strategy_data[ModelParam.MODEL_NAME]
        _validate_strategy(self._strategy_name)
        self._create_b2c_links_data()

    def _create_b2c_links_data(self) -> None:
        """
        Create the b2c links data.
        """
        # Convert the b2c links df to dictionary
        self._b2c_links_data = dict(
            zip(
                self._b2c_links_df[ColumnNames.B2C_LINKS[1]],
                self._b2c_links_df[ColumnNames.B2C_LINKS[2]],
            )
        )

    def get_controller(self, base_station: int) -> int:
        """
        Get the controller for the base station.
        """
        return self._b2c_links_data[base_station]


class R2BAllocator:
    def __init__(self, r2b_links_df: DataFrame, strategy_data: dict):
        """
        Initialize the r2b allocator.
        """
        self._r2b_links_df: DataFrame = r2b_links_df

        self._r2b_links_data: dict = {}
        self._strategy_name: str = strategy_data[ModelParam.MODEL_NAME]
        _validate_strategy(self._strategy_name)
        self._create_r2b_links_data()

    def _create_r2b_links_data(self) -> None:
        """
        Create the r2b links data.
        """
        # Convert the r2b links df to dictionary
        # Distances are in the trace, can be used later.
        self._r2b_links_data = dict(
            zip(
                self._r2b_links_df[ColumnNames.R2B_LINKS[1]],
                self._r2b_links_df[ColumnNames.R2B_LINKS[2]],
            )
        )
        # for rsu_id, base_stations in r2b_dict.items():
        #     match self._strategy_name:
        #         case "random":
        #             self._r2b_links_data[rsu_id] = choice(base_stations)
        #         case "nearest":
        #             self._r2b_links_data[rsu_id] = base_stations[0]

    def get_base_station(self, roadside_unit: int) -> int:
        """
        Get the base station for the roadside unit.
        """
        base_stations = self._r2b_links_data[roadside_unit]
        match self._strategy_name:
            case ModelType.RANDOM:
                return choice(base_stations)
            case ModelType.NEAREST:
                return base_stations[0]


class R2RAllocator:
    def __init__(self, r2r_links_df: DataFrame, strategy_data: dict):
        """
        Initialize the r2r allocator.
        """
        self._r2r_links_df: DataFrame = r2r_links_df

        self._r2r_links_data: dict = {}
        self._strategy_name: str = strategy_data[ModelParam.MODEL_NAME]
        _validate_strategy(self._strategy_name)
        self._create_r2r_links_data()

    def _create_r2r_links_data(self) -> None:
        """
        Create the r2r links data.
        """
        # Convert the r2r links df to dictionary
        # Distances are in the trace, can be used later.
        self._r2r_links_data = dict(
            zip(
                self._r2r_links_df[ColumnNames.R2R_LINKS[1]],
                self._r2r_links_df[ColumnNames.R2R_LINKS[2]],
            )
        )

    def get_roadside_unit(self, roadside_unit: int) -> int:
        """
        Get the roadside unit for the roadside unit.
        """
        roadside_units = self._r2r_links_data[roadside_unit]
        match self._strategy_name:
            case ModelType.RANDOM:
                return choice(roadside_units)
            case ModelType.NEAREST:
                return roadside_units[0]
