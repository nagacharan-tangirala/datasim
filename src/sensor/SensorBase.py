from enum import Enum
from abc import ABCMeta, abstractmethod


class SensorType(Enum):
    """Enum for IOT sensor types."""
    CAMERA = 0
    RADAR = 1
    LIDAR = 2
    GPS = 3
    IMU = 4
    SPEED = 5
    LIGHT = 6
    TEMPERATURE = 7
    HUMIDITY = 8
    PRESSURE = 9
    NOISE = 10


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
        """Get the name of the sensor."""
        return self.entity_id

    def get_type(self):
        """Get the type of the sensor."""
        return self.type

    @abstractmethod
    def collect_data(self):
        """Collect the data from the sensor."""
        pass

    @abstractmethod
    def get_data_size(self):
        """Get the data type of the sensor."""
        pass

    @abstractmethod
    def get_data_unit(self):
        """Get the data unit of the sensor."""
        pass

    @abstractmethod
    def get_data_range(self):
        """Get the data range of the sensor."""
        pass

    @abstractmethod
    def get_data_rate(self):
        """Get the data rate of the sensor."""
        pass

    @abstractmethod
    def get_data_accuracy(self):
        """Get the data accuracy of the sensor."""
        pass

    @abstractmethod
    def get_data_resolution(self):
        """Get the data resolution of the sensor."""
        pass

    @abstractmethod
    def get_data_precision(self):
        """Get the data precision of the sensor."""
        pass

    @abstractmethod
    def get_data_error(self):
        """Get the data error of the sensor."""
        pass

    @abstractmethod
    def get_data_noise(self):
        """Get the data noise of the sensor."""
        pass

    @abstractmethod
    def get_data_delay(self):
        """Get the data delay of the sensor."""
        pass
