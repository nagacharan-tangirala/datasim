class ApplicationSettings:
    def __init__(self, app_settings: dict):
        """
        Initialize the application settings.
        """
        self._type: str = app_settings["type"]
        self._priority: int = app_settings["priority"]

        self._cpu_required: float = app_settings["cpu_required"]
        self._memory_required: float = app_settings["memory_required"]
        self._gpu_required: float = app_settings["gpu_required"]
        self._battery_required: float = app_settings["battery_required"]
        self._storage_required: float = app_settings["storage_required"]

        self._uplink_required: float = app_settings["uplink_required"]
        self._downlink_required: float = app_settings["downlink_required"]

    @property
    def type(self) -> str:
        """ Get the type. """
        return self._type

    @property
    def cpu_required(self) -> float:
        """ Get the cpu usage. """
        return self._cpu_required

    @property
    def memory_required(self) -> float:
        """ Get the memory usage. """
        return self._memory_required

    @property
    def gpu_required(self) -> float:
        """ Get the gpu usage. """
        return self._gpu_required

    @property
    def battery_required(self) -> float:
        """ Get the battery usage. """
        return self._battery_required

    @property
    def storage_required(self) -> float:
        """ Get the storage usage. """
        return self._storage_required

    @property
    def uplink_data(self) -> float:
        """ Get the uplink data. """
        return self._uplink_required

    def is_active(self, current_time) -> bool:
        """ Get the active status. """
        return True
