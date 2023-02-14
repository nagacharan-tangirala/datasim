from enum import Enum
from abc import ABCMeta, abstractmethod


class EntityType(Enum):
    """Enum for entity types."""

    RSU = 0
    VEHICLE = 1
    INFRA = 2
    IOT = 3
    

class EntityBase(metaclass=ABCMeta):
    """Base class for all entity classes."""

    def __init__(self, entity_info: dict):
        """Initialize the entity."""
        self.sensor_dict = entity_info.get('sensor_dict', None)
        self.sensors = {}

    def initiate_sensors(self):
        """
        Initiate the sensor_params with their respective parameters.
        """
        self.sensor_ids = list(self.sensor_dict.keys())

    @abstractmethod
    def run(self):
        """Run the entity."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the entity."""
        pass

    @abstractmethod
    def get_status(self):
        """Get the status of the entity."""
        pass

    @abstractmethod
    def get_statistics(self):
        """Get the statistics of the entity."""
        pass

    @abstractmethod
    def get_version(self):
        """Get the version of the entity."""
        pass

    @abstractmethod
    def get_id(self):
        """Get the ID of the entity."""
        pass

    @abstractmethod
    def get_name(self):
        """Get the mode of the entity."""
        pass

    @abstractmethod
    def get_location(self):
        """Get the location of the entity."""
        pass

    @abstractmethod
    def get_type(self):
        """Get the type of the entity."""
        pass

    @abstractmethod
    def get_description(self):
        """Get the description of the entity."""
        pass

    @abstractmethod
    def get_ip(self):
        """Get the IP address of the entity."""
        pass

    @abstractmethod
    def get_mac(self):
        """Get the MAC address of the entity."""
        pass

    @abstractmethod
    def get_port(self):
        """Get the port of the entity."""
        pass

    @abstractmethod
    def get_username(self):
        """Get the username of the entity."""
        pass

    @abstractmethod
    def get_password(self):
        """Get the password of the entity."""
        pass

    @abstractmethod
    def get_protocol(self):
        """Get the protocol of the entity."""
        pass

    @abstractmethod
    def get_os(self):
        """Get the OS of the entity."""
        pass

    @abstractmethod
    def get_os_version(self):
        """Get the OS version of the entity."""
        pass

    @abstractmethod
    def get_os_architecture(self):
        """Get the OS architecture of the entity."""
        pass

    @abstractmethod
    def get_os_kernel(self):
        """Get the OS kernel of the entity."""
        pass

    @abstractmethod
    def get_os_release(self):
        """Get the OS release of the entity."""
        pass