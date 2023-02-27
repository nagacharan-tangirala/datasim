from src.device.BEntity import EntityBase, EntityType, EntityStatus


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

    def get_location(self) -> list[float]:
        """
        Get the location of the vehicle entity.

        Returns
        ----------
        list
            The location of the vehicle entity as a list.
        """
        return self.location

    def process_entity(self, ts: int):
        """
        Update the location and collect data from the sensors associated with this entity.

        Parameters
        ----------
        ts : int
            The current time.
        """
        # Update the location of the entity
        self.mobility_model.update_location(ts)
        self.location = self.mobility_model.get_current_location()

        # Update and get the data collected by the sensors
        self.total_sensor_data_size = 0
        for sensor in self.sensors.values():
            sensor.collect_data(ts)
            self.total_sensor_data_size = self.total_sensor_data_size + sensor.get_collected_data_size()

    def toggle_entity_status(self):
        """
        Toggle the status of the entity.
        """
        self.status = EntityStatus.ACTIVE if self.status == EntityStatus.INACTIVE else EntityStatus.INACTIVE
