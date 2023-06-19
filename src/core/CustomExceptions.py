

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
