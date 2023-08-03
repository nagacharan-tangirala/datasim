import logging
from typing import Any

from pandas import DataFrame, read_csv

from src.core.common_constants import CC_CSV

logger = logging.getLogger(__name__)


class CSVDataReader:
    def __init__(
        self, input_file: str, column_names: list[str], column_dtypes: dict[str, Any]
    ):
        """
        Initialize the input data streamer.
        """
        self._input_file: str = input_file
        self._column_names: list[str] = column_names
        self._column_dtypes: dict[str, Any] = column_dtypes

        self._type = CC_CSV

    @property
    def input_file(self) -> str:
        """Returns the input file."""
        return self._input_file

    @property
    def type(self) -> str:
        """Returns the data reader type."""
        return self._type

    def read_all_data(self) -> DataFrame:
        """
        Reads all data from the input file.

        Returns
        -------
        pd.DataFrame
            The data dataframe.
        """
        data_df = read_csv(
            self._input_file,
            names=self._column_names,
            dtype=self._column_dtypes,
            skiprows=1,
        )
        logger.debug(f"Returning {len(data_df)} rows from the file {self._input_file}.")
        return data_df
