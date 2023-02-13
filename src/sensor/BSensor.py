from enum import StrEnum
from abc import ABCMeta, abstractmethod


class SensorType(StrEnum):
    """Enum for sensor types."""
    BASIC = 'basic'
    INTERMITTENT = 'intermittent'
    RANDOM = 'random'


class SensorName(StrEnum):
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
        self.id = params.get('id', None)
        self.entity_id = params.get('entity_id', None)

        self.name = params.get('name', None)
        self.type = params.get('type', None)

        self.last_update_time = 0
        self.data = None
        self.is_active = False

    def activate_sensor(self):
        """
        Activate the sensor. This method is called by the entity when the start time of the sensor is reached.
        """
        self.is_active = True

    def deactivate_sensor(self):
        """
        Disable the sensor. This method is called by the entity when the end time of the sensor is reached.
        """
        self.is_active = False

    def get_status(self):
        """Get the status of the sensor."""
        return self.is_active

    def get_id(self):
        """Get the ID of the sensor."""
        return self.id

    def get_entity_id(self):
        """Get the entity ID to which the sensor belongs to."""
        return self.entity_id

    def get_name(self):
        """Get the name of the sensor."""
        return self.name

    @abstractmethod
    def get_data_size(self):
        """Get the data size of the sensor."""
        pass

    @abstractmethod
    def get_collected_data_size(self, sim_time: int):
        """
        Collect data from the sensor.

        Returns
        ----------
        int
            The amount of data collected from the sensor.

        """
        pass

    @abstractmethod
    def _collect_data(self, sim_time: int):
        """Collect data from the sensor."""
        pass
