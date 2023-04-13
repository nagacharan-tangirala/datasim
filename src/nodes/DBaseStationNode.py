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

        self.entities_data = 0
        self.in_range_entities = []

    def get_statistics(self):
        pass

    def update_node(self, time: int):
        """
        Update the node. This includes collecting data from all the entities which are in range.

        Parameters
        ----------
        time : int
            The current time.
        """
        # Get the data collected by the entities.
        self.entities_data = 0
        for entity in self.in_range_entities:
            self.entities_data = self.entities_data + entity.get_collected_data_size(time)

    def get_collected_data_size(self) -> int:
        """
        Get the collected data size.

        Returns
        ----------
        int
            The collected data size.
        """
        return self.entities_data
