from abc import ABCMeta, abstractmethod


class TrafficControlBase(metaclass=ABCMeta):
    """Base class for all traffic control classes."""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """Initialize the traffic control."""
        pass

    @abstractmethod
    def run(self):
        """Run the traffic control."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the traffic control."""
        pass

    @abstractmethod
    def get_status(self):
        """Get the status of the traffic control."""
        pass

    @abstractmethod
    def get_statistics(self):
        """Get the statistics of the traffic control."""
        pass

    @abstractmethod
    def get_version(self):
        """Get the version of the traffic control."""
        pass

    @abstractmethod
    def get_id(self):
        """Get the ID of the traffic control."""
        pass

    @abstractmethod
    def get_name(self):
        """Get the name of the traffic control."""
        pass

    @abstractmethod
    def get_location(self):
        """Get the location of the traffic control."""
        pass

    @abstractmethod
    def get_type(self):
        """Get the type of the traffic control."""
        pass

    @abstractmethod
    def get_description(self):
        """Get the description of the traffic control."""
        pass
