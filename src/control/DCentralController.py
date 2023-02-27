from src.control.BTrafficController import TrafficControllerBase, TrafficControllerType


class CentralController(TrafficControllerBase):
    def __init__(self, params: dict, nodes: dict):
        """
        Initialize the central controller.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the central controller.
        nodes : dict
            Dictionary containing all the nodes for the central controller.
        """
        super().__init__(params, nodes)
        self.type = TrafficControllerType.CENTRAL

    def get_location(self):
        pass
