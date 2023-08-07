class NoBaseStationsInSimulationError(Exception):
    """There are no base stations in the simulation."""

    def __init__(self, message: str = ""):
        super().__init__(message)

    def __str__(self):
        return f"There are no base stations in the simulation."


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


class WrongActivationTimeError(Exception):
    """The activation time is wrong."""

    def __init__(self, activation_time: int, start_time: int, message: str = ""):
        super().__init__(message)
        self.activation_time = activation_time
        self.start_time = start_time

    def __str__(self):
        return f"The activation time '{self.activation_time}' is wrong. It should be equal to the start time '{self.start_time}'."


class WrongDeactivationTimeError(Exception):
    """The deactivation time is wrong."""

    def __init__(self, deactivation_time: int, end_time: int, message: str = ""):
        super().__init__(message)
        self.deactivation_time = deactivation_time
        self.end_time = end_time

    def __str__(self):
        return f"The deactivation time '{self.deactivation_time}' is wrong. It should be equal to the end time '{self.end_time}'."


class DuplicateDeviceFoundError(Exception):
    """The UE is duplicated in the input file."""

    def __init__(self, device_id: int, device_type: str, message: str = ""):
        super().__init__(message)
        self.device_id = device_id
        self.device_type = device_type

    def __str__(self):
        return f"The device with id '{self.device_id}' and '{self.device_type}' is duplicated in the input file."


class ModelTypeNotImplementedError(Exception):
    """The model type is not implemented."""

    def __init__(self, model_name, model_type: str, message: str = ""):
        super().__init__(message)
        self.model_name = model_name
        self.model_type = model_type

    def __str__(self):
        return f"The model '{self.model_name}' with type '{self.model_type}' is not implemented."
