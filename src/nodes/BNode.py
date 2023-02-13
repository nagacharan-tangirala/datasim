from abc import ABCMeta, abstractmethod


class NodeBase(metaclass=ABCMeta):
    """Base class for all base station classes."""

    def __init__(self, params: dict):
        """Initialize the base station."""
        pass


    @abstractmethod
    def run(self):
        """Run the base station."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the base station."""
        pass

    @abstractmethod
    def get_status(self):
        """Get the status of the base station."""
        pass

    @abstractmethod
    def get_statistics(self):
        """Get the statistics of the base station."""
        pass

    @abstractmethod
    def get_version(self):
        """Get the version of the base station."""
        pass

    @abstractmethod
    def get_id(self):
        """Get the ID of the base station."""
        pass

    @abstractmethod
    def get_name(self):
        """Get the name of the base station."""
        pass

    @abstractmethod
    def get_location(self):
        """Get the location of the base station."""
        pass

    @abstractmethod
    def get_type(self):
        """Get the type of the base station."""
        pass

    @abstractmethod
    def get_description(self):
        """Get the description of the base station."""
        pass

    @abstractmethod
    def get_capabilities(self):
        """Get the capabilities of the base station."""
        pass

    @abstractmethod
    def get_configuration(self):
        """Get the configuration of the base station."""
        pass

    @abstractmethod
    def get_network(self):
        """Get the network of the base station."""
        pass

    @abstractmethod
    def get_network_status(self):
        """Get the network status of the base station."""
        pass

    @abstractmethod
    def get_network_statistics(self):
        """Get the network statistics of the base station."""
        pass

    @abstractmethod
    def get_network_configuration(self):
        """Get the network configuration of the base station."""
        pass

    @abstractmethod
    def get_network_capabilities(self):
        """Get the network capabilities of the base station."""
        pass

    @abstractmethod
    def get_network_interfaces(self):
        """Get the network interfaces of the base station."""
        pass

    @abstractmethod
    def get_network_interface_status(self, interface):
        """Get the network interface status of the base station."""
        pass

    @abstractmethod
    def get_network_interface_statistics(self, interface):
        """Get the network interface statistics of the base station."""
        pass
