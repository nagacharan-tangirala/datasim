class NetworkingHardware:
    def __init__(self, capacity: float, max_connections: int):
        self._capacity: float = capacity
        self._max_connections: int = max_connections

    @property
    def capacity(self) -> float:
        """ Get the capacity. """
        return self._capacity

    @property
    def max_connections(self) -> int:
        """ Get the max connections. """
        return self._max_connections

    def consume_capacity(self, data_size: float) -> None:
        """
        Send data to the base station.
        """
        self._capacity -= data_size
