from dataclasses import dataclass, field


@dataclass
class VehiclePayload:
    source: int = -1
    timestamp: int = -1
    cpu_required: float = 0.0
    memory_required: float = 0.0
    gpu_required: float = 0.0
    battery_required: float = 0.0
    storage_required: float = 0.0
    uplink_data: float = 0.0


@dataclass
class BaseStationPayload:
    sources: list[int] = field(default_factory=lambda: [-1])
    timestamp: int = -1
    cpu_required: float = 0.0
    memory_required: float = 0.0
    gpu_required: float = 0.0
    battery_required: float = 0.0
    storage_required: float = 0.0
    uplink_data: list[float] = field(default_factory=lambda: [0.0])


@dataclass
class VehicleResponse:
    destination: int = -1
    timestamp: int = -1
    downlink_data: float = -1
    status: bool = False


@dataclass
class BaseStationResponse:
    destination_vehicles: list[int] = field(default_factory=lambda: [-1])
    timestamp: int = -1
    downlink_data: list[float] = field(default_factory=lambda: [0.0])
    status: bool = False
