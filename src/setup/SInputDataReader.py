from abc import abstractmethod
from typing import Any

from pandas import DataFrame


class InputDataReader:
    def __init__(self, input_file: str, column_names: list[str], column_dtypes: dict[str, Any]):
        """
        Initialize the input data reader.
        """
        self.input_file: str = input_file
        self.column_names: list[str] = column_names
        self.column_dtypes: dict[str, Any] = column_dtypes

        self.data_df: DataFrame | None = None

    @abstractmethod
    def get_type(self) -> str:
        """
        Get the type of the input data reader.

        Returns
        -------
        str
            The type of the input data reader.
        """
        pass

    def get_input_file(self) -> str:
        """
        Get the input file.

        Returns
        -------
        str
            The input file.
        """
        return self.input_file

    def read_data_until_timestamp(self, timestamp: int) -> DataFrame:
        """
        Read the next chunk from the input file. This method is used for the data reader types that support reading data in chunks.

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
        Reads all data from the input file. This method is used for the data reader types read all data at once.

        Returns
        -------
        DataFrame
            The data dataframe.
        """
        raise NotImplementedError
