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
