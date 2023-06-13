from src.channel.BControllerChannel import ControllerChannelBase


class InfiniteBandwidthControllerChannel(ControllerChannelBase):
    def __init__(self, channel_id: int):
        """
        Initialize the infinite bandwidth controller channel.
        """
        super().__init__(channel_id)

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
