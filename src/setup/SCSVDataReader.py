from typing import Any

import pandas as pd

from src.setup.SInputDataReader import InputDataReader


class CSVDataReader(InputDataReader):
    def __init__(self, input_file: str, column_names: list[str], column_dtypes: dict[str, Any]):
        """
        Initialize the input data streamer.
        """
        super().__init__(input_file, column_names, column_dtypes)

    def get_type(self) -> str:
        """
        Get the type of the input data reader.

        Returns
        -------
        str
            The type of the input data reader.
        """
        return 'csv'

    def read_all_data(self) -> pd.DataFrame:
        """
        Reads all data from the input file.

        Returns
        -------
        pd.DataFrame
            The data dataframe.
        """
        self.data_df = pd.read_csv(self.input_file, names=self.column_names, dtype=self.column_dtypes)
        return self.data_df