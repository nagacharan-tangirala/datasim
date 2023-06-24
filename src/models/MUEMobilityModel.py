from mesa import Model
from mesa.time import BaseScheduler
from pandas import DataFrame

from src.models.DStaticUEMobility import StaticUEMobility
from src.models.DTraceUEMobility import TraceUEMobility


class UEMobilityModel(Model):
    def __init__(self, mobility_model_data: dict):
        """
        Initialize the mobility model.
        """
        super().__init__()

        self.mobility = self._create_mobility(mobility_model_data)

    def step(self, *args, **kwargs):
        """
        Step function for the model.
        """
        # Get current time
        current_time: int = int(args[0])

        # Set the current time and step through the scheduler
        self.mobility.set_current_time(current_time)
        self.schedule.step()

    def activate(self):
        """
        Activate the model.
        """
        # Override the scheduler and add the mobility model to the schedule
        self.schedule = BaseScheduler(self)
        self.schedule.add(self.mobility)

    def deactivate(self):
        """
        Deactivate the model by removing the mobility model from the schedule.
        """
        self.schedule.remove(self.mobility)

    def update_mobility_data(self, mobility_data: DataFrame) -> None:
        """
        Update the mobility data.
        """
        if self.mobility.get_type() == 'trace':
            self.mobility.update_positions(mobility_data)

    def get_location(self) -> list[float]:
        """
        Get the current location of the ue.
        """
        return self.mobility.get_current_location()

    def _create_mobility(self, mobility_model_data: dict) -> StaticUEMobility | TraceUEMobility:
        """
        Create a mobility model from the given parameters.

        Parameters
        ----------
        mobility_model_data : dict
            Dictionary containing all the mobility model data.
        """
        model_name = mobility_model_data['name']
        match model_name:
            case 'static':
                return StaticUEMobility(mobility_model_data['positions'])
            case 'trace':
                return TraceUEMobility()
            case _:
                raise NotImplementedError("Other mobility types are not implemented.")
