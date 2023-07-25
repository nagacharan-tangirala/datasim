import logging
from typing import Any

from pandas import DataFrame, concat
from pyarrow.parquet import ParquetFile

from src.core.CommonConstants import CC_PARQUET, CC_TIME_STEP

logger = logging.getLogger(__name__)


class ParquetDataReader:
    def __init__(self, input_file: str, column_names: list[str], column_dtypes: dict[str, Any]):
        """
        Initialize the input data streamer.
        """
        self._input_file: str = input_file
        self._column_names: list[str] = column_names
        self._column_dtypes: dict[str, Any] = column_dtypes

        self._input_file_reader: ParquetFile = ParquetFile(input_file)
        self._total_row_groups: int = self._input_file_reader.num_row_groups

        self._row_group_idx: int = 0
        self._type = CC_PARQUET

    @property
    def input_file(self) -> str:
        """ Returns the input file."""
        return self._input_file

    @property
    def type(self) -> str:
        """ Returns the data reader type."""
        return self._type

    def read_data_until_timestamp(self, timestamp: int) -> DataFrame:
        """
        Stream the data from the input file until the timestamp.
        """
        data_df = DataFrame()
        logger.debug(f"Trying to fetch data until timestamp {timestamp}.")
        while self._row_group_idx < self._total_row_groups:
            # Read the next row group from the input file and convert it to a pandas dataframe.
            temp_data_df = self._input_file_reader.read_row_group(self._row_group_idx,
                                                                  columns=self._column_names,
                                                                  use_threads=True).to_pandas()

            logger.debug(f"Got data for row group {self._row_group_idx} from the input file.")
            logger.debug(f"Number of rows in the row group is {len(temp_data_df)}.")

            if temp_data_df.empty:
                return data_df

            # Set the column dtypes and get the maximum timestamp in the current chunk.
            temp_data_df = temp_data_df.astype(self._column_dtypes)
            max_timestamp = temp_data_df[CC_TIME_STEP].max()

            logger.debug(f"Maximum timestamp in the streamed data is {max_timestamp}.")

            # Check if the maximum timestamp is less than the timestamp.
            if max_timestamp < timestamp:
                # Add the entire data to the dataframe.
                data_df = concat([data_df, temp_data_df], ignore_index=True)
                self._row_group_idx += 1
            else:
                # Add the data until the timestamp to the dataframe. Do not increment the row group index.
                temp_data_df = temp_data_df[temp_data_df[CC_TIME_STEP] < timestamp]
                data_df = concat([data_df, temp_data_df], ignore_index=True)
                break

        logger.debug(f"Returning data until timestamp {timestamp} with {len(data_df)} rows.")
        return data_df
