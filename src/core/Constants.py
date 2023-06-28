# Top level keys in the input json file
P_INPUT_FILES = "input_files"
P_SIMULATION_SETTINGS = "simulation_settings"
P_UES = "ues"
P_CELL_TOWERS = "cell_towers"
P_CONTROLLERS = "controllers"
P_WIRELESS_CHANNEL = "wireless_channel"
P_WIRED_CHANNEL = "wired_channel"

# Input files keys in the input json file
P_UE_TRACE_FILE = "p_ue_trace_file"
P_UE_LINKS_FILE = "p_ue_links_file"
P_CELL_TOWER_LINKS_FILE = "p_tower_links_file"
P_CELL_TOWERS_FILE = "p_cell_towers_file"
P_CONTROLLERS_FILE = "p_controller_file"
P_CONTROLLER_LINKS_FILE = "p_controller_links_file"

# Simulation parameters keys in the input json file
P_SIMULATION_START_TIME = "p_start_time"
P_SIMULATION_END_TIME = "p_end_time"
P_SIMULATION_TIME_STEP = "p_time_step"
P_DATA_STREAMING_INTERVAL = "p_data_streaming_interval"
P_OUTPUT_TYPE = "p_output_type"
P_LOGGING_LEVEL = "p_logging_level"
P_LOG_FILE = "p_log_file"
P_OUTPUT_LOCATION = "p_output_location"

# UE keys in the input json file
P_UE_TYPE = "p_ue_type"
P_UE_RATIO = "p_ue_ratio"
P_UE_MOBILITY_MODEL = "p_mobility_model"
P_UE_DATA_MODEL = "p_data_model"

# Cell tower keys in the input json file
P_CELL_TOWER_TYPE = "p_cell_tower_type"

# Controller keys in the input json file
P_CONTROLLER_TYPE = "p_controller_type"

# Channel keys in the input json file
P_CHANNEL_NAME = "p_channel_name"
P_THROUGHPUT_PER_SECOND = "p_throughput_per_second"
P_DATA_PROCESSOR_MODEL = "p_data_processor_model"
P_DATA_PROCESSOR_NAME = "p_data_processor_name"
P_DATA_COMPRESSION_RATIO = "p_data_compression_ratio"
P_TOWER_LOOKUP_MODEL = "p_tower_lookup_model"
P_TOWER_LOOKUP_NAME = "p_tower_lookup_name"
P_TOWER_LOOKUP_N = "p_tower_lookup_n"
P_NEIGHBOUR_LOOKUP_MODEL = "p_neighbour_lookup_model"
P_NEIGHBOUR_LOOKUP_NAME = "p_neighbour_lookup_name"
P_CONTROLLER_LOOKUP_MODEL = "p_controller_lookup_model"
P_CONTROLLER_LOOKUP_NAME = "p_controller_lookup_name"

# Column names and data types for the input files
P_UE_TRACE_COLUMN_NAMES = ['vehicle_id', 'time', 'x', 'y']
P_UE_TRACE_COLUMN_DTYPES = {'vehicle_id': int, 'time': float, 'x': float, 'y': float}

P_UE_LINKS_COLUMN_NAMES = ['vehicle_id', 'time', 'neighbours', 'neighbour_distances']
P_UE_LINKS_COLUMN_DTYPES = {'vehicle_id': int, 'time': int, 'neighbours': str, 'neighbour_distances': str}

P_CELL_TOWER_COLUMN_NAMES = ['cell_tower_id', 'x', 'y', 'type']
P_CELL_TOWER_COLUMN_DTYPES = {'cell_tower_id': int, 'x': float, 'y': float, 'type': str}

P_CONTROLLERS_COLUMN_NAMES = ['controller_id', 'x', 'y']
P_CONTROLLERS_COLUMN_DTYPES = {'controller_id': int, 'x': float, 'y': float}

P_CONTROLLER_LINKS_COLUMN_NAMES = ['link_id', 'source_type', 'source_id', 'target_type', 'target_id']
P_CONTROLLER_LINKS_COLUMN_DTYPES = {'link_id': int, 'source_type': str, 'source_id': int, 'target_type': str, 'target_id': int}

P_CELL_TOWER_LINKS_COLUMN_NAMES = ['link_id', 'source_type', 'source_id', 'target_type', 'target_id']
P_CELL_TOWER_LINKS_COLUMN_DTYPES = {'link_id': int, 'source_type': str, 'source_id': int, 'target_type': str, 'target_id': int}

P_PARQUET_FILE_EXTENSION: str = "parquet"
P_CSV_FILE_EXTENSION: str = "csv"
