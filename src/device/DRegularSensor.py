from mesa import Model
from src.device.BSensor import SensorBase


class RegularSensor(SensorBase):
    def __init__(self, params: dict, sensor_model: Model, time_step: int):
        """
        Initialize the sensor.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the sensor.
        """
        super().__init__(params, sensor_model, time_step)

    def step(self):
        """
        Step function for the sensor.
        """
        self.data_cache.append(self.data)
        if self.active:
            self.data = (self.time_step / 1000.0) * self.frequency * self.data_size
