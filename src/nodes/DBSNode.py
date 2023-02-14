from src.nodes.BNode import NodeBase


class BaseStation(NodeBase):
    def __init__(self, params: dict):
        """
        Initialize the base station.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the base station.
        """
        super().__init__(params)
        self._initiate_sensors(params.get('sensor_dict', None))