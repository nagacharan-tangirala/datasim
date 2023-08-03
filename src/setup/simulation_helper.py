import logging
from os import makedirs
from os.path import dirname, exists, join

import toml

from src.core.common_constants import *
from src.core.constants import *
from src.core.custom_exceptions import *
from src.core.logger_config import LoggerConfig
from src.setup.csv_data_reader import CSVDataReader
from src.setup.parquet_data_reader import ParquetDataReader

logger = logging.getLogger(__name__)


class SimulationHelper:
    def __init__(self, config_file: str):
        """
        Initialize the simulation helper.

        Parameters
        ----------
        config_file : str
            The path to the configuration file.
        """
        self.config_file: str = config_file
        self.config_data: dict = {}
        self.project_path: str = dirname(config_file)

        self.file_readers: dict[str, CSVDataReader | ParquetDataReader] = {}

        self.vehicle_models_data: dict = {}
        self.base_station_models_data: dict = {}
        self.controller_models_data: dict = {}

        self.orchestrator_models_data: dict = {}
        self.simulation_data: dict = {}
        self.application_data: dict = {}
        self.json_validator: dict = {}

    def read_config_file(self) -> None:
        """
        Read the config file.
        """
        with open(self.config_file, "r") as f:
            self.config_data = toml.load(f)

    def read_simulation_and_model_settings(self) -> None:
        """
        Read the input files.
        """
        # Read simulation settings.
        logger.debug("Storing the simulation settings.")
        self.simulation_data = self.config_data[C_SIMULATION_SETTINGS]

        logger.debug("Storing the application settings.")
        self.application_data = self.config_data[C_APPLICATIONS]

        # Read the channel models.
        logger.debug("Storing the wireless and wired channel model.")
        self.orchestrator_models_data[C_EDGE_ORCHESTRATOR] = self.config_data[
            C_EDGE_ORCHESTRATOR
        ]
        self.orchestrator_models_data[C_CLOUD_ORCHESTRATOR] = self.config_data[
            C_CLOUD_ORCHESTRATOR
        ]

        # Read the devices.
        logger.debug("Storing all of the device models.")
        self.vehicle_models_data = self.config_data[C_VEHICLES]
        self.base_station_models_data = self.config_data[C_BASE_STATIONS]
        self.controller_models_data = self.config_data[C_CONTROLLERS]

    def create_output_directory(self) -> None:
        """
        Create the output directory.
        """
        # Create output directory.
        logger.debug("Creating the output directory.")
        self._create_output_dir(self.simulation_data[C_OUTPUT_LOCATION])

    def create_loggers(self) -> None:
        """
        Create the loggers.
        """
        logging_level = "INFO"
        if C_LOGGING_LEVEL in self.config_data[C_SIMULATION_SETTINGS]:
            logging_level = str(
                self.config_data[C_SIMULATION_SETTINGS][C_LOGGING_LEVEL]
            ).upper()

        logging_filename = "simulation.log"
        if C_LOG_FILE in self.config_data[C_SIMULATION_SETTINGS]:
            logging_filename = self.config_data[C_SIMULATION_SETTINGS][C_LOG_FILE]

        logging_file = join(self.project_path, logging_filename)
        if not exists(dirname(logging_file)):
            makedirs(dirname(logging_file))

        logger_config = LoggerConfig(logging_file, logging_level)
        logger_config.setup_logger_config()

    def create_file_readers(self) -> None:
        """
        Read the input files.
        """
        # Read the input files.
        logger.debug("Creating input file readers.")
        input_files = self.config_data[C_INPUT_FILES]

        # Create the file readers
        logger.debug("Creating file reader for vehicle trace file.")
        self._create_new_file_reader(
            input_files[CC_VEHICLE_TRACE_FILE],
            CC_VEHICLE_TRACE_COLUMN_NAMES,
            CC_VEHICLE_TRACE_COLUMN_DTYPES,
            CC_VEHICLE_TRACE_FILE,
        )

        logger.debug("Creating file reader for activation times file.")
        self._create_new_file_reader(
            input_files[CC_VEHICLE_ACTIVATIONS_FILE],
            CC_ACTIVATION_TIMES_COLUMN_NAMES,
            CC_ACTIVATION_TIMES_COLUMN_DTYPES,
            CC_VEHICLE_ACTIVATIONS_FILE,
        )

        logger.debug("Creating file reader for v2v links file.")
        self._create_new_file_reader(
            input_files[CC_V2V_LINKS_FILE],
            CC_V2V_LINKS_COLUMN_NAMES,
            CC_V2V_LINKS_COLUMN_DTYPES,
            CC_V2V_LINKS_FILE,
        )

        logger.debug("Creating file reader for base stations file.")
        self._create_new_file_reader(
            input_files[CC_BASE_STATIONS_FILE],
            CC_BASE_STATION_COLUMN_NAMES,
            CC_BASE_STATION_COLUMN_DTYPES,
            CC_BASE_STATIONS_FILE,
        )

        logger.debug("Creating file reader for v2b links file.")
        self._create_new_file_reader(
            input_files[CC_V2B_LINKS_FILE],
            CC_V2B_LINKS_COLUMN_NAMES,
            CC_V2B_LINKS_COLUMN_DTYPES,
            CC_V2B_LINKS_FILE,
        )

        logger.debug("Creating file reader for controllers file.")
        self._create_new_file_reader(
            input_files[CC_CONTROLLERS_FILE],
            CC_CONTROLLERS_COLUMN_NAMES,
            CC_CONTROLLERS_COLUMN_DTYPES,
            CC_CONTROLLERS_FILE,
        )

        logger.debug("Creating file reader for b2c links file.")
        self._create_new_file_reader(
            input_files[CC_B2C_LINKS_FILE],
            CC_B2C_LINKS_COLUMN_NAMES,
            CC_B2C_LINKS_COLUMN_DTYPES,
            CC_B2C_LINKS_FILE,
        )

        logger.debug("Creating optional file readers if they are provided.")
        if input_files[CC_BASE_STATION_ACTIVATIONS_FILE] != "":
            logger.debug("Creating file reader for base station activations file.")
            self._create_new_file_reader(
                input_files[CC_BASE_STATION_ACTIVATIONS_FILE],
                CC_ACTIVATION_TIMES_COLUMN_NAMES,
                CC_ACTIVATION_TIMES_COLUMN_DTYPES,
                CC_BASE_STATION_ACTIVATIONS_FILE,
            )
        else:
            self._create_none_file_reader(CC_BASE_STATION_ACTIVATIONS_FILE)

        if input_files[CC_CONTROLLER_ACTIVATIONS_FILE] != "":
            logger.debug("Creating file reader for controller activations file.")
            self._create_new_file_reader(
                input_files[CC_CONTROLLER_ACTIVATIONS_FILE],
                CC_ACTIVATION_TIMES_COLUMN_NAMES,
                CC_ACTIVATION_TIMES_COLUMN_DTYPES,
                CC_CONTROLLER_ACTIVATIONS_FILE,
            )
        else:
            self._create_none_file_reader(CC_CONTROLLER_ACTIVATIONS_FILE)

    def _create_new_file_reader(
        self, filename: str, column_names: list[str], column_dtypes: dict, file_key: str
    ) -> None:
        """
        Create a new file reader.

        Parameters
        ----------
        filename : str
            The filename.
        column_names : list[str]
            The column names.
        column_dtypes : dict
            The column data types.
        file_key : str
            The file key.
        """
        # Get the path to the file and the file type
        file_path = join(self.project_path, filename)

        # Check if it is a valid file.
        if not exists(file_path):
            logger.warning("File %s does not exist. Skipping file.", file_path)
            return

        file_type = filename.split(".")[-1]

        logger.debug("Creating reader object for file %s", file_path)
        if file_type == CC_PARQUET:
            self.file_readers[file_key] = ParquetDataReader(
                file_path, column_names, column_dtypes
            )
        elif file_type == CC_CSV:
            self.file_readers[file_key] = CSVDataReader(
                file_path, column_names, column_dtypes
            )
        else:
            raise UnsupportedInputFormatError(file_type)

    def _create_none_file_reader(self, file_key: str) -> None:
        """
        Create a None file reader.

        Parameters
        ----------
        file_key : str
            The file key.
        """
        self.file_readers[file_key] = None

    def _create_output_dir(self, output_dir: str) -> str:
        """
        Create the output directory if it does not exist.

        Parameters
        ----------
        output_dir : str
            The relative path to the output directory.
        """
        output_dir = join(self.project_path, output_dir)
        if not exists(output_dir):
            makedirs(output_dir)

        logger.debug("Output directory: %s", output_dir)
        return output_dir
