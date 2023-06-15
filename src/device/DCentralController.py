import pandas as pd

from src.device.BController import BaseController


class CentralController(BaseController):
    def __init__(self, controller_id, position):
        """
        Initialize the central controller.

        Parameters
        ----------
        controller_id : int
            The ID of the controller.
        position : list[float]
            The position of the controller.
        """
        super().__init__(controller_id, position)

    def get_location(self):
        """
        Get the location of the traffic controller.
        """
        return self.position

    def initiate_models(self, link_data: pd.DataFrame):
        """
        Initiate the models related to this traffic controller.
        """
        # Retain only the links that are connected to this controller.
        this_controller_links = link_data[link_data['controller'] == self.unique_id]

        # Make sure that the controller is linked.
        if len(this_controller_links) == 0:
            raise ValueError(f'Controller {self.unique_id} is not in the link data.')
