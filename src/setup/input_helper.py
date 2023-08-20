import logging
from pathlib import Path

import toml
from core.exceptions import UnsupportedInputFormatError

from src.core.common_constants import (
    ColumnDTypes,
    ColumnNames,
    FileExtension,
    FilenameKey,
)
from src.core.constants import Defaults, LogKey, MainKey, OutputKey
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

        self._output_dir: Path | None = None

    def read_config_file(self) -> None:
        """Read the config file."""
        with self.config_file.open(mode="r") as f:
            self.config_data = toml.load(f)

    @property
    def output_dir(self) -> Path:
        """Get the output directory."""
        return self._output_dir

    def read_simulation_and_model_settings(self) -> None:
        """Read the input files."""
        logger.debug("Storing the simulation settings.")
        self.simulation_data = self.config_data[MainKey.SIMULATION_SETTINGS]

        logger.debug("Storing the output settings.")
        self.output_data = self.config_data[MainKey.OUTPUT_SETTINGS]

        logger.debug("Storing the space settings.")
        self.space_settings = self.config_data[MainKey.SPACE]

        logger.debug("Storing the edge and cloud orchestrator models.")
        self.orchestrator_models_data[MainKey.EDGE_ORCHESTRATOR] = self.config_data[
            MainKey.EDGE_ORCHESTRATOR
        ]
        self.orchestrator_models_data[MainKey.CLOUD_ORCHESTRATOR] = self.config_data[
            MainKey.CLOUD_ORCHESTRATOR
        ]

        logger.debug("Storing all of the device models.")
        self.vehicle_models_data = self.config_data[MainKey.VEHICLES]
        self.base_station_models_data = self.config_data[MainKey.BASE_STATIONS]
        self.controller_models_data = self.config_data[MainKey.CONTROLLERS]
        self.rsu_models_data = self.config_data[MainKey.ROADSIDE_UNITS]

    def create_output_directory(self) -> None:
        """
        Create the output directory.
        """
        logger.debug("Creating the output directory.")
        output_filepath: Path = Path(self.output_data[OutputKey.LOCATION])
        self._create_output_dir(output_filepath)

    def create_loggers(self) -> None:
        """
        Create the loggers.
        """
        output_data = self.config_data[MainKey.OUTPUT_SETTINGS]
        logging_level = Defaults.LOG_LEVEL
        if LogKey.LEVEL in output_data:
            logging_level = str(output_data[LogKey.LEVEL]).upper()

        log_overwrite = Defaults.LOG_OVERWRITE
        if LogKey.OVERWRITE in output_data and output_data[LogKey.OVERWRITE] == "yes":
            log_overwrite = True

        logging_filename = Defaults.LOG_FILE
        if LogKey.FILE in output_data:
            logging_filename = output_data[LogKey.FILE]

        logging_location = self.project_path
        if LogKey.LOCATION in output_data:
            logging_location = logging_location / (output_data[LogKey.LOCATION])

        logging_file = logging_location / logging_filename
        if not logging_file.exists():
            Path.mkdir(logging_location, parents=True, exist_ok=True)

        logger_config = LoggerConfig(logging_file, logging_level, log_overwrite)
        logger_config.setup_logger_config()

    def create_file_readers(self) -> None:
        """
        Read the input files.
        """
        logger.debug("Creating input file readers.")
        self._create_all_devices_file_readers()
        self._create_activation_file_readers()
        self._create_vehicle_links_file_readers()
        self._create_other_links_file_readers()

    def _create_all_devices_file_readers(self) -> None:
        """Create the file readers for all devices."""
        logger.debug("Creating file reader for vehicle trace file.")
        self._create_new_file_reader(
            FilenameKey.VEHICLE_TRACE,
            ColumnNames.VEHICLE_TRACES,
            ColumnDTypes.VEHICLE_TRACES,
        )

        logger.debug("Creating file reader for base stations file.")
        self._create_new_file_reader(
            FilenameKey.BASE_STATIONS,
            ColumnNames.BASE_STATIONS,
            ColumnDTypes.BASE_STATIONS,
        )

        logger.debug("Creating file reader for controllers file.")
        self._create_new_file_reader(
            FilenameKey.CONTROLLERS, ColumnNames.CONTROLLERS, ColumnDTypes.CONTROLLERS
        )

        logger.debug("Creating file reader for roadside units file.")
        self._create_new_file_reader(
            FilenameKey.ROADSIDE_UNITS,
            ColumnNames.ROADSIDE_UNITS,
            ColumnDTypes.ROADSIDE_UNITS,
        )

    def _create_activation_file_readers(self) -> None:
        """Create the file readers for all activation files."""
        input_files = self.config_data[MainKey.INPUT_FILES]
        logger.debug("Creating file reader for vehicle activation times file.")
        self._create_new_file_reader(
            FilenameKey.VEHICLE_ACTIVATIONS,
            ColumnNames.ACTIVATION_TIMES,
            ColumnDTypes.ACTIVATION_TIMES,
        )

        if input_files[FilenameKey.BASE_STATION_ACTIVATIONS] != "":
            logger.debug("Creating file reader for base station activations file.")
            self._create_new_file_reader(
                FilenameKey.BASE_STATION_ACTIVATIONS,
                ColumnNames.ACTIVATION_TIMES,
                ColumnDTypes.ACTIVATION_TIMES,
            )
        else:
            self._create_none_file_reader(FilenameKey.BASE_STATION_ACTIVATIONS)

        if input_files[FilenameKey.CONTROLLER_ACTIVATIONS] != "":
            logger.debug("Creating file reader for controller activations file.")
            self._create_new_file_reader(
                FilenameKey.CONTROLLER_ACTIVATIONS,
                ColumnNames.ACTIVATION_TIMES,
                ColumnDTypes.ACTIVATION_TIMES,
            )
        else:
            self._create_none_file_reader(FilenameKey.CONTROLLER_ACTIVATIONS)

        if input_files[FilenameKey.RSU_ACTIVATIONS] != "":
            logger.debug("Creating file reader for roadside unit activations file.")
            self._create_new_file_reader(
                FilenameKey.RSU_ACTIVATIONS,
                ColumnNames.ACTIVATION_TIMES,
                ColumnDTypes.ACTIVATION_TIMES,
            )
        else:
            self._create_none_file_reader(FilenameKey.RSU_ACTIVATIONS)

    def _create_vehicle_links_file_readers(self) -> None:
        """Create the file readers for all vehicle links files."""
        logger.debug("Creating file reader for v2v links file.")
        self._create_new_file_reader(
            FilenameKey.V2V_LINKS, ColumnNames.V2V_LINKS, ColumnDTypes.V2V_LINKS
        )

        logger.debug("Creating file reader for v2b links file.")
        self._create_new_file_reader(
            FilenameKey.V2B_LINKS, ColumnNames.V2B_LINKS, ColumnDTypes.V2B_LINKS
        )

        logger.debug("Creating file reader for v2r links file.")
        self._create_new_file_reader(
            FilenameKey.V2R_LINKS, ColumnNames.V2R_LINKS, ColumnDTypes.V2R_LINKS
        )

    def _create_other_links_file_readers(self) -> None:
        """Create the file readers for all other links files."""
        logger.debug("Creating file reader for b2c links file.")
        self._create_new_file_reader(
            FilenameKey.B2C_LINKS, ColumnNames.B2C_LINKS, ColumnDTypes.B2C_LINKS
        )

        logger.debug("Creating file reader for r2r links file.")
        self._create_new_file_reader(
            FilenameKey.R2R_LINKS, ColumnNames.R2R_LINKS, ColumnDTypes.R2R_LINKS
        )

        logger.debug("Creating file reader for r2b links file.")
        self._create_new_file_reader(
            FilenameKey.R2B_LINKS, ColumnNames.R2B_LINKS, ColumnDTypes.R2B_LINKS
        )

    def _create_new_file_reader(
        self, file_key: str, column_names: list[str], column_dtypes: dict
    ) -> None:
        """
        Create a new file reader.

        Parameters
        ----------
        file_key : str
            The file key.
        column_names : list[str]
            The column names.
        column_dtypes : dict
            The column data types.
        """
        input_files = self.config_data[MainKey.INPUT_FILES]
        file_path = self.project_path / input_files[file_key]

        if not file_path.exists():
            logger.error(f"File {file_path} does not exist.")
            exit(1)

        logger.debug(f"Creating file reader for file {file_path}.")
        if file_path.suffix.endswith(FileExtension.PARQUET):
            self.file_readers[file_key] = ParquetDataReader(
                file_path, column_names, column_dtypes
            )
        elif file_path.suffix.endswith(FileExtension.CSV):
            self.file_readers[file_key] = CSVDataReader(
                file_path, column_names, column_dtypes
            )
        else:
            raise UnsupportedInputFormatError(file_path.suffix)

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
        output_dir : Path
            The relative path to the output directory.
        """
        self._output_dir = self.project_path / output_dir
        if not output_dir.exists():
            Path.mkdir(output_dir, parents=True, exist_ok=True)

        logger.debug("Output directory: %s", self._output_dir)
