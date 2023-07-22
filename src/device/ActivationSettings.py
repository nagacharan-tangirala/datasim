class ActivationSettings:
    def __init__(self, activate_times: list[int], disable_times: list[int], active: bool = False):
        """
        Initialize the activation settings.
        """
        self._activate_times: list[int] = activate_times
        self._disable_times: list[int] = disable_times
        self._index: int = 0
        self._active = active

    @property
    def start_time(self) -> int:
        """ Get the start time. """
        return self._activate_times[self._index]

    @property
    def end_time(self) -> int:
        """ Get the end time. """
        return self._disable_times[self._index]

    @property
    def active(self) -> bool:
        """ Get the active state. """
        return self._active

    @active.setter
    def active(self, active: bool) -> None:
        """ Set the active state. """
        self._active = active
        # Increment the index if the device is deactivated
        if not active:
            self._index += 1
