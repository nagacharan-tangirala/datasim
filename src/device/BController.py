from abc import abstractmethod

import pandas as pd
from mesa import Agent


class Link:
    def __init__(self):
        self.source = None
        self.target = None
        self.bandwidth_in = None
        self.bandwidth_out = None
        self.latency = None


class BaseController(Agent):
    def __init__(self, controller_id: int, position: list[float], model=None):
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
    def initiate_models(self, link_data: pd.DataFrame):
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
