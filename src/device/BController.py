from abc import abstractmethod

from mesa import Agent
from pandas import DataFrame


class Link:
    def __init__(self):
        self.source = None
        self.target = None
        self.bandwidth_in = None
        self.bandwidth_out = None
        self.latency = None


class BaseController(Agent):
    def __init__(self, controller_id: int, position: list[float], controller_models_data: dict, controller_links_data: DataFrame, model=None):
        """
        Initialize the traffic controller.

        Parameters
        ----------
        controller_id : int
            The ID of the traffic controller.
        position : list[float]
            The position of the traffic controller.
        """
        super().__init__(controller_id, model)
        self.position = position

        self.incoming_links: list = []
        self.outgoing_links: list = []

        self.incoming_data = None
        self.outgoing_data = None

        self.controller_models_data = controller_models_data
        self.controller_links_data = controller_links_data

    def get_id(self) -> int:
        """
        Get the ID of the traffic controller.

        Returns
        ----------
        int
            The ID of the traffic controller.
        """
        return self.unique_id

    @abstractmethod
    def initiate_models(self, link_data: DataFrame):
        """
        Initiate the models related to this traffic controller.
        """
        pass

    @abstractmethod
    def get_location(self):
        """
        Get the location of the traffic controller.
        """
        pass
