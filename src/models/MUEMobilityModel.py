from mesa import Model
from mesa.time import BaseScheduler
from pandas import DataFrame

from src.setup.SDeviceModelFactory import DeviceModelFactory


class MobilityModel(Model):
    def __init__(self, positions: DataFrame):
        """
        Initialize the mobility model.
        """
        super().__init__()
        self.positions: DataFrame = positions
        self.mobility = None

    def step(self, *args, **kwargs):
        """
        Step function for the model.
        """
        self.schedule.step()

    def activate(self):
        """
        Activate the model.
        """
        # Override the scheduler
        self.schedule = BaseScheduler(self)

        # Create mobility factory and the mobility model
        model_factory = DeviceModelFactory()
        self.mobility = model_factory.create_mobility(self.positions)

        # Add the mobility model to the schedule
        self.schedule.add(self.mobility)

    def deactivate(self):
        """
        Deactivate the model by removing the mobility model from the schedule.
        """
        self.schedule.remove(self.mobility)

    def get_location(self) -> list[float]:
        """
        Get the current location of the ue.
        """
        return self.mobility.get_current_location()
