from src.sensor.BSensor import SensorBase


class AlwaysOnSensor(SensorBase):
    def __init__(self, params: dict):
        """
        Initialize the sensor.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the sensor.
        """
        super().__init__(params)
        self.is_active = True

    def get_data_size(self):
        pass

    def _update_sensor_status(self, sim_time: int):
        """
        Activate the sensor. This method is called by the entity when the start time of the sensor is reached.
        For the AlwaysActiveSensor, this method does not change the status of the sensor.
        """
        self.is_active = True
