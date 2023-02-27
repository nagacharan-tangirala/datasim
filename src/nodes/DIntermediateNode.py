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

        self.in_range_nodes = []
        self.nodes_data = 0

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
        return self.nodes_data

    def process_node(self, time: int):
        """
        Update the node. This includes collecting data from all the entities which are in range.

        Parameters
        ----------
        time : int
            The current time.
        """
        # Get the data collected by the nodes associated with the intermediate node.
        self.nodes_data = 0
        for node in self.in_range_nodes:
            self.nodes_data = self.nodes_data + node.get_collected_data_size(time)
