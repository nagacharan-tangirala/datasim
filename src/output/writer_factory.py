from pathlib import Path

from src.core.common_constants import FileExtension
from src.core.exceptions import UnsupportedOutputFormatError
from src.output.agent_data import AgentOutputCSV, AgentOutputParquet
from src.output.model_data import ModelOutputCSV, ModelOutputParquet


class OutputWriterFactory:
    def __init__(self, output_path: Path):
        """
        Initialize the output writer factory.
        """
        self.output_filepath: Path = output_path

    def create_model_output_writer(
        self, output_type: str
    ) -> ModelOutputParquet | ModelOutputCSV:
        """
        Create the model output writer.
        """
        match output_type:
            case FileExtension.PARQUET:
                return ModelOutputParquet(self.output_filepath)
            case FileExtension.CSV:
                return ModelOutputCSV(self.output_filepath)
            case _:
                raise UnsupportedOutputFormatError(output_type)

    def create_agent_output_writer(
        self, output_type: str
    ) -> AgentOutputParquet | AgentOutputCSV:
        """
        Create the agent output writer.
        """
        match output_type:
            case FileExtension.PARQUET:
                return AgentOutputParquet(self.output_filepath)
            case FileExtension.CSV:
                return AgentOutputCSV(self.output_filepath)
            case _:
                raise UnsupportedOutputFormatError(output_type)
