from typing import Any

import pandas as pd

from src.core.CustomExceptions import StreamingEnabledError, StreamingNotEnabledError, UnsupportedFormatForStreamingError, UnsupportedInputFormatError


class InputDataStreamer:
    def __init__(self, input_file: str, column_names: list[str], column_dtypes: dict[str, Any], is_streaming: bool = False):
        """
        Initialize the input data streamer.
        """
        self.input_file: str = input_file
        self.column_names: list[str] = column_names
        self.column_dtypes: dict[str, Any] = column_dtypes
        self.is_streaming: bool = is_streaming

        self.input_file_type: str = input_file.split(".")[-1]

        self.data_df: pd.DataFrame | None = None
        self.row_group_idx: int = 0

    def stream_next_chunk(self) -> None:
        """
        Read the next chunk from the input file.
        """
        if not self.is_streaming:
            raise StreamingNotEnabledError(self.input_file)

        match self.input_file_type:
            case "csv":
                raise UnsupportedFormatForStreamingError(self.input_file_type)
            case "parquet":
                self.data_df = pd.read_parquet(self.input_file, columns=self.column_names, dtype=self.column_dtypes, row_group=self.row_group_idx)
            case _:
                raise UnsupportedInputFormatError(self.input_file)

        # Increment the row group index.
        self.row_group_idx += 1

    def read_all_data(self) -> None:
        """
        Reads all data from the input file.
        """
        if self.is_streaming:
            raise StreamingEnabledError(self.input_file)

        match self.input_file_type:
            case "csv":
                self.data_df = pd.read_csv(self.input_file, names=self.column_names, dtype=self.column_dtypes)
            case "parquet":
                self.data_df = pd.read_parquet(self.input_file, columns=self.column_names, dtype=self.column_dtypes)
            case _:
                raise UnsupportedInputFormatError(self.input_file)

    def get_data_df(self) -> pd.DataFrame:
        """
        Get the data dataframe.
        """
        return self.data_df
