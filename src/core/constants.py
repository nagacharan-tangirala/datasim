from enum import Enum, IntEnum, StrEnum
from typing import final


class MainKey(StrEnum):
    """
    Enum for the primary keys in the input file.
    """

    INPUT_FILES: final(str) = "input_files"
    SIMULATION_SETTINGS: final(str) = "simulation_settings"
    VEHICLES: final(str) = "vehicles"
    BASE_STATIONS: final(str) = "base_stations"
    CONTROLLERS: final(str) = "controllers"
    ROADSIDE_UNITS: final(str) = "roadside_units"
    EDGE_ORCHESTRATOR: final(str) = "edge_orchestrator"
    CLOUD_ORCHESTRATOR: final(str) = "cloud_orchestrator"
    OUTPUT_SETTINGS: final(str) = "output_settings"
    SPACE: final(str) = "space"


class SimTimes(StrEnum):
    """
    Enum for the simulation settings keys.
    """

    START: final(str) = "start_time"
    END: final(str) = "end_time"
    STEP: final(str) = "time_step"
    DATA_STREAMING_INTERVAL: final(str) = "data_streaming_interval"


class LogKey(StrEnum):
    """
    Enum for the logging keys.
    """

    LEVEL: final(str) = "logging_level"
    FILE: final(str) = "log_file"
    LOCATION: final(str) = "log_location"
    OVERWRITE: final(str) = "log_overwrite"


class OutputKey(StrEnum):
    """
    Enum for the output settings keys.
    """

    TYPE: final(str) = "output_type"
    LOCATION: final(str) = "output_location"


class HardwareKey(StrEnum):
    """
    Enum for the hardware keys.
    """

    COMPUTING: final(str) = "computing_hardware"
    NETWORKING: final(str) = "networking_hardware"
    WIRED: final(str) = "wired"
    WIRELESS: final(str) = "wireless"


class ModelName(StrEnum):
    """
    Enum for the names of the models.
    """

    MOBILITY: final(str) = "mobility"
    DATA_SOURCE: final(str) = "data_source"
    DATA_COMPOSER: final(str) = "composer"
    DATA_SIMPLIFIER: final(str) = "simplifier"
    DATA_COLLECTOR: final(str) = "collector"
    BASE_STATION_FINDER: final(str) = "base_station_finder"
    NEIGHBOUR_FINDER: final(str) = "neighbour_finder"


class ModelType(StrEnum):
    """
    Enum for the types of the models.
    """

    STATIC: final(str) = "static"
    TRACE: final(str) = "trace"
    NEAREST: final(str) = "nearest"
    SIMPLE: final(str) = "simple"


class ModelParam(StrEnum):
    """
    Enum for the settings of the models.
    """

    MODEL_NAME: final(str) = "name"
    POSITION: final(str) = "position"
    VEHICLE_RATIO: final(str) = "ratio"
    RETENTION_FACTOR: final(str) = "retention_factor"
    COMPRESSION_FACTOR: final(str) = "compression_factor"


class DataSourceKey(StrEnum):
    """
    Enum for the data source keys.
    """

    DATA_SIZE: final(str) = "data_size"
    DATA_COUNTS: final(str) = "data_counts"
    DATA_SOURCE_TYPE: final(str) = "data_type"
    DATA_SIDE_LINK: final(str) = "side_link"
    DATA_PRIORITY: final(str) = "priority"


class ProgressBar(StrEnum):
    """
    Enum for the progress bar keys.
    """

    # Simulation progress bar
    SIM_PROGRESS_UNIT: final(str) = " steps"
    SIM_RUNNING_MESSAGE: final(str) = "Running. Simulation Progress"
    SIM_PAUSED_MESSAGE: final(str) = "Paused. Refreshing Input Data"
    SIM_DONE_MESSAGE: final(str) = "Done. Simulation Completed"

    # Output file saving progress bar
    SAVE_PROGRESS_UNIT: final(str) = " files"
    SAVE_STARTING_MESSAGE: final(str) = "Saving Files"
    SAVE_DONE_MESSAGE: final(str) = " Done. Output Files Saved "

    # Common for the progress bars
    RUNNING_COLOUR: final(str) = "#05d6fc"
    PAUSED_COLOUR: final(str) = "#fa772a"
    DONE_COLOUR: final(str) = "#11c26c"


class ProgressBarWidth(IntEnum):
    """
    Enum for the progress bar widths.
    """

    SIM: final(int) = 150
    FILE_SAVE: final(int) = 120


class Defaults:
    """
    Enum for the miscellaneous keys.
    """

    BUFFER_SPACE: final(float) = 10.0
    LOG_FILE: final(str) = "simulation.log"
    LOG_LEVEL: final(str) = "INFO"
    LOG_OVERWRITE: final(bool) = False
