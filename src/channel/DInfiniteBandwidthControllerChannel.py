from src.channel.BControllerChannel import BaseControllerChannel


class InfiniteBandwidthControllerChannel(BaseControllerChannel):
    def __init__(self):
        """
        Initialize the infinite bandwidth controller channel.
        """
        super().__init__(0, None)

    def _collect_from_nodes(self):
        """
        Collect data from the nodes.
        """
        pass

    def _send_to_controller(self):
        """
        Send data to the controller.
        """
        pass
