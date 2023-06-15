from abc import abstractmethod

from mesa import Agent
from pandas import DataFrame

from src.device.BNode import NodeBase


class BaseControllerChannel(Agent):
    def __init__(self, controller_links: DataFrame):
        super().__init__(0, None)

        self.controller_links = controller_links
        self.node_to_controller = {}
        self.nodes: dict = {}

        self.incoming_data: dict = {}

    def assign_nodes(self, nodes: dict[int, NodeBase]) -> None:
        """
        Add a node to the channel.
        """
        # Add the nodes to the channel
        self.nodes = nodes

        # Read the controller links
        self._read_controller_links()

    def _read_controller_links(self) -> None:
        """
        Read the controller links.
        """
        # Based on the controller links, assign nodes to the controller
        for _, row in self.controller_links.iterrows():
            # Get the node ID
            node_id = row['node']

            # Add the node to the controller
            self.node_to_controller[node_id] = row['controller']

    @abstractmethod
    def _collect_from_nodes(self):
        """
        Collect data from the nodes.
        """
        pass

    @abstractmethod
    def _send_to_controller(self):
        """
        Send data to the controller.
        """
        pass

    def step(self) -> None:
        """
        Step through the controller channel.
        """
        # Collect data from the nodes
        self._collect_from_nodes()

        # Send data to the controller
        self._send_to_controller()
