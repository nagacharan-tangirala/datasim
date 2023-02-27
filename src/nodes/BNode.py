from abc import ABCMeta, abstractmethod
from enum import Enum


class NodeType(Enum):
    """Enum for node types."""

    BASE_STATION = 'base_station'
    INTERMEDIATE = 'intermediate'


class NodeBase(metaclass=ABCMeta):
    """Base class for all node classes."""

    def __init__(self, params: dict):
        """
        Initialize the node class.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the node.
        """
        self.node_id = params.get('id', None)
        self.location = params.get('location', None)

        self.type: NodeType = NodeType.BASE_STATION

    def get_id(self) -> int:
        """
        Get the ID of the node.

        Returns
        ----------
        int
            The ID of the ndoe.
        """
        return self.node_id

    def get_location(self) -> list[float]:
        """
        Get the location of the node.

        Returns
        ----------
        tuple
            Tuple containing the x and y coordinates of the node.
        """
        return self.location

    def get_type(self) -> str:
        """
        Get the type of the node.

        Returns
        ----------
        str
            The type of the node as a string.
        """
        return self.type.value

    @abstractmethod
    def process_node(self, time: int):
        """
        Update the node.

        Parameters
        ----------
        time : int
            The current time.
        """
        pass

    @abstractmethod
    def get_collected_data_size(self, time: int) -> int:
        """
        Get the collected data size.

        Parameters
        ----------
        time : int
            The current time.

        Returns
        ----------
        int
            The collected data size.
        """
        pass
