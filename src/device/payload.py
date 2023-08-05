from dataclasses import dataclass, field


@dataclass
class DataPayload:
    type: str = ""
    count: int = 0
    data_size: float = 0.0


@dataclass
class VehiclePayload:
    source: int = -1
    timestamp: int = -1
    uplink_data_size: float = 0.0
    uplink_payload: list[DataPayload] = field(default_factory=lambda: [DataPayload()])


@dataclass
class BaseStationPayload:
    timestamp: int = -1
    uplink_data_size: float = 0.0
    sources: list[int] = field(default_factory=lambda: [-1])
    uplink_data: list[VehiclePayload] = field(
        default_factory=lambda: [VehiclePayload()]
    )


@dataclass
class VehicleResponse:
    timestamp: int = -1
    destination: int = -1
    downlink_data: float = -1
    status: bool = False


@dataclass
class BaseStationResponse:
    destination_vehicles: list[int] = field(default_factory=lambda: [-1])
    timestamp: int = -1
    downlink_data: list[float] = field(default_factory=lambda: [0.0])
    status: bool = False
