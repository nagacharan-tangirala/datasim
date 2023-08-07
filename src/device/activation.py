from numpy import ndarray


class ActivationSettings:
    def __init__(
        self, activate_times: ndarray, disable_times: ndarray, active: bool = False
    ):
        """
        Initialize the activation settings.
        """
        self._activate_times: ndarray[int] = [int(x) for x in activate_times]
        self._disable_times: ndarray[int] = [int(x) for x in disable_times]
        self._index: int = 0
        self._active = active

    @property
    def start_time(self) -> int:
        """Get the start time."""
        if self._index >= len(self._activate_times):
            return 0
        return self._activate_times[self._index]

    @property
    def end_time(self) -> int:
        """Get the end time."""
        if self._index >= len(self._activate_times):
            # Return a very large number to ensure that the device is never deactivated
            return 100000000
        return self._disable_times[self._index]

    @property
    def active(self) -> bool:
        """Get the active state."""
        return self._active

    @active.setter
    def active(self, active: bool) -> None:
        """Set the active state."""
        self._active = active
        # Increment the index if the device is deactivated
        if not active:
            self._index += 1
