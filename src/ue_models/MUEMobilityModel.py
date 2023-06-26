from mesa import Model
from mesa.time import BaseScheduler
from pandas import DataFrame

from src.ue_models.BUEMobility import UEMobilityBase
from src.ue_models.DStaticUEMobility import StaticUEMobility
from src.ue_models.DTraceUEMobility import TraceUEMobility


class UEMobilityModel(Model):
    def __init__(self, mobility_model_data: dict):
        """
        Initialize the mobility model.
        """
        super().__init__()

        self.mobility: UEMobilityBase = self._create_mobility(mobility_model_data)

    def step(self, *args, **kwargs):
        """
        Step function for the model.
        """
        # Get current time
        current_time: int = int(args[0])

        # Set the current time and step through the scheduler
        self.mobility.current_time = current_time
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

    def get_location(self) -> list[float]:
        """
        Get the current location of the ue.
        """
        return self.mobility.current_location

    def update_data(self, positions: DataFrame) -> None:
        """
        Update the mobility model.
        """
        self.mobility.update_positions(positions)

    def get_start_and_end_time(self) -> tuple[int, int]:
        """
        Get the start and end time of the mobility model.

        Returns
        -------
        tuple[int, int]
            The start and end time of the mobility model.
        """
        return self.mobility.get_start_and_end_time()

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
                return StaticUEMobility(mobility_model_data['trace'])
            case 'trace':
                return TraceUEMobility(mobility_model_data['trace'])
            case _:
                raise NotImplementedError("Other mobility types are not implemented.")
