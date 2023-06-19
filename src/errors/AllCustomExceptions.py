

class NearestTowerNotAssignedError(Exception):
    """ The nearest tower is not assigned to a vehicle. """
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"The nearest tower is not assigned to a vehicle."
