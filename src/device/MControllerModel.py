import pandas as pd
from mesa import Model
from mesa.time import BaseScheduler

from src.channel.BControllerChannel import BaseControllerChannel
from src.device.BController import BaseController
from src.setup.SDeviceModelFactory import DeviceModelFactory


class ControllerModel(Model):
    def __init__(self, controllers: dict[int, BaseController], links: pd.DataFrame, controller_model_data: dict):
        """
        Initialize the controller model.
        """
        super().__init__()

        self.controllers = controllers
        self.connections = links

        # All models are defined here
        self.controller_channel: BaseControllerChannel | None = None

        self.schedule: BaseScheduler = BaseScheduler(self)
        self._create_models(controller_model_data)

    def _create_node_controller_links(self):
        """
        Create the links between the nodes and controllers.
        """
        pass

    def get_agent_channel(self) -> BaseControllerChannel | None:
        """
        Get the channel for the agent model.
        """
        return self.controller_channel

    def _create_models(self, controller_model_data: dict) -> None:
        """
        Create all the models for the controllers.
        """
        # Create the controller channel model
        model_factory = DeviceModelFactory()
        self.controller_channel = model_factory.create_controller_channel(controller_model_data['channel'])

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
