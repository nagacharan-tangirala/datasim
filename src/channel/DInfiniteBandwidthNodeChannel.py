from src.channel.BNodeChannel import NodeChannelBase


class InfiniteBandwidthNodeChannel(NodeChannelBase):
    def __init__(self):
        """
        Initialize the infinite bandwidth node channel.
        """
        super().__init__()
