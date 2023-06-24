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


class InvalidXMLTagError(Exception):
    """ The XML tag is invalid. """

    def __init__(self, tag: str, message: str = ""):
        super().__init__(message)
        self.tag = tag

    def __str__(self):
        return f"The XML tag '{self.tag}' is invalid in the configuration file."


class InvalidXMLAttributeError(Exception):
    """ The XML attribute is invalid. """

    def __init__(self, tag: str, attribute: str, valid_values: list, message: str = ""):
        super().__init__(message)
        self.tag = tag
        self.attribute = attribute
        self.valid_values = valid_values

    def __str__(self):
        return f"The XML attribute '{self.attribute}' in the XML tag '{self.tag}' is invalid. Valid values are {self.valid_values}."


class DuplicateDeviceModelError(Exception):
    """ The model is duplicated for a given device. """

    def __init__(self, model: str, message: str = ""):
        super().__init__(message)
        self.model = model

    def __str__(self):
        return f"The model '{self.model}' is duplicated for a given device."
