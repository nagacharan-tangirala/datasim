from pathlib import Path

from pandas import DataFrame


class ModelOutputParquet:
    def __init__(self, output_path: Path):
        """
        Initialize the model output.
        """
        self._output_file = output_path / "model_output.parquet"

    def write_output(self, data: DataFrame):
        """
        Write the output to the file.
        """
        data.to_parquet(self._output_file)


class ModelOutputCSV:
    def __init__(self, output_path: Path):
        """
        Initialize the model output.
        """
        self._output_file = output_path / "model_output.csv"

    def write_output(self, data: DataFrame):
        """
        Write the output to the file.
        """
        data.to_csv(self._output_file)
