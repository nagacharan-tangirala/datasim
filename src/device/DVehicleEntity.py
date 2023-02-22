from src.device.BEntity import EntityBase, EntityType


class VehicleEntity(EntityBase):
    """
    Vehicle entity class designed to mimic the behavior of vehicles.
    """

    def __init__(self, params: dict, sensors: dict):
        """
        Initialize the vehicle entity.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the vehicle entity.
        """
        super().__init__(params, sensors)
        self.type: EntityType = EntityType.VEHICLE

    def get_statistics(self):
        pass

    def get_location(self) -> list[float]:
        """
        Get the location of the vehicle entity.

        Returns
        ----------
        list
            The location of the vehicle entity as a list.
        """
        return self.location
