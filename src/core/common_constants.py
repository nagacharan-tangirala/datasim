# Input file names
VEHICLE_TRACE_FILE: str = "vehicle_traces"
VEHICLE_ACTIVATIONS_FILE: str = "vehicle_activations"
V2V_LINKS_FILE: str = "v2v_links"
BASE_STATIONS_FILE: str = "base_stations"
BASE_STATION_ACTIVATIONS_FILE: str = "base_station_activations"
V2B_LINKS_FILE: str = "v2b_links"
CONTROLLERS_FILE: str = "controllers"
CONTROLLER_ACTIVATIONS_FILE: str = "controller_activations"
B2C_LINKS_FILE: str = "b2c_links"
ROADSIDE_UNITS_FILE: str = "road_side_units"
RSU_ACTIVATIONS_FILE: str = "rsu_activations"
R2B_LINKS_FILE: str = "r2b_links"
V2R_LINKS_FILE: str = "v2r_links"
R2R_LINKS_FILE: str = "r2r_links"

# Main columns in the input files
VEHICLE_ID: str = "vehicle_id"
TIME_STEP: str = "time_step"
X: str = "x"
Y: str = "y"
VELOCITY: str = "velocity"
NEIGHBOURS: str = "neighbours"
DISTANCES: str = "distances"
BASE_STATIONS: str = "base_stations"
BASE_STATION_ID: str = "base_station_id"
ROADSIDE_UNITS: str = "roadside_units"
RSU_ID: str = "rsu_id"
CONTROLLER_ID: str = "controller_id"
START_TIME: str = "start_time"
END_TIME: str = "end_time"
LINK_ID: str = "link_id"

# Column names and data types for the input files
VEHICLE_TRACE_COLUMN_NAMES: list[str] = [TIME_STEP, VEHICLE_ID, X, Y, VELOCITY]
VEHICLE_TRACE_COLUMN_DTYPES: dict[str, type] = {
    TIME_STEP: float,
    VEHICLE_ID: int,
    X: float,
    Y: float,
    VELOCITY: float,
}

BASE_STATION_COLUMN_NAMES: list[str] = [BASE_STATION_ID, X, Y]
BASE_STATION_COLUMN_DTYPES: dict[str, type] = {BASE_STATION_ID: int, X: float, Y: float}

CONTROLLERS_COLUMN_NAMES: list[str] = [CONTROLLER_ID, X, Y]
CONTROLLERS_COLUMN_DTYPES: dict[str, type] = {CONTROLLER_ID: int, X: float, Y: float}

ROADSIDE_UNITS_COLUMN_NAMES: list[str] = [RSU_ID, X, Y]
ROADSIDE_UNITS_COLUMN_DTYPES: dict[str, type] = {RSU_ID: int, X: float, Y: float}

V2V_LINKS_COLUMN_NAMES: list[str] = [VEHICLE_ID, TIME_STEP, NEIGHBOURS, DISTANCES]
V2V_LINKS_COLUMN_DTYPES: dict[str, type] = {
    VEHICLE_ID: int,
    TIME_STEP: int,
    NEIGHBOURS: str,
    DISTANCES: str,
}


V2B_LINKS_COLUMN_NAMES: list[str] = [VEHICLE_ID, TIME_STEP, BASE_STATIONS, DISTANCES]
V2B_LINKS_COLUMN_DTYPES: dict[str, type] = {
    VEHICLE_ID: int,
    TIME_STEP: int,
    BASE_STATIONS: str,
    DISTANCES: str,
}

V2R_LINKS_COLUMN_NAMES: list[str] = [VEHICLE_ID, TIME_STEP, ROADSIDE_UNITS, DISTANCES]
V2R_LINKS_COLUMN_DTYPES: dict[str, type] = {
    VEHICLE_ID: int,
    TIME_STEP: int,
    ROADSIDE_UNITS: str,
    DISTANCES: str,
}

B2C_LINKS_COLUMN_NAMES: list[str] = [LINK_ID, BASE_STATION_ID, CONTROLLER_ID]
B2C_LINKS_COLUMN_DTYPES: dict[str, type] = {
    LINK_ID: int,
    BASE_STATION_ID: int,
    CONTROLLER_ID: int,
}

R2B_LINKS_COLUMN_NAMES: list[str] = [LINK_ID, RSU_ID, BASE_STATIONS, DISTANCES]
R2B_LINKS_COLUMN_DTYPES: dict[str, type] = {
    LINK_ID: int,
    RSU_ID: int,
    BASE_STATIONS: str,
    DISTANCES: str,
}

R2R_LINKS_COLUMN_NAMES: list[str] = [LINK_ID, RSU_ID, ROADSIDE_UNITS, DISTANCES]
R2R_LINKS_COLUMN_DTYPES: dict[str, type] = {
    LINK_ID: int,
    RSU_ID: int,
    ROADSIDE_UNITS: str,
    DISTANCES: str,
}

ACTIVATION_TIMES_COLUMN_NAMES: list[str] = [VEHICLE_ID, START_TIME, END_TIME]
ACTIVATION_TIMES_COLUMN_DTYPES: dict[str, type] = {
    VEHICLE_ID: int,
    START_TIME: str,
    END_TIME: str,
}

# File extensions
PARQUET: str = "parquet"
CSV: str = "csv"

# Space keys
SPACE_X_MIN = "x_min"
SPACE_X_MAX = "x_max"
SPACE_Y_MIN = "y_min"
SPACE_Y_MAX = "y_max"
