from abc import abstractmethod

from mesa import Agent


class ControllerChannelBase(Agent):
    def __init__(self):
        super().__init__(0, None)

    @abstractmethod
    def _collect_from_nodes(self):
        """
        Collect data from the nodes.
        """
        pass

    @abstractmethod
    def _send_to_controller(self):
        """
        Send data to the controller.
        """
        pass
