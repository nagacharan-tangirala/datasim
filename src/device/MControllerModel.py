import pandas as pd
from mesa import Model
from mesa.time import BaseScheduler

from src.channel.BControllerChannel import ControllerChannelBase
from src.device.BTrafficController import TrafficControllerBase
from src.setup.SDeviceModelFactory import DeviceModelFactory


class ControllerModel(Model):
    def __init__(self, controllers: dict[int, TrafficControllerBase], links: pd.DataFrame, controller_model_data: dict):
        """
        Initialize the controller model.
        """
        super().__init__()

        self.controllers = controllers
        self.connections = links

        # All models are defined here
        self.controller_channel: ControllerChannelBase | None = None

        self.schedule: BaseScheduler = BaseScheduler(self)
        self._create_models(controller_model_data)

    def _create_node_controller_links(self):
        """
        Create the links between the nodes and controllers.
        """
        pass

    def get_controller_channel(self) -> ControllerChannelBase:
        """
        Get the controller channel.
        """
        return self.controller_channel

    def _create_models(self, controller_model_data: dict) -> None:
        """
        Create all the models for the controllers.
        """
        # Iterate through the models and create them
        model_factory = DeviceModelFactory()
        for model_id, model_data in controller_model_data.items():
            if model_data['type'] == 'channel':
                self.controller_channel = model_factory.create_controller_channel(model_data)
            else:
                raise ValueError(f"Unknown model type {model_data['type']}")

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
