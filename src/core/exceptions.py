class UnsupportedInputFormatError(Exception):
    """The input file is not supported."""

    def __init__(self, file_name: str, message: str = ""):
        super().__init__(message)
        self.file_name = file_name

    def __str__(self):
        return f"The input file '{self.file_name}' has unsupported format."


class UnsupportedOutputFormatError(Exception):
    """The output format is not supported."""

    def __init__(self, output_format: str, message: str = ""):
        super().__init__(message)
        self.output_format = output_format

    def __str__(self):
        return f"The output format '{self.output_format}' is not supported."


class ModelTypeNotImplementedError(Exception):
    """The model type is not implemented."""

    def __init__(self, model_name, model_type: str, message: str = ""):
        super().__init__(message)
        self.model_name = model_name
        self.model_type = model_type

    def __str__(self):
        return f"The model '{self.model_name}' with type '{self.model_type}' is not implemented."
