from enum import Enum, StrEnum
from typing import final


class FilenameKey(StrEnum):
    """
    Enum for the input file names.
    """

    VEHICLE_TRACE: final(str) = "vehicle_traces"
    BASE_STATIONS: final(str) = "base_stations"
    CONTROLLERS: final(str) = "controllers"
    ROADSIDE_UNITS: final(str) = "roadside_units"

    V2V_LINKS: final(str) = "v2v_links"
    V2B_LINKS: final(str) = "v2b_links"
    V2R_LINKS: final(str) = "v2r_links"
    B2C_LINKS: final(str) = "b2c_links"
    R2B_LINKS: final(str) = "r2b_links"
    R2R_LINKS: final(str) = "r2r_links"

    VEHICLE_ACTIVATIONS: final(str) = "vehicle_activations"
    CONTROLLER_ACTIVATIONS: final(str) = "controller_activations"
    BASE_STATION_ACTIVATIONS: final(str) = "base_station_activations"
    RSU_ACTIVATIONS: final(str) = "rsu_activations"

    DATA_SOURCE_CONFIG: final(str) = "data_source_config"


class DeviceName(StrEnum):
    """
    Enum for the names of the devices in the simulation.
    """

    VEHICLES: final(str) = "vehicles"
    BASE_STATIONS: final(str) = "base_stations"
    CONTROLLERS: final(str) = "controllers"
    ROADSIDE_UNITS: final(str) = "roadside_units"
    EDGE_ORCHESTRATOR: final(str) = "edge_orchestrator"
    CLOUD_ORCHESTRATOR: final(str) = "cloud_orchestrator"


class DeviceId(StrEnum):
    """
    Enum for the IDs of the devices in the simulation.
    """

    VEHICLE: final(str) = "vehicle_id"
    BASE_STATION: final(str) = "base_station_id"
    CONTROLLER: final(str) = "controller_id"
    RSU: final(str) = "rsu_id"
    LINK: final(str) = "link_id"
    DEVICE: final(str) = "device_id"


class CoordSpace(StrEnum):
    """
    Enum for the coordinates.
    """

    X: final(str) = "x"
    X_MIN: final(str) = "x_min"
    X_MAX: final(str) = "x_max"
    Y: final(str) = "y"
    Y_MIN: final(str) = "y_min"
    Y_MAX: final(str) = "y_max"


class TraceTimes(StrEnum):
    """
    Enum for the simulation time settings.
    """

    START_TIME: final(str) = "start_time"
    END_TIME: final(str) = "end_time"
    TIME_STEP: final(str) = "time_step"


class Column(StrEnum):
    """
    Enum for some of the column headers in the input files.
    """

    VELOCITY: final(str) = "velocity"
    VEHICLES_STR: final(str) = "vehicles_str"
    BASE_STATIONS_STR: final(str) = "base_stations_str"
    ROADSIDE_UNITS_STR: final(str) = "roadside_units_str"
    DISTANCES_STR: final(str) = "distances_str"


class ColumnNames(list[str], Enum):
    """
    Enum for the column names in the input files.
    """

    VEHICLE_TRACES: list[str] = [
        TraceTimes.TIME_STEP,
        DeviceId.VEHICLE,
        CoordSpace.X,
        CoordSpace.Y,
        Column.VELOCITY,
    ]
    BASE_STATIONS: list[str] = [
        DeviceId.BASE_STATION,
        CoordSpace.X,
        CoordSpace.Y,
    ]
    CONTROLLERS: list[str] = [DeviceId.CONTROLLER, CoordSpace.X, CoordSpace.Y]
    ROADSIDE_UNITS: list[str] = [DeviceId.RSU, CoordSpace.X, CoordSpace.Y]

    ACTIVATION_TIMES: list[str] = [
        DeviceId.DEVICE,
        TraceTimes.START_TIME,
        TraceTimes.END_TIME,
    ]
    V2V_LINKS: list[str] = [
        DeviceId.VEHICLE,
        TraceTimes.TIME_STEP,
        Column.VEHICLES_STR,
        Column.DISTANCES_STR,
    ]
    V2B_LINKS: list[str] = [
        DeviceId.VEHICLE,
        TraceTimes.TIME_STEP,
        Column.BASE_STATIONS_STR,
        Column.DISTANCES_STR,
    ]
    V2R_LINKS: list[str] = [
        DeviceId.VEHICLE,
        TraceTimes.TIME_STEP,
        Column.ROADSIDE_UNITS_STR,
        Column.DISTANCES_STR,
    ]

    B2C_LINKS: list[str] = [
        DeviceId.LINK,
        DeviceId.BASE_STATION,
        DeviceId.CONTROLLER,
    ]
    R2B_LINKS: list[str] = [
        DeviceId.LINK,
        DeviceId.RSU,
        Column.BASE_STATIONS_STR,
        Column.DISTANCES_STR,
    ]
    R2R_LINKS: list[str] = [
        DeviceId.LINK,
        DeviceId.RSU,
        Column.ROADSIDE_UNITS_STR,
        Column.DISTANCES_STR,
    ]


class ColumnDTypes(dict[str, type], Enum):
    """
    Enum for the data types of the columns in the input files.
    """

    VEHICLE_TRACES: dict[str, type] = {
        TraceTimes.TIME_STEP: int,
        DeviceId.VEHICLE: int,
        CoordSpace.X: float,
        CoordSpace.Y: float,
        Column.VELOCITY: float,
    }
    BASE_STATIONS: dict[str, type] = {
        DeviceId.BASE_STATION: int,
        CoordSpace.X: float,
        CoordSpace.Y: float,
    }
    CONTROLLERS: dict[str, type] = {
        DeviceId.CONTROLLER: int,
        CoordSpace.X: float,
        CoordSpace.Y: float,
    }
    ROADSIDE_UNITS: dict[str, type] = {
        DeviceId.RSU: int,
        CoordSpace.X: float,
        CoordSpace.Y: float,
    }

    V2V_LINKS: dict[str, type] = {
        DeviceId.VEHICLE: int,
        TraceTimes.TIME_STEP: int,
        Column.VEHICLES_STR: str,
        Column.DISTANCES_STR: str,
    }
    V2B_LINKS: dict[str, type] = {
        DeviceId.VEHICLE: int,
        TraceTimes.TIME_STEP: int,
        Column.BASE_STATIONS_STR: str,
        Column.DISTANCES_STR: str,
    }
    V2R_LINKS: dict[str, type] = {
        DeviceId.VEHICLE: int,
        TraceTimes.TIME_STEP: int,
        Column.ROADSIDE_UNITS_STR: str,
        Column.DISTANCES_STR: str,
    }
    B2C_LINKS: dict[str, type] = {
        DeviceId.LINK: int,
        DeviceId.BASE_STATION: int,
        DeviceId.CONTROLLER: int,
    }
    R2B_LINKS: dict[str, type] = {
        DeviceId.LINK: int,
        DeviceId.RSU: int,
        Column.BASE_STATIONS_STR: str,
        Column.DISTANCES_STR: str,
    }
    R2R_LINKS: dict[str, type] = {
        DeviceId.LINK: int,
        DeviceId.RSU: int,
        Column.ROADSIDE_UNITS_STR: str,
        Column.DISTANCES_STR: str,
    }
    ACTIVATION_TIMES: dict[str, type] = {
        DeviceId.DEVICE: int,
        TraceTimes.START_TIME: str,
        TraceTimes.END_TIME: str,
    }


class FileExtension(StrEnum):
    """
    Enum for the file extensions.
    """

    PARQUET: final(str) = "parquet"
    CSV: final(str) = "csv"
