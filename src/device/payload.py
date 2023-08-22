from dataclasses import dataclass, field


@dataclass
class DataPayload:
    type: str = "Empty"
    count: int = 1
    data_size: float = 0.01


@dataclass
class VehiclePayload:
    source: int = -1
    timestamp: int = -1
    total_data_size: float = 0.01
    data_payload_list: list[DataPayload] = field(default_factory=lambda: [])


@dataclass
class RSUPayload:
    source: int = -1
    timestamp: int = -1
    total_data_size: float = 0.01
    data_payload_list: list[DataPayload] = field(default_factory=lambda: [])


@dataclass
class BaseStationPayload:
    timestamp: int = -1
    uplink_data_size: float = 0.01
    sources: list[int] = field(default_factory=lambda: [])
    uplink_data: list[VehiclePayload] = field(default_factory=lambda: [])


@dataclass
class VehicleResponse:
    timestamp: int = -1
    destination: int = -1
    downlink_data: float = 0.01
    status: bool = False


@dataclass
class RSUResponse:
    timestamp: int = -1
    destination_vehicles: list[int] = field(default_factory=lambda: [])
    downlink_data: list[float] = field(default_factory=lambda: [])
    status: bool = False


@dataclass
class BaseStationResponse:
    destination_vehicles: list[int] = field(default_factory=lambda: [])
    timestamp: int = -1
    downlink_data: list[float] = field(default_factory=lambda: [])
    status: bool = False
