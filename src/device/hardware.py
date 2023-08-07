from src.device.payload import VehiclePayload


class ComputingHardware:
    def __init__(self, hardware_settings: dict):
        """
        Initialize the hardware settings.

        Parameters
        ----------
        hardware_settings : dict
            The hardware settings.
        """
        self._cpu: float = hardware_settings["cpu"]
        self._gpu: float = hardware_settings["gpu"]
        self._memory: float = hardware_settings["memory"]
        self._battery: float = hardware_settings["battery"]
        self._storage: float = hardware_settings["storage"]

        self._cpu_load: float = 0.0
        self._gpu_load: float = 0.0
        self._memory_load: float = 0.0
        self._storage_load: float = 0.0

    @property
    def cpu_load(self) -> float:
        """Get the cpu load."""
        return self._cpu_load

    @property
    def gpu_load(self) -> float:
        """Get the gpu load."""
        return self._gpu_load

    @property
    def memory_load(self) -> float:
        """Get the memory load."""
        return self._memory_load

    def update_consumption(self, payload_request: VehiclePayload) -> None:
        """
        Update the load.
        """
        self._cpu_load = payload_request.cpu_required
        self._gpu_load = payload_request.gpu_required
        self._memory_load = payload_request.memory_required
        self._storage_load = payload_request.storage_required
        self._battery -= payload_request.battery_required

    def reset_consumption(self):
        """
        Reset the load.
        """
        self._cpu_load = 0.0
        self._gpu_load = 0.0
        self._memory_load = 0.0
        self._storage_load = 0.0

    def is_load_feasible(self, payload_request: VehiclePayload) -> bool:
        """
        Check if the new load is feasible to run.
        """
        return (
            self._cpu_load + payload_request.cpu_required <= self._cpu
            and self._gpu_load + payload_request.gpu_required <= self._gpu
            and self._memory_load + payload_request.memory_required <= self._memory
            and self._battery - payload_request.battery_required >= 0.0
            and self._storage_load + payload_request.storage_required <= self._storage
        )


class NetworkHardware:
    def __init__(self, networking_hardware: dict):
        self._capacity: float = networking_hardware["capacity"]
        self._max_connections: int = networking_hardware["max_connections"]

    @property
    def capacity(self) -> float:
        """Get the capacity."""
        return self._capacity

    @property
    def max_connections(self) -> int:
        """Get the max connections."""
        return self._max_connections

    def consume_capacity(self, data_size: float) -> None:
        """
        Send data to the base station.
        """
        self._capacity -= data_size
