import logging

from numpy import array, ndarray

logger = logging.getLogger(__name__)


class ActivationSettings:
    def __init__(
        self,
        enable_times: ndarray[int],
        disable_times: ndarray[int],
        sim_start_time: int,
        sim_end_time: int,
        is_always_on: bool = False,
    ):
        """
        Initialize the activation settings.
        """
        self.enable_times: ndarray[int] = array([int(x) for x in enable_times])
        self.disable_times: ndarray[int] = array([int(x) for x in disable_times])

        self._sim_start_time: int = sim_start_time
        self._sim_end_time: int = sim_end_time

        self._is_always_on: bool = is_always_on
        self._retain_valid_times()

    def _retain_valid_times(self):
        """
        Retain only valid times.
        """
        # Loop through both enable and disable times
        for i in range(len(self.enable_times)):
            enable_time = self.enable_times[i]
            disable_time = self.disable_times[i]

            if enable_time > disable_time:
                logger.exception(
                    f"Enable time {enable_time} is greater than "
                    f"disable time {disable_time}."
                )

            if enable_time > self._sim_end_time:
                # Remove all the subsequent enable and disable times from the list.
                self.enable_times = self.enable_times[:i]
                self.disable_times = self.disable_times[:i]
                continue

            if disable_time < self._sim_start_time:
                # Remove all the subsequent enable and disable times from the list.
                self.enable_times = self.enable_times[:i]
                self.disable_times = self.disable_times[:i]
                continue

            if disable_time > self._sim_end_time:
                # Set the disable time to the simulation end time.
                self.disable_times[i] = self._sim_end_time

            if enable_time < self._sim_start_time:
                # Set the enable time to the simulation start time.
                self.enable_times[i] = self._sim_start_time

        if len(self.enable_times) == 0:
            if self._is_always_on:
                self.enable_times = array([self._sim_start_time])
                self.disable_times = array([self._sim_end_time])
            else:
                logger.debug("Skipping inactive device.")
