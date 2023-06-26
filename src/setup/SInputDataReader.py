from typing import Any

from pandas import DataFrame


class InputDataReader:
    def __init__(self, input_file: str, column_names: list[str], column_dtypes: dict[str, Any]):
        """
        Initialize the input data reader.
        """
        self._input_file: str = input_file
        self._column_names: list[str] = column_names
        self._column_dtypes: dict[str, Any] = column_dtypes

        self.data_df: DataFrame | None = None
        self.type = ''

    @property
    def input_file(self) -> str:
        return self._input_file

    def read_data_until_timestamp(self, timestamp: int) -> DataFrame:
        """
        Read the next chunk from the input file. This method should be overridden for the data reader types that support reading data in chunks.

        Parameters
        ----------
        timestamp : int
            The timestamp until which the data should be read.

        Returns
        -------
        DataFrame
            The data dataframe.
        """
        raise NotImplementedError

    def read_all_data(self) -> DataFrame:
        """
        Reads all data from the input file. This method should be overridden for the data reader types read all data at once.

        Returns
        -------
        DataFrame
            The data dataframe.
        """
        raise NotImplementedError
