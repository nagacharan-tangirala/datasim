from mesa import Model
from mesa.time import BaseScheduler
from pandas import DataFrame

from src.models.BTowerFinder import TowerFinderBase
from src.setup.SDeviceModelFactory import DeviceModelFactory


class TowerFinderModel(Model):
    def __init__(self, nearest_towers_df: DataFrame):
        """
        Initialize the tower finder.
        """
        super().__init__()

        self.nearest_towers_df: DataFrame = nearest_towers_df
        self.tower_finder: TowerFinderBase | None = None

        self.current_time: int = 0
        self.nearest_tower: int = -1

    def step(self, *args, **kwargs):
        """
        Step function for the model.
        """
        # Get the time step from args
        current_time = int(args[0])
        self.tower_finder.set_current_time(current_time)

        # Step through the coverage model
        self.schedule.step()

    def activate(self):
        """
        Activate the model.
        """
        # Override the scheduler
        self.schedule = BaseScheduler(self)

        # Create model factory and the tower finder model
        model_factory = DeviceModelFactory()
        self.tower_finder = model_factory.create_tower_finder(self.nearest_towers_df)

        # Add the tower finder to the schedule
        self.schedule.add(self.tower_finder)

    def deactivate(self):
        """
        Deactivate the model by removing the tower finder model from the schedule.
        """
        self.schedule.remove(self.tower_finder)

    def get_nearest_tower(self) -> int:
        """
        Get the nearest tower to the ue.
        """
        return self.tower_finder.get_nearest_tower()
