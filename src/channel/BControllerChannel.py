from abc import abstractmethod

from mesa import Agent


class ControllerChannelBase(Agent):
    def __init__(self, channel_id: int):
        super().__init__(channel_id, None)

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
