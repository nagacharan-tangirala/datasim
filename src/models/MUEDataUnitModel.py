from mesa import Model
from mesa.time import BaseScheduler

from src.data_unit.DRegularDataUnit import RegularDataUnit


class UEDataUnitModel(Model):
    def __init__(self, ue_id: int, data_unit_model_data: dict):
        """
        Initialize the data unit model.
        """
        super().__init__()

        self.data_unit = self._create_data_unit(ue_id, data_unit_model_data)
        self.current_time: int = 0
        self.schedule: BaseScheduler = BaseScheduler(self)

    def step(self, *args, **kwargs) -> None:
        """
        Step through the data unit model.
        """
        # Get the current time
        current_time: int = int(args[0])

        # Set the current time and step through the scheduler
        self.data_unit.set_current_time(current_time)
        self.schedule.step()

    def get_generated_data(self) -> int:
        """
        Get the generated data.
        """
        return self.data_unit.get_generated_data()

    def get_cached_data(self) -> int:
        """
        Get the cached data.
        """
        return self.data_unit.get_cached_data()

    def activate(self):
        """
        Activate the model.
        """
        # Override the scheduler and add the data unit to the schedule
        self.schedule = BaseScheduler(self)
        self.schedule.add(self.data_unit)

    def deactivate(self):
        """
        Deactivate the model.
        """
        # Remove the data unit from the schedule
        self.schedule.remove(self.data_unit)

    def _create_data_unit(self, ue_id, data_unit_model_data: dict) -> RegularDataUnit:
        """
        Create a data unit from the given parameters.

        Parameters
        ----------
        data_unit_model_data : dict
            Dictionary containing all the data unit model data.
        """
        # Data source is the ue id
        data_source = [ue_id]

        data_unit_name: str = data_unit_model_data['name']
        match data_unit_name:
            case 'regular':
                return RegularDataUnit(data_unit_model_data['bytes_per_second'], data_source, data_target=None)
            case _:
                raise NotImplementedError('Other data unit models are not supported for UEs.')
