from abc import ABCMeta, abstractmethod
from enum import Enum


class TrafficControllerStatus(Enum):
    """Enum for traffic controller status."""

    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class TrafficControllerType(Enum):
    """Enum for traffic controller types."""

    CENTRAL = 'CENTRAL'
    BACKUP = 'BACKUP'


class TrafficControllerBase(metaclass=ABCMeta):
    """Base class for all traffic controllerler classes."""

    @abstractmethod
    def __init__(self, params: dict, nodes: dict):
        """
        Initialize the traffic controller.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the traffic controller.
        nodes : dict
            Dictionary containing all the nodes for the traffic controller.
        """
        self.controller_id = params.get('id', None)
        self.nodes = nodes

        self.status = None
        self.type = None

    def get_id(self) -> int:
        """
        Get the ID of the traffic controllerler.

        Returns
        ----------
        int
            The ID of the traffic controllerler.
        """
        return self.controller_id

    def get_type(self) -> str:
        """
        Get the type of the traffic controller.

        Returns
        ----------
        str
            The type of the traffic controller as a string.
        """
        return self.type.value

    def get_status(self) -> str:
        """
        Get the status of the traffic controller.

        Returns
        ----------
        str
            The status of the traffic controller as a string.
        """
        return self.status.value

    @abstractmethod
    def get_location(self):
        """Get the location of the traffic controller."""
        pass
