from src.channel.DInfiniteBandwidthAgentChannel import InfiniteBandwidthAgentChannel


class ChannelFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_agent_channel(type: str):
        """
        Create an agent channel of the given type.
        """
        if type == 'infinite_bandwidth':
            return InfiniteBandwidthAgentChannel()
        else:
            raise ValueError("Agent channel type {} not supported.".format(type))

    @staticmethod
    def create_node_channel(type: str):
        """
        Create a node channel of the given type.
        """
        if type == 'infinite_bandwidth':
            return InfiniteBandwidthNodeChannel()
        else:
            raise ValueError("Node channel type {} not supported.".format(type))
