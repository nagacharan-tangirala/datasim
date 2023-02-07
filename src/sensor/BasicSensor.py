from src.sensor.SensorBase import SensorBase, SensorType


class BasicSensor(SensorBase):
    def __init__(self, params: dict):
        """
        Initialize the sensor.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the sensor.
        """
        super().__init__(params)

        self.start_times = params.get('start_times', None)
        self.end_times = params.get('end_times', None)

        self.frequency = params.get('frequency', None)
        self.data_size = params.get('data_size', None)
