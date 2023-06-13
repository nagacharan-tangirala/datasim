import pandas as pd
from mesa import Model
from mesa.time import BaseScheduler

from src.channel.BControllerChannel import ControllerChannelBase
from src.device.BTrafficController import TrafficControllerBase


class ControllerModel(Model):
    def __init__(self, controllers: dict[int, TrafficControllerBase], links: pd.DataFrame):
        """
        Initialize the controller model.
        """
        super().__init__()

        self.controllers = controllers
        self.connections = links

        self.controller_channel: ControllerChannelBase | None = None
        self.schedule: BaseScheduler = BaseScheduler(self)

    def _create_node_controller_links(self):
        """
        Create the links between the nodes and controllers.
        """

    def step(self) -> None:
        """
        Step function for the model. This function is called every time step.
        """
        # Step the scheduler
        self.schedule.step()

    def _initiate_models(self):
        """
        Initiate the controllers and add them to the scheduler.
        """
        for controller_id, controller in self.controllers.items():
            self.schedule.add(controller)
