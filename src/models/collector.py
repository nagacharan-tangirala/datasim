from src.device.payload import BaseStationPayload, VehiclePayload


class ControllerCollector:
    def __init__(self):
        """
        Initialize the data collector.
        """
        self._total_data_size: float = 0.0
        self._all_vehicles: list[int] = []

        self._data_sizes_by_type: dict[str, float] = {}
        self._data_counts_by_type: dict[str, int] = {}

    @property
    def total_data_size(self) -> float:
        """Get the total data size."""
        return self._total_data_size

    @property
    def all_vehicles(self) -> list[int]:
        """Get the list of all vehicles."""
        return self._all_vehicles

    @property
    def data_sizes_by_type(self) -> dict[str, float]:
        """Get the data types and their sizes."""
        return self._data_sizes_by_type

    @property
    def data_counts_by_type(self) -> dict[str, int]:
        """Get the data types and their counts."""
        return self._data_counts_by_type

    def collect_data(self, incoming_data: dict[int, BaseStationPayload]):
        """
        Collect the data from the controller.
        """
        # Collect the statistics of the incoming data
        self._total_data_size = 0.0
        self._all_vehicles: list[int] = []

        self._data_sizes_by_type = {}
        self._data_counts_by_type = {}
        for base_station_payload in incoming_data.values():
            # Calculate total data size and the list of all vehicles
            self._total_data_size += base_station_payload.uplink_data_size
            self._all_vehicles.extend(base_station_payload.sources)

            for vehicle_payload in base_station_payload.uplink_data:
                # Collect the types and their sizes
                for data_payload in vehicle_payload.data_payload_list:
                    data_type = data_payload.type

                    # Store data size by type
                    data_size = data_payload.data_size
                    if data_type not in self._data_sizes_by_type:
                        self._data_sizes_by_type[data_type] = 0
                    self._data_sizes_by_type[data_type] += data_size

                    # Store data count by type
                    data_count: int = data_payload.count
                    if data_type not in self._data_counts_by_type:
                        self._data_counts_by_type[data_type] = 0
                    self._data_counts_by_type[data_type] += data_count


class VehicleCollector:
    def __init__(self):
        """
        Initialize the data collector.
        """
        self._total_data_size: float = 0.0
        self._data_sizes_by_type: dict[str, float] = {}
        self._data_counts_by_type: dict[str, int] = {}

    @property
    def total_data_size(self) -> float:
        """Get the total data size."""
        return self._total_data_size

    @property
    def data_sizes_by_type(self) -> dict[str, float]:
        """Get the data types and their sizes."""
        return self._data_sizes_by_type

    @property
    def data_counts_by_type(self) -> dict[str, int]:
        """Get the data types and their counts."""
        return self._data_counts_by_type

    def collect_data(self, incoming_data: dict[int, VehiclePayload]):
        """
        Collect the data from the vehicle.
        """
        # Collect the statistics of the incoming data
        self._total_data_size = 0.0
        self._data_sizes_by_type = {}
        self._data_counts_by_type = {}
        for vehicle_payload in incoming_data.values():
            # Calculate total data size and the list of all vehicles
            self._total_data_size += vehicle_payload.total_data_size

            for data_payload in vehicle_payload.data_payload_list:
                data_type = data_payload.type

                # Store data size by type
                data_size = data_payload.data_size
                if data_type not in self._data_sizes_by_type:
                    self._data_sizes_by_type[data_type] = 0
                self._data_sizes_by_type[data_type] += data_size

                # Store data count by type
                data_count: int = data_payload.count
                if data_type not in self._data_counts_by_type:
                    self._data_counts_by_type[data_type] = 0
                self._data_counts_by_type[data_type] += data_count


class RSUCollector:
    def __init__(self):
        """
        Initialize the data collector.
        """
        self._total_data_size: float = 0.0
        self._data_sizes_by_type: dict[str, float] = {}
        self._data_counts_by_type: dict[str, int] = {}

    @property
    def total_data_size(self) -> float:
        """Get the total data size."""
        return self._total_data_size

    @property
    def data_sizes_by_type(self) -> dict[str, float]:
        """Get the data types and their sizes."""
        return self._data_sizes_by_type

    @property
    def data_counts_by_type(self) -> dict[str, int]:
        """Get the data types and their counts."""
        return self._data_counts_by_type

    def collect_data(self, incoming_data: dict[int, VehiclePayload]):
        """
        Collect the data from the vehicle.
        """
        # Collect the statistics of the incoming data
        self._total_data_size = 0.0
        self._data_sizes_by_type = {}
        self._data_counts_by_type = {}
        for vehicle_payload in incoming_data.values():
            # Calculate total data size and the list of all vehicles
            self._total_data_size += vehicle_payload.total_data_size

            for data_payload in vehicle_payload.data_payload_list:
                data_type = data_payload.type

                # Store data size by type
                data_size = data_payload.data_size
                if data_type not in self._data_sizes_by_type:
                    self._data_sizes_by_type[data_type] = 0
                self._data_sizes_by_type[data_type] += data_size

                # Store data count by type
                data_count: int = data_payload.count
                if data_type not in self._data_counts_by_type:
                    self._data_counts_by_type[data_type] = 0
                self._data_counts_by_type[data_type] += data_count
