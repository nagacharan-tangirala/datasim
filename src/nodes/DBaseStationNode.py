from src.nodes.BNode import NodeBase, NodeType


class BaseStation(NodeBase):
    """
    Base station class designed to mimic the behavior of base stations.
    """
    def __init__(self, params: dict):
        """
        Initialize the base station.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the base station.
        """
        super().__init__(params)
        self.type = NodeType.BASE_STATION

    def get_statistics(self):
        pass
