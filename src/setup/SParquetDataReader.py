from typing import Any

from pandas import DataFrame, read_parquet
from pyarrow.parquet import ParquetFile

from src.setup.SInputDataReader import InputDataReader


class ParquetDataReader(InputDataReader):
    def __init__(self, input_file: str, column_names: list[str], column_dtypes: dict[str, Any]):
        """
        Initialize the input data streamer.
        """
        super().__init__(input_file, column_names, column_dtypes)
        self.total_row_groups: int = ParquetFile(input_file).num_row_groups

        self.data_df: DataFrame = DataFrame()
        self.row_group_idx: int = 0

    def get_type(self) -> str:
        """
        Get the type of the input data reader.

        Returns
        -------
        str
            The type of the input data reader.
        """
        return 'parquet'

    def read_data_until_timestamp(self, timestamp: int) -> DataFrame:
        """
        Read the next chunk from the input file.
        """
        self.data_df = DataFrame()
        while self.row_group_idx < self.total_row_groups:
            temp_data_df = read_parquet(self.input_file, columns=self.column_names, dtype=self.column_dtypes, row_group=self.row_group_idx)

            # Check if the data is empty.
            if temp_data_df.empty:
                return self.data_df

            # Get the maximum timestamp in the current chunk.
            max_timestamp = temp_data_df['time'].max()

            # Check if the maximum timestamp is less than the timestamp.
            if max_timestamp < timestamp:
                # Add the entire data to the dataframe.
                self.data_df = self.data_df.append(temp_data_df, ignore_index=True)
                self.row_group_idx += 1
            else:
                # Add the data until the timestamp to the dataframe. Do not increment the row group index.
                self.data_df = self.data_df.append(temp_data_df[temp_data_df['time'] < timestamp], ignore_index=True)
                break

        return self.data_df
