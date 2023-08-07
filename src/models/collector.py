from src.device.payload import BaseStationPayload


class ControllerCollector:
    def __init__(self):
        """
        Initialize the data collector.
        """
        self._total_data_size: float = 0.0
        self._all_vehicles: list[int] = []

        self._data_types_sizes: dict[str, float] = {}

    @property
    def total_data_size(self) -> float:
        """Get the total data size."""
        return self._total_data_size

    @property
    def all_vehicles(self) -> list[int]:
        """Get the list of all vehicles."""
        return self._all_vehicles

    @property
    def data_types_sizes(self) -> dict[str, float]:
        """Get the data types and their sizes."""
        return self._data_types_sizes

    def collect_data(self, incoming_data: dict[int, BaseStationPayload]):
        """
        Collect the data from the controller.
        """
        # Collect the statistics of the incoming data
        self._total_data_size = 0.0
        self._all_vehicles: list[int] = []
        self._data_types_sizes = {}

        for base_station_id, base_station_payload in incoming_data.items():
            # Calculate total data size and the list of all vehicles
            self._total_data_size += base_station_payload.uplink_data_size
            self._all_vehicles.extend(base_station_payload.sources)

            for vehicle_payload in base_station_payload.uplink_data:
                # Collect the types and their sizes
                for data_payload in vehicle_payload.uplink_payload:
                    data_type = data_payload.type
                    data_size = data_payload.data_size

                    if data_type not in self._data_types_sizes:
                        self._data_types_sizes[data_type] = 0
                    self._data_types_sizes[data_type] += data_size
