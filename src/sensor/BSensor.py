from enum import StrEnum
from abc import ABCMeta, abstractmethod


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


class SensorBase(metaclass=ABCMeta):
    """Base class for all sensor classes."""

    def __init__(self, params):
        """
        Initialize the sensor with given parameters.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the sensor.

        """
        self.sensor_id = params.get('id', None)
        self.entity_id = params.get('entity_id', None)

        self.mode = params.get('mode', None)
        self.type = params.get('type', None)

        self.start_time = params.get('start_time', None)
        self.end_time = params.get('end_time', None)

        self.frequency = params.get('frequency', None)
        self.data_size = params.get('data_size', None)

        self.last_update_time = 0
        self.data = None
        self.is_active = False

    @abstractmethod
    def _update_sensor_status(self, sim_time: int):
        """
        Update the sensor status based on the constraints. This method is called before collecting data.

        Parameters
        ----------
        sim_time : int
            The current simulation time.
        """
        pass

    @abstractmethod
    def get_data_size(self):
        """
        Get the data size of the sensor.
        """
        pass

    def is_active(self):
        """
        Check if the sensor is active.

        Returns
        ----------
        bool
            True if the sensor is active, False otherwise.
        """
        return self.is_active

    def get_id(self) -> int:
        """
        Get the ID of the sensor.

        Returns
        ----------
        int
            The ID of the sensor.
        """
        return self.sensor_id

    def get_mode(self):
        """
        Get the mode of the sensor.

        Returns
        ----------
        str
            The mode of the sensor as a string.
        """
        return self.mode.value

    def get_collected_data_size(self) -> int:
        """
        Collect data from the sensor.

        Returns
        ----------
        int
            The amount of data collected from the sensor.

        """
        return self.data * self.data_size

    def collect_data(self, sim_time: int):
        """
        Collect data from the sensor.
        """
        self._update_sensor_status(sim_time)
        if not self.is_active:
            self.data = 0
        else:
            self.data = ((sim_time - self.last_update_time) / 1000) * self.frequency
        self.last_update_time = sim_time
