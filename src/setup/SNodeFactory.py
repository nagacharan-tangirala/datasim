from src.nodes.DBaseStationNode import BaseStation
from src.nodes.DIntermediateNode import IntermediateNode


class NodeFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_node(params):
        """
        Create a node from the given parameters.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the node.
        """
        node_type = params.get('type', None)
        if node_type == 'bs':
            return BaseStation(params)
        elif node_type == 'intermediate':
            return IntermediateNode(params)
        else:
            raise ValueError("Node type not supported.")
