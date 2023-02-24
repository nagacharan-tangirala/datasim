from src.sensor.BSensor import SensorBase


class RegularSensor(SensorBase):
    def __init__(self, params: dict):
        """
        Initialize the sensor.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the sensor.
        """
        super().__init__(params)

    def get_data_size(self):
        pass

    def _update_sensor_status(self, sim_time: int):
        """
        Activate the sensor. This method is called by the entity when the start time of the sensor is reached.
        """
        if self.is_active:
            # If the sensor is already active, check if the sensor should be deactivated
            if sim_time > self.end_time:
                self.is_active = False
        else:
            # If the sensor is not active, check if the sensor should be activated
            if self.start_time < sim_time <= self.end_time:
                self.is_active = True
                self.last_update_time = self.start_time
