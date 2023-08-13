from os.path import join

from pandas import DataFrame


class AgentOutputParquet:
    def __init__(self, output_path: str):
        """
        Initialize the agent output writer
        """
        self._output_file = join(output_path, "agent_output.parquet")

    def write_output(self, data: DataFrame):
        """
        Write the output to the file.
        """
        data.to_parquet(self._output_file)


class AgentOutputCSV:
    def __init__(self, output_path: str):
        """
        Initialize the agent output writer.
        """
        self._output_file = join(output_path, "agent_output.csv")

    def write_output(self, data: DataFrame):
        """
        Write the output to the file.
        """
        data.to_csv(self._output_file)
