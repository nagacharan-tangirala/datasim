from abc import abstractmethod
from enum import StrEnum
from mesa import Agent, Model


class SensorMode(StrEnum):
    """Enum for sensor types."""
    RANDOM = 'random'
    MARKOV = 'markov'
    CUSTOM = 'custom'
    REGULAR = 'regular'
    ALWAYS_ON = 'always_on'


class SensorType(StrEnum):
    """Enum for sensor types."""
    CAMERA = 'camera'
    RADAR = 'radar'
    LIDAR = 'lidar'
    GPS = 'gps'
    IMU = 'imu'
    SPEED = 'speed'
    LIGHT = 'light'
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    PRESSURE = 'pressure'
    NOISE = 'noise'


class SensorBase(Agent):
    """Base class for all sensor classes."""

    def __init__(self, params, sensor_model: Model, time_step: int):
        """
        Initialize the sensor with given parameters.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the sensor.

        """
        super().__init__(params.get('id', 0), sensor_model)

        self.mode = params.get('mode', None)
        self.type = params.get('type', None)

        self.start_time = params.get('start_time', None)
        self.end_time = params.get('end_time', None)

        self.frequency = params.get('frequency', None)
        self.data_size = params.get('data_size', None)

        self.sensor_model = sensor_model
        self.time_step = time_step

        self.data = None
        self.active = False

    @abstractmethod
    def step(self):
        """
        Collect data from the sensor.
        """
        pass

    def activate(self):
        """
        Activate the sensor.
        """
        self.active = True
        self.sensor_model.schedule.add(self)

    def deactivate(self):
        """
        Deactivate the sensor.
        """
        self.active = False
        self.sensor_model.schedule.remove(self)

    def _update_sensor_status(self, sim_time: int):
        """
        Update the sensor status based on the constraints. This method is called before collecting data.

        Parameters
        ----------
        sim_time : int
            The current simulation time.
        """
        pass

    def get_collected_data_size(self) -> float:
        """
        Get the size of the data collected by the sensor.

        Returns
        ----------
        float
            The amount of data collected from the sensor.

        """
        return self.data * self.data_size
