from src.device.BEntity import EntityBase, EntityType, EntityStatus


class RSUEntity(EntityBase):
    """
    Vehicle entity class designed to mimic the behavior of vehicles.
    """

    def __init__(self, params: dict, sensors: dict):
        """
        Initialize the RSU.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the RSU.
        """
        super().__init__(params, sensors)
        self.type: EntityType = EntityType.RSU

        self.status = EntityStatus.ACTIVE  # RSU is always active

    def get_statistics(self):
        pass

    def get_location(self) -> list[float]:
        """
        Get the location of the RSU.

        Returns
        ----------
        list
            The location of the RSU as a list.
        """
        return self.location

    def process_entity(self, time: int):
        """
        Update the location and collect data from the sensors associated with this entity.

        Parameters
        ----------
        time : int
            The current time.
        """
        # Get the data collected by the sensors
        self.total_sensor_data_size = 0
        for sensor in self.sensors.values():
            sensor.collect_data(time)
            self.total_sensor_data_size = self.total_sensor_data_size + sensor.get_collected_data_size()

    def toggle_entity_status(self):
        """
        Toggle the status of the entity. RSU is always active.
        """
        self.status = EntityStatus.ACTIVE
