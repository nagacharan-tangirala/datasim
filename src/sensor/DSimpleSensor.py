from src.sensor.BSensor import SensorBase, SensorName


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

    def get_data_size(self):
        pass

    def get_collected_data_size(self, sim_time):
        """
        Collect data from the sensor.

        Returns
        ----------
        int
            The amount of data collected from the sensor.

        """
        if not self.is_active:
            return 0
        self._collect_data(sim_time)
        return self.data * self.data_size

    def _collect_data(self, sim_time: int):
        """
        Collect data from the sensor. This is the distinct part of each sensor.
        Depending on the type of sensor, the data may be collected in different ways.
        We provide a default implementation for the basic sensor which multiplies the frequency with the data size.
        """
        self.data = (self.last_update_time - sim_time) % self.frequency
        self.last_update_time = sim_time
