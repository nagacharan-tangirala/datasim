class NearestTowerNotAssignedError(Exception):
    """ The nearest tower is not assigned to a vehicle. """

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"The nearest tower is not assigned to a vehicle."


class NotSupportedCellTowerError(Exception):
    """ The cell tower type is not supported. """

    def __init__(self, cell_tower_type: str, message: str = ""):
        super().__init__(message)
        self.cell_tower_type = cell_tower_type

    def __str__(self):
        return f"The cell tower type '{self.cell_tower_type}' is not supported."


class NoCellTowersInSimulationError(Exception):
    """ There are no cell towers in the simulation. """

    def __init__(self, message: str = ""):
        super().__init__(message)

    def __str__(self):
        return f"There are no cell towers in the simulation."


class KeyMissinginConfigError(Exception):
    """ The JSON file is missing a key. """

    def __init__(self, key: str, message: str = ""):
        super().__init__(message)
        self.key: str = key

    def __str__(self):
        return f"The JSON file does not contain the key '{self.key}'."


class DuplicateDeviceModelError(Exception):
    """ The model is duplicated for a given device. """

    def __init__(self, model: str, message: str = ""):
        super().__init__(message)
        self.model = model

    def __str__(self):
        return f"The model '{self.model}' is duplicated for a given device."


class UnsupportedInputFormatError(Exception):
    """ The input file is not supported. """

    def __init__(self, file_name: str, message: str = ""):
        super().__init__(message)
        self.file_name = file_name

    def __str__(self):
        return f"The input file '{self.file_name}' has unsupported format."


class TimeColumnMissingError(Exception):
    """ The time column is missing in the input file. """

    def __init__(self, file_name: str, message: str = ""):
        super().__init__(message)
        self.file_name = file_name

    def __str__(self):
        return f"The time column is missing in the input file '{self.file_name}'."


class WrongActivationTimeError(Exception):
    """ The activation time is wrong. """

    def __init__(self, activation_time: int, start_time: int, message: str = ""):
        super().__init__(message)
        self.activation_time = activation_time
        self.start_time = start_time

    def __str__(self):
        return f"The activation time '{self.activation_time}' is wrong. It should be equal to the start time '{self.start_time}'."


class WrongDeactivationTimeError(Exception):
    """ The deactivation time is wrong. """

    def __init__(self, deactivation_time: int, end_time: int, message: str = ""):
        super().__init__(message)
        self.deactivation_time = deactivation_time
        self.end_time = end_time

    def __str__(self):
        return f"The deactivation time '{self.deactivation_time}' is wrong. It should be equal to the end time '{self.end_time}'."


class DuplicateDeviceFoundError(Exception):
    """ The UE is duplicated in the input file. """

    def __init__(self, device_id: int, device_type: str, message: str = ""):
        super().__init__(message)
        self.device_id = device_id
        self.device_type = device_type

    def __str__(self):
        return f"The device with id '{self.device_id}' and '{self.device_type}' is duplicated in the input file."


class ModelTypeNotImplementedError(Exception):
    """ The model type is not implemented. """

    def __init__(self, model_name, model_type: str, message: str = ""):
        super().__init__(message)
        self.model_name = model_name
        self.model_type = model_type

    def __str__(self):
        return f"The model '{self.model_name}' with type '{self.model_type}' is not implemented."


class DuplicateChannelModelError(Exception):
    """ The channel model is duplicated. """

    def __init__(self, channel_model: str, message: str = ""):
        super().__init__(message)
        self.channel_model = channel_model

    def __str__(self):
        return f"The channel model '{self.channel_model}' is duplicated."
