import logging
from pathlib import Path

import toml
from core.exceptions import UnsupportedInputFormatError

import src.core.common_constants as cc
import src.core.constants as constants
from src.core.logger_config import LoggerConfig
from src.setup.file_reader import CSVDataReader, ParquetDataReader

logger = logging.getLogger(__name__)


class SimulationInputHelper:
    def __init__(self, config_file: Path):
        """
        Initialize the simulation input helper.

        Parameters
        ----------
        config_file : Path
            The path to the configuration file.
        """
        self.config_file: Path = config_file
        self.project_path: Path = config_file.parent
        self.config_data: dict = {}

        self.file_readers: dict[str, CSVDataReader | ParquetDataReader | None] = {}

        self.vehicle_models_data: dict = {}
        self.base_station_models_data: dict = {}
        self.controller_models_data: dict = {}
        self.rsu_models_data: dict = {}

        self.simulation_data: dict = {}
        self.output_data: dict = {}
        self.space_settings: dict = {}
        self.orchestrator_models_data: dict = {}

        self._output_dir: str = ""

    def read_config_file(self) -> None:
        """Read the config file."""
        with self.config_file.open(mode="r") as f:
            self.config_data = toml.load(f)

    @property
    def output_dir(self) -> str:
        """Get the output directory."""
        return self._output_dir

    def read_simulation_and_model_settings(self) -> None:
        """Read the input files."""
        # Read simulation settings.
        logger.debug("Storing the simulation settings.")
        self.simulation_data = self.config_data[constants.SIMULATION_SETTINGS]

        # Read the output settings.
        logger.debug("Storing the output settings.")
        self.output_data = self.config_data[constants.OUTPUT_SETTINGS]

        # Read the space settings.
        logger.debug("Storing the space settings.")
        self.space_settings = self.config_data[constants.SPACE]

        # Read the channel models.
        logger.debug("Storing the edge and cloud orchestrator models.")
        self.orchestrator_models_data[constants.EDGE_ORCHESTRATOR] = self.config_data[
            constants.EDGE_ORCHESTRATOR
        ]
        self.orchestrator_models_data[constants.CLOUD_ORCHESTRATOR] = self.config_data[
            constants.CLOUD_ORCHESTRATOR
        ]

        # Read the devices.
        logger.debug("Storing all of the device models.")
        self.vehicle_models_data = self.config_data[constants.VEHICLES]
        self.base_station_models_data = self.config_data[constants.BASE_STATIONS]
        self.controller_models_data = self.config_data[constants.CONTROLLERS]
        self.rsu_models_data = self.config_data[constants.ROADSIDE_UNITS]

    def create_output_directory(self) -> None:
        """
        Create the output directory.
        """
        # Create output directory.
        logger.debug("Creating the output directory.")
        output_filepath: Path = Path(self.output_data[constants.OUTPUT_LOCATION])
        self._create_output_dir(output_filepath)

    def create_loggers(self) -> None:
        """
        Create the loggers.
        """
        output_data = self.config_data[constants.OUTPUT_SETTINGS]
        logging_level = constants.DEFAULT_LOG_LEVEL
        if constants.LOGGING_LEVEL in output_data:
            logging_level = str(output_data[constants.LOGGING_LEVEL]).upper()

        log_overwrite = False
        if (
            constants.LOG_OVERWRITE in output_data
            and output_data[constants.LOG_OVERWRITE] == "yes"
        ):
            log_overwrite = True

        logging_filename = constants.DEFAULT_LOG_FILE
        if constants.LOG_FILE in output_data:
            logging_filename = output_data[constants.LOG_FILE]

        logging_location = self.project_path
        if constants.LOG_LOCATION in output_data:
            logging_location = logging_location / (output_data[constants.LOG_LOCATION])

        logging_file = logging_location / logging_filename
        if not logging_file.exists():
            Path.mkdir(logging_location, parents=True, exist_ok=True)

        logger_config = LoggerConfig(logging_file, logging_level, log_overwrite)
        logger_config.setup_logger_config()

    def create_file_readers(self) -> None:
        """
        Read the input files.
        """
        self._create_all_devices_file_readers()
        self._create_activation_file_readers()
        self._create_links_file_readers()

    def _create_all_devices_file_readers(self) -> None:
        """Create the file readers for all devices."""
        input_files = self.config_data[constants.INPUT_FILES]
        logger.debug("Creating file reader for vehicle trace file.")
        self._create_new_file_reader(
            input_files[cc.VEHICLE_TRACE_FILE],
            cc.VEHICLE_TRACE_COLUMN_NAMES,
            cc.VEHICLE_TRACE_COLUMN_DTYPES,
            cc.VEHICLE_TRACE_FILE,
        )

        logger.debug("Creating file reader for base stations file.")
        self._create_new_file_reader(
            input_files[cc.BASE_STATIONS_FILE],
            cc.BASE_STATION_COLUMN_NAMES,
            cc.BASE_STATION_COLUMN_DTYPES,
            cc.BASE_STATIONS_FILE,
        )

        logger.debug("Creating file reader for controllers file.")
        self._create_new_file_reader(
            input_files[cc.CONTROLLERS_FILE],
            cc.CONTROLLERS_COLUMN_NAMES,
            cc.CONTROLLERS_COLUMN_DTYPES,
            cc.CONTROLLERS_FILE,
        )

    def _create_activation_file_readers(self) -> None:
        """Create the file readers for all activation files."""
        input_files = self.config_data[constants.INPUT_FILES]
        logger.debug("Creating file reader for vehicle activation times file.")
        self._create_new_file_reader(
            input_files[cc.VEHICLE_ACTIVATIONS_FILE],
            cc.ACTIVATION_TIMES_COLUMN_NAMES,
            cc.ACTIVATION_TIMES_COLUMN_DTYPES,
            cc.VEHICLE_ACTIVATIONS_FILE,
        )
        if input_files[cc.BASE_STATION_ACTIVATIONS_FILE] != "":
            logger.debug("Creating file reader for base station activations file.")
            self._create_new_file_reader(
                input_files[cc.BASE_STATION_ACTIVATIONS_FILE],
                cc.ACTIVATION_TIMES_COLUMN_NAMES,
                cc.ACTIVATION_TIMES_COLUMN_DTYPES,
                cc.BASE_STATION_ACTIVATIONS_FILE,
            )
        else:
            self._create_none_file_reader(cc.BASE_STATION_ACTIVATIONS_FILE)

        if input_files[cc.CONTROLLER_ACTIVATIONS_FILE] != "":
            logger.debug("Creating file reader for controller activations file.")
            self._create_new_file_reader(
                input_files[cc.CONTROLLER_ACTIVATIONS_FILE],
                cc.ACTIVATION_TIMES_COLUMN_NAMES,
                cc.ACTIVATION_TIMES_COLUMN_DTYPES,
                cc.CONTROLLER_ACTIVATIONS_FILE,
            )
        else:
            self._create_none_file_reader(cc.CONTROLLER_ACTIVATIONS_FILE)

        if input_files[cc.RSU_ACTIVATIONS_FILE] != "":
            logger.debug("Creating file reader for roadside unit activations file.")
            self._create_new_file_reader(
                input_files[cc.RSU_ACTIVATIONS_FILE],
                cc.ACTIVATION_TIMES_COLUMN_NAMES,
                cc.ACTIVATION_TIMES_COLUMN_DTYPES,
                cc.RSU_ACTIVATIONS_FILE,
            )
        else:
            self._create_none_file_reader(cc.RSU_ACTIVATIONS_FILE)

    def _create_links_file_readers(self) -> None:
        """Create the file readers for all links files."""
        logger.debug("Creating input file readers.")
        input_files = self.config_data[constants.INPUT_FILES]

        logger.debug("Creating file reader for v2v links file.")
        self._create_new_file_reader(
            input_files[cc.V2V_LINKS_FILE],
            cc.V2V_LINKS_COLUMN_NAMES,
            cc.V2V_LINKS_COLUMN_DTYPES,
            cc.V2V_LINKS_FILE,
        )

        logger.debug("Creating file reader for v2b links file.")
        self._create_new_file_reader(
            input_files[cc.V2B_LINKS_FILE],
            cc.V2B_LINKS_COLUMN_NAMES,
            cc.V2B_LINKS_COLUMN_DTYPES,
            cc.V2B_LINKS_FILE,
        )

        logger.debug("Creating file reader for b2c links file.")
        self._create_new_file_reader(
            input_files[cc.B2C_LINKS_FILE],
            cc.B2C_LINKS_COLUMN_NAMES,
            cc.B2C_LINKS_COLUMN_DTYPES,
            cc.B2C_LINKS_FILE,
        )

        logger.debug("Creating file reader for roadside units file.")
        self._create_new_file_reader(
            input_files[cc.ROADSIDE_UNITS_FILE],
            cc.ROADSIDE_UNITS_COLUMN_NAMES,
            cc.ROADSIDE_UNITS_COLUMN_DTYPES,
            cc.ROADSIDE_UNITS_FILE,
        )

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
        file_path = self.project_path / filename

        # Check if it is a valid file.
        if not file_path.exists():
            logger.warning("File %s does not exist. Skipping file.", file_path)
            return

        file_type = filename.split(".")[-1]

        logger.debug("Creating reader object for file %s", file_path)
        if file_type == cc.PARQUET:
            self.file_readers[file_key] = ParquetDataReader(
                file_path, column_names, column_dtypes
            )
        elif file_type == cc.CSV:
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

    def _create_output_dir(self, output_dir: Path) -> None:
        """
        Create the output directory if it does not exist.

        Parameters
        ----------
        output_dir : str
            The relative path to the output directory.
        """
        self._output_dir = self.project_path / output_dir
        if not output_dir.exists():
            Path.mkdir(output_dir, parents=True, exist_ok=True)

        logger.debug("Output directory: %s", self._output_dir)
