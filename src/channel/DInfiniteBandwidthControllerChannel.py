from src.channel.BControllerChannel import BaseControllerChannel


class InfiniteBandwidthControllerChannel(BaseControllerChannel):
    def __init__(self):
        """
        Initialize the infinite bandwidth controller channel.
        """
        super().__init__(controller_links)

    def _collect_from_nodes(self):
        """
        Collect data from the nodes.
        """
        # Collect data from the nodes
        for node_id, node in self.nodes.items():
            self.incoming_data[node_id] = node.get_incoming_data()

    def _send_to_controller(self):
        """
        Send data to the controller.
        """
        # Send data to the controller
