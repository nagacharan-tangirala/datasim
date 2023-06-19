from mesa import Model
from mesa.time import BaseScheduler

from src.channel.BUEChannel import BaseUEChannel
from src.device.BUE import BaseUE
from src.setup.SDeviceModelFactory import DeviceModelFactory


class UEModel(Model):
    def __init__(self, ues: dict[int, BaseUE], ue_model_data: dict):
        """
        Initialize the model for the ues.
        """
        # Override the default scheduler
        super().__init__()
        self.schedule: BaseScheduler = BaseScheduler(self)

        self.ues: dict[int, BaseUE] = ues
        self.ue_activation_times: dict[int, list[int]] = {}

        self.current_time: int = 0

        # All models are defined here
        self.ue_channel: BaseUEChannel | None = None
        self.data_model: dict[int, float] = {}

        self._prepare_active_ues_dict()
        self._create_models(ue_model_data)

    def _prepare_active_ues_dict(self) -> None:
        """
        Prepare a dictionary with time step as the key and the respective ues to activate in that time step.
        """
        for ue_id, ue in self.ues.items():
            start_time, end_time = ue.get_start_and_end_time()
            # Add the ue to the dictionary with the start time as the key
            if start_time not in self.ue_activation_times:
                self.ue_activation_times[start_time] = [ue_id]
            else:
                self.ue_activation_times[start_time].append(ue_id)

            # Add the ue to the dictionary with the end time as the key
            if end_time not in self.ue_activation_times:
                self.ue_activation_times[end_time] = [ue_id]
            else:
                self.ue_activation_times[end_time].append(ue_id)

    def _create_models(self, ue_model_data: dict) -> None:
        """
        Create all the models for the ues.
        """
        # Iterate through the model data and create the models
        model_factory = DeviceModelFactory()
        for model_id, model_data in ue_model_data.items():
            if model_data['type'] == 'channel':
                self.ue_channel = model_factory.create_ue_channel(model_data)
            else:
                raise ValueError(f"Unknown model type {model_data['type']}")

    def get_ue_channel(self) -> BaseUEChannel | None:
        """
        Get the channel for the ue model.
        """
        return self.ue_channel

    def _refresh_active_ues(self, time_step: int) -> None:
        """
        If the start or end time of an ue is equal to the current time step, activate or deactivate the ue.

        Parameters
        ----------
        time_step : int
            The time step of the simulation.
        """
        ues_to_update = self.ue_activation_times[time_step]
        for ue_id in ues_to_update:
            ue = self.ues[ue_id]
            ue.toggle_status()

            # If the ue is active, add it to the scheduler and channel. Otherwise, remove from them.
            if ue.is_active():
                self.schedule.add(ue)
                self.ue_channel.add_ue(ue)
                ue.sim_model = self
            else:
                self.schedule.remove(ue)
                self.ue_channel.remove_ue(ue)
                ue.sim_model = None

    def step(self, *args, **kwargs):
        """
        Step function for the model.
        """
        # Refresh the active ues
        current_time = int(args[0])
        if current_time in self.ue_activation_times:
            self._refresh_active_ues(current_time)

        # Step through the schedule object
        self.schedule.step()
