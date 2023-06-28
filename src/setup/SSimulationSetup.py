import json
import logging
from os import makedirs
from os.path import dirname, exists, join

from src.core.Constants import *
from src.core.CustomExceptions import *
from src.core.LoggerConfig import LoggerConfig
from src.setup.SCSVDataReader import CSVDataReader
from src.setup.SConfigValidator import ConfigSettingsValidator
from src.setup.SInputDataReader import InputDataReader
from src.setup.SParquetDataReader import ParquetDataReader

logger = logging.getLogger(__name__)


class SimulationSetup:
    def __init__(self, config_file: str):
        """
        Initialize the config reader.

        Parameters
        ----------
        config_file : str
            The path to the configuration file.
        """
        self.config_file: str = config_file
        self.config_data: dict = {}
        self.project_path: str = dirname(config_file)

        self.file_readers: dict[str, InputDataReader] = {}

        self.ue_models_data: dict = {}
        self.cell_tower_models_data: dict = {}
        self.controller_models_data: dict = {}

        self.channel_model_data: dict = {}
        self.simulation_data: dict = {}
        self.json_validator: dict = {}

    def read_input_file(self) -> None:
        """
        Read the config file.
        """
        with open(self.config_file, 'r') as f:
            self.config_data = json.load(f)

        self._create_loggers()

        # Validate the config file.
        config_validator = ConfigSettingsValidator(self.config_data, self.project_path)
        config_validator.validate()

        # Read the input files.
        self._read_input_files(self.config_data[P_INPUT_FILES])

        # Read simulation settings.
        self.simulation_data = self.config_data[P_SIMULATION_SETTINGS]

        # Read the channel models.
        self.channel_model_data['wireless'] = self.config_data[P_WIRELESS_CHANNEL]
        self.channel_model_data['wired'] = self.config_data[P_WIRED_CHANNEL]

        # Read the devices.
        self.ue_models_data = self.config_data[P_UES]
        self.cell_tower_models_data = self.config_data[P_CELL_TOWERS]
        self.controller_models_data = self.config_data[P_CONTROLLERS]

    def _create_loggers(self) -> None:
        """
        Create the loggers.
        """
        logging_level = "INFO"
        if P_LOGGING_LEVEL in self.config_data[P_SIMULATION_SETTINGS]:
            logging_level = str(self.config_data[P_SIMULATION_SETTINGS][P_LOGGING_LEVEL]).upper()

        logging_filename = "simulation.log"
        if P_LOG_FILE in self.config_data[P_SIMULATION_SETTINGS]:
            logging_filename = self.config_data[P_SIMULATION_SETTINGS][P_LOG_FILE]

        logging_file = join(self.project_path, logging_filename)
        if not exists(dirname(logging_file)):
            makedirs(dirname(logging_file))

        logger_config = LoggerConfig(logging_file, logging_level)
        logger_config.setup_logger_config()
        logger.debug("Reading the config file.")

    def _read_input_files(self, input_files: dict) -> None:
        """
        Read the input files.

        Parameters
        ----------
        input_files : Element
            The input files element.
        """
        self._read_ue_trace(input_files[P_UE_TRACE_FILE])
        self._read_ue_links(input_files[P_UE_LINKS_FILE])
        self._read_cell_towers(input_files[P_CELL_TOWERS_FILE])
        self._read_tower_links(input_files[P_CELL_TOWER_LINKS_FILE])
        self._read_controllers(input_files[P_CONTROLLERS_FILE])
        self._read_controller_links(input_files[P_CONTROLLER_LINKS_FILE])

    def _read_ue_trace(self, ue_trace_filename: str) -> None:
        """
        Read the ues trace data.

        Parameters
        ----------
        ue_trace_filename : str
            The ue trace filename.
        """
        # Get the path to the ue trace file and the file type
        ue_trace_file = join(self.project_path, ue_trace_filename)
        file_type = ue_trace_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers[P_UE_TRACE_FILE] = ParquetDataReader(ue_trace_file, P_UE_TRACE_COLUMN_NAMES, P_UE_TRACE_COLUMN_DTYPES)
            case 'csv':
                self.file_readers[P_UE_TRACE_FILE] = CSVDataReader(ue_trace_file, P_UE_TRACE_COLUMN_NAMES, P_UE_TRACE_COLUMN_DTYPES)
            case _:
                raise UnsupportedInputFormatError(file_type)

    def _read_ue_links(self, ue_links_filename: str) -> None:
        """
        Read the UE links data.

        Parameters
        ----------
        ue_links_filename : str
            The UE links filename.
        """
        # Get the path to the ue links file and the file type
        ue_links_file = join(self.project_path, ue_links_filename)
        file_type = ue_links_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers[P_UE_LINKS_FILE] = ParquetDataReader(ue_links_file, P_UE_LINKS_COLUMN_NAMES, P_UE_LINKS_COLUMN_DTYPES)
            case 'csv':
                self.file_readers[P_UE_LINKS_FILE] = CSVDataReader(ue_links_file, P_UE_LINKS_COLUMN_NAMES, P_UE_LINKS_COLUMN_DTYPES)
            case _:
                raise UnsupportedInputFormatError(file_type)

    def _read_cell_towers(self, cell_towers_filename: str) -> None:
        """
        Read the cell towers data from the CSV file.

        Parameters
        ----------
        cell_towers_filename : str
            The cell towers filename.
        """
        # Get the path to the cell towers file and the file type
        cell_towers_file = join(self.project_path, cell_towers_filename)
        file_type = cell_towers_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers[P_CELL_TOWERS_FILE] = ParquetDataReader(cell_towers_file, P_CELL_TOWER_COLUMN_NAMES, P_CELL_TOWER_COLUMN_DTYPES)
            case 'csv':
                self.file_readers[P_CELL_TOWERS_FILE] = CSVDataReader(cell_towers_file, P_CELL_TOWER_COLUMN_NAMES, P_CELL_TOWER_COLUMN_DTYPES)
            case _:
                raise UnsupportedInputFormatError(file_type)

    def _read_controllers(self, controller_filename: str) -> None:
        """
        Read the controllers data from the CSV file.

        Parameters
        ----------
        controller_filename : str
            The controllers filename.
        """
        # Get the path to the controllers file and the file type
        controller_file = join(self.project_path, controller_filename)
        file_type = controller_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers[P_CONTROLLERS_FILE] = ParquetDataReader(controller_file, P_CONTROLLERS_COLUMN_NAMES, P_CONTROLLERS_COLUMN_DTYPES)
            case 'csv':
                self.file_readers[P_CONTROLLERS_FILE] = CSVDataReader(controller_file, P_CONTROLLERS_COLUMN_NAMES, P_CONTROLLERS_COLUMN_DTYPES)
            case _:
                raise UnsupportedInputFormatError(file_type)

    def _read_controller_links(self, controller_links_filename: str) -> None:
        """
        Read the links data from the links CSV file.

        Parameters
        ----------
        controller_links_filename : str
            The links filename.
        """
        # Get the path to the links file and the file type
        controller_links_file = join(self.project_path, controller_links_filename)
        file_type = controller_links_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers[P_CONTROLLER_LINKS_FILE] = ParquetDataReader(controller_links_file, P_CONTROLLER_LINKS_COLUMN_NAMES, P_CONTROLLER_LINKS_COLUMN_DTYPES)
            case 'csv':
                self.file_readers[P_CONTROLLER_LINKS_FILE] = CSVDataReader(controller_links_file, P_CONTROLLER_LINKS_COLUMN_NAMES, P_CONTROLLER_LINKS_COLUMN_DTYPES)
            case _:
                raise UnsupportedInputFormatError(file_type)

    def _read_tower_links(self, tower_links_filename: str) -> None:
        """
        Read the tower links data from the CSV file.

        Parameters
        ----------
        tower_links_filename : str
            The tower links filename.
        """
        tower_links_file = join(self.project_path, tower_links_filename)

        # Get the file type
        file_type = tower_links_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers[P_CELL_TOWER_LINKS_FILE] = ParquetDataReader(tower_links_file, P_CELL_TOWER_LINKS_COLUMN_NAMES, P_CELL_TOWER_LINKS_COLUMN_DTYPES)
            case 'csv':
                self.file_readers[P_CELL_TOWER_LINKS_FILE] = CSVDataReader(tower_links_file, P_CELL_TOWER_LINKS_COLUMN_NAMES, P_CELL_TOWER_LINKS_COLUMN_DTYPES)
            case _:
                raise UnsupportedInputFormatError(file_type)

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
        return output_dir
