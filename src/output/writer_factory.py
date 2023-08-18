from pathlib import Path

import src.core.common_constants as cc
from src.core.exceptions import UnsupportedOutputFormatError
from src.output.agent_data import AgentOutputCSV, AgentOutputParquet
from src.output.model_data import ModelOutputCSV, ModelOutputParquet


class OutputWriterFactory:
    def __init__(self, output_path: str):
        """
        Initialize the output writer factory.
        """
        self.output_path: str = output_path

    def create_model_output_writer(
        self, output_type: str
    ) -> ModelOutputParquet | ModelOutputCSV:
        """
        Create the model output writer.
        """
        match output_type:
            case cc.PARQUET:
                return ModelOutputParquet(self.output_path)
            case cc.CSV:
                return ModelOutputCSV(self.output_path)
            case _:
                raise UnsupportedOutputFormatError(output_type)

    def create_agent_output_writer(
        self, output_type: str
    ) -> AgentOutputParquet | AgentOutputCSV:
        """
        Create the agent output writer.
        """
        match output_type:
            case cc.PARQUET:
                return AgentOutputParquet(self.output_path)
            case cc.CSV:
                return AgentOutputCSV(self.output_path)
            case _:
                raise UnsupportedOutputFormatError(output_type)
