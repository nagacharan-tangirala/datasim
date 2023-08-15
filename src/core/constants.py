# Top level keys in the input file
INPUT_FILES = "input_files"
SIMULATION_SETTINGS = "simulation_settings"
VEHICLES = "vehicles"
BASE_STATIONS = "base_stations"
CONTROLLERS = "controllers"
EDGE_ORCHESTRATOR = "edge_orchestrator"
CLOUD_ORCHESTRATOR = "cloud_orchestrator"
OUTPUT_SETTINGS = "output_settings"
SPACE = "space"

# Simulation parameters keys
SIMULATION_START_TIME = "start_time"
SIMULATION_END_TIME = "end_time"
SIMULATION_TIME_STEP = "time_step"
DATA_STREAMING_INTERVAL = "data_streaming_interval"

# Logging settings keys
LOGGING_LEVEL = "logging_level"
LOG_FILE = "log_file"
LOG_LOCATION = "log_location"
LOG_OVERWRITE = "log_overwrite"
OUTPUT_TYPE = "output_type"
OUTPUT_LOCATION = "output_location"

# Other logging constants
DEFAULT_LOG_FILE = "simulation.log"
DEFAULT_LOG_LEVEL = "INFO"

# Vehicle data keys
VEHICLE_RATIO = "ratio"

# Hardware data keys
COMPUTING_HARDWARE = "computing_hardware"
NETWORKING_HARDWARE = "networking_hardware"
WIRED = "wired"
WIRELESS = "wireless"

# Model data keys
MOBILITY = "mobility"
DATA_SOURCE = "data_source"
DATA_COMPOSER = "composer"
DATA_SIMPLIFIER = "simplifier"
DATA_COLLECTOR = "collector"
BASE_STATION_FINDER = "base_station_finder"
NEIGHBOUR_FINDER = "neighbour_finder"

# Model parameter keys
POSITION = "position"
MODEL_NAME = "name"
DATA_SIZE = "data_size"
DATA_COUNTS = "data_counts"
DATA_SOURCE_TYPE = "data_type"
DATA_SIDE_LINK = "side_link"
DATA_PRIORITY = "priority"
RETENTION_FACTOR = "retention_factor"
COMPRESSION_FACTOR = "compression_factor"

# Model type keys
STATIC_MOBILITY = "static"
TRACE_MOBILITY = "trace"

TRACE_V2V = "trace"
NEAREST_V2B = "nearest"

SIMPLE_VEHICLE_DATA_COLLECTOR = "simple"
SIMPLE_VEHICLE_DATA_COMPOSER = "simple"
SIMPLE_VEHICLE_DATA_SIMPLIFIER = "simple"

SIMPLE_CONTROLLER_DATA_COLLECTOR = "simple"
SIMPLE_CONTROLLER_DATA_COMPOSER = "simple"

SIMPLE_BASE_STATION_DATA_COMPOSER = "simple"
SIMPLE_BASE_STATION_DATA_SIMPLIFIER = "simple"

# Main progress bar keys
PROGRESS_BAR_UNIT = " steps"

PROGRESS_BAR_RUNNING_MESSAGE = "Running. Simulation Progress"
PROGRESS_BAR_PAUSED_MESSAGE = "Paused. Refreshing Input Data"
PROGRESS_BAR_DONE_MESSAGE = "Done. Simulation Completed"

PROGRESS_BAR_RUNNING_COLOUR = "#05d6fc"
PROGRESS_BAR_PAUSED_COLOUR = "#fa772a"
PROGRESS_BAR_DONE_COLOUR = "#11c26c"

PROGRESS_BAR_WIDTH = 150

# File progress bar keys
FILE_PROGRESS_BAR_UNIT = " files"
FILE_PROGRESS_BAR_WIDTH = 120
FILE_PROGRESS_BAR_STARTING_MESSAGE = "Saving Files"
FILE_PROGRESS_BAR_DONE_MESSAGE = " Done. Output Files Saved "

# Space related constants
BUFFER_SPACE = 100.0
