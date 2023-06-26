from mesa import Model
from mesa.time import BaseScheduler

from src.data.UEDataHandler import UEDataHandler
from src.device.BUE import UEData


class UEDataHandlerModel(Model):
    def __init__(self, ue_id: int, data_unit_model_data: dict):
        """
        Initialize the data handler model.
        """
        super().__init__()

        self._ue_id: int = ue_id
        self.current_time: int = 0
        self.schedule: BaseScheduler = BaseScheduler(self)

        self.ue_data_handler = self._create_data_unit(data_unit_model_data)
        self._data_to_send: int = -1

    @property
    def data_to_send(self) -> int:
        """ Get the data to send. """
        return self._data_to_send

    def step(self, *args, **kwargs) -> None:
        """
        Step through the data handler model.
        """
        # Get the current time
        current_time: int = int(args[0])

        # Set the current time and step through the scheduler
        self.ue_data_handler.time_stamp = current_time
        self.schedule.step()
        self._data_to_send = self.ue_data_handler.data_to_send

    def get_generated_data(self) -> UEData:
        """
        Get the generated data.
        """
        return self.ue_data_handler.data_to_send

    def get_cached_data(self) -> UEData:
        """
        Get the cached data.
        """
        return self.ue_data_handler.data_cache

    def activate(self):
        """
        Activate the model.
        """
        # Override the scheduler and add the data handler to the schedule
        self.schedule = BaseScheduler(self)
        self.schedule.add(self.ue_data_handler)

    def deactivate(self):
        """
        Deactivate the model.
        """
        # Remove the data handler from the schedule
        self.schedule.remove(self.ue_data_handler)

    def _create_data_unit(self, data_unit_model_data: dict) -> UEDataHandler:
        """
        Create a data handler from the given parameters.

        Parameters
        ----------
        data_unit_model_data : dict
            Dictionary containing all the data handler model data.
        """
        # Data source is the ue id
        data_source = self._ue_id

        data_unit_name: str = data_unit_model_data['name']
        match data_unit_name:
            case 'basic':
                return UEDataHandler(data_source, data_unit_model_data)
            case _:
                raise NotImplementedError('Other data unit models are not supported for UEs.')
