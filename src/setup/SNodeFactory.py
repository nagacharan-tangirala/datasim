import pandas as pd

from src.device.DBaseStationNode import BaseStation
from src.device.DIntermediateNode import IntermediateNode


class NodeFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_node(node_id, node_data: pd.Series):
        """
        Create a node from the given parameters.

        Parameters
        ----------
        node_data : pd.Series
            Series containing all the parameters for the node.
        """
        node_type = node_data['type']
        if node_type == 'bs':
            return BaseStation(node_id, node_data)
        elif node_type == 'intermediate':
            return IntermediateNode(node_id, node_data)
        else:
            raise ValueError("Node {} type not supported.".format(node_type))
