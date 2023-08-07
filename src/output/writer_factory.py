import src.core.common_constants as cc
from src.core.exceptions import UnsupportedOutputFormatError
from src.output.model_data import ModelOutputParquet, ModelOutputCSV


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
