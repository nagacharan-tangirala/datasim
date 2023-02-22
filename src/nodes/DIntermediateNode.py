from src.nodes.BNode import NodeBase, NodeType


class IntermediateNode(NodeBase):
    def __init__(self, params: dict):
        """
        Initialize the intermediate node.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the intermediate node.
        """
        super().__init__(params)
        self.type = NodeType.INTERMEDIATE

    def get_statistics(self):
        pass
