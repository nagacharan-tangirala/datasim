from mesa import Model
from mesa.time import BaseScheduler

from src.core.CustomExceptions import DuplicateDeviceFoundError
from src.device.BUE import UEBase


class UEModel(Model):
    def __init__(self, ues: dict[int, UEBase]):
        """
        Initialize the model for the ues.
        """
        # Override the default scheduler
        super().__init__()
        self.schedule: BaseScheduler = BaseScheduler(self)

        self.ues: dict[int, UEBase] = ues
        self.ue_activation_times: dict[int, list[int]] = {}
        self.ue_deactivation_times: dict[int, list[int]] = {}

        self._current_time: int = -1

    @property
    def current_time(self) -> int:
        """Get the current time."""
        return self._current_time
    
    def _prepare_active_ue_times(self) -> None:
        """
        Prepare a dictionary with time step as the key and the respective ues to activate in that time step.
        """
        for ue_id, ue in self.ues.items():
            start_time, end_time = ue.start_time, ue.end_time
            self._save_activation_time(start_time, ue_id)
            self._save_deactivation_time(end_time, ue_id)

    def update_ues(self, ues: dict[int, UEBase]) -> None:
        """
        Update the ues.

        Parameters
        ----------
        ues : dict[int, UEBase]
            The ues to update.
        """
        for ue_id, ue in ues.items():
            if ue_id in self.ues:
                raise DuplicateDeviceFoundError(ue_id, 'ue')
            self.ues[ue_id] = ue

        self._update_active_ue_times()

    def _update_active_ue_times(self) -> None:
        """
        Update the activation and deactivation times for the UEs. This function is called when the UEs are updated.
        """
        for ue_id, ue in self.ues.items():
            start_time, end_time = ue.start_time, ue.end_time

            # If end time is less than the current time, the device is already deactivated
            if end_time < self.current_time:
                continue

            if start_time > self.current_time:
                # If start time is greater than the current time, the device is not activated yet. Add the activation time and deactivation time.
                self._save_activation_time(start_time, ue_id)
                self._save_deactivation_time(end_time, ue_id)
            else:
                # The device is already activated. Remove the current deactivation time and add the new one.
                if self.current_time in self.ue_deactivation_times:
                    self.ue_deactivation_times[end_time].pop(ue_id)
                self._save_deactivation_time(end_time, ue_id)

    def _save_activation_time(self, time: int, ue_id: int):
        """
        Update the activation time of the ue.
        """
        if time not in self.ue_activation_times:
            self.ue_activation_times[time] = [ue_id]
        else:
            self.ue_activation_times[time].append(ue_id)

    def _save_deactivation_time(self, time: int, ue_id: int):
        """
        Update the deactivation time of the ue.
        """
        if time not in self.ue_deactivation_times:
            self.ue_deactivation_times[time] = [ue_id]
        else:
            self.ue_deactivation_times[time].append(ue_id)

    def _refresh_active_ues(self, time_step: int) -> None:
        """
        If the start or end time of an ue is equal to the current time step, activate or deactivate the ue.

        Parameters
        ----------
        time_step : int
            The time step of the simulation.
        """
        if len(self.ue_activation_times) == 0:
            self._prepare_active_ue_times()

        self._activate_ues(time_step)
        self._deactivate_ues(time_step)

    def _activate_ues(self, time_step: int) -> None:
        """
        Activate the ues in the current time step.
        """
        ues_to_activate = self.ue_activation_times[time_step]
        for ue_id in ues_to_activate:
            ue = self.ues[ue_id]
            ue.activate_ue(time_step)

            # Add to the schedule and channel and set the mesa model to this
            self.schedule.add(ue)
            self.ue_channel.add_ue(ue)
            ue.sim_model = self

    def _deactivate_ues(self, time_step: int) -> None:
        """
        Deactivate the ues in the current time step.
        """
        ues_to_deactivate = self.ue_deactivation_times[time_step]
        for ue_id in ues_to_deactivate:
            ue = self.ues[ue_id]
            ue.deactivate_ue(time_step)

            # Remove from the schedule and channel and set the mesa model to None
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
