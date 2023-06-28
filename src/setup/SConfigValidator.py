import logging
from os.path import exists, join

from src.core.Constants import *
from src.core.CustomExceptions import KeyMissinginConfigError

logger = logging.getLogger(__name__)


class ConfigSettingsValidator:
    def __init__(self, config_data: dict, file_path: str):
        self.config_data = config_data
        self.file_path = file_path

    def validate(self):
        """
        Validate the JSON file.
        """
        self._check_for_main_keys()
        logger.info("All main keys are present.")
        self._check_for_input_files()
        logger.info("All the input files are given and exist.")
        self._validate_simulation_settings()
        logger.info("The simulation settings are valid.")
        self._validate_ues()
        logger.info("The UEs are valid.")

    def _check_for_main_keys(self):
        """
        Check if the JSON file contains all the main keys.
        """
        main_keys = [P_INPUT_FILES, P_SIMULATION_SETTINGS, P_UES, P_CELL_TOWERS, P_CONTROLLERS, P_WIRED_CHANNEL, P_WIRELESS_CHANNEL]
        for main_key in main_keys:
            if main_key not in self.config_data:
                raise KeyMissinginConfigError(main_key)

    def _check_for_input_files(self):
        """
        Check if the JSON file contains all the input files keys.
        """
        input_files_keys = [P_UE_TRACE_FILE, P_UE_LINKS_FILE, P_CELL_TOWER_LINKS_FILE, P_CELL_TOWERS_FILE, P_CONTROLLERS_FILE, P_CONTROLLER_LINKS_FILE]
        for input_files_key in input_files_keys:
            if input_files_key not in self.config_data[P_INPUT_FILES]:
                raise KeyMissinginConfigError(input_files_key)

            input_file_path = join(self.file_path, self.config_data[P_INPUT_FILES][input_files_key])
            if not exists(input_file_path):
                raise FileNotFoundError(input_file_path)

    def _validate_simulation_settings(self):
        """
        Validate the simulation settings.
        """
        simulation_settings_keys = [P_SIMULATION_START_TIME, P_SIMULATION_END_TIME, P_SIMULATION_TIME_STEP, P_DATA_STREAMING_INTERVAL, P_OUTPUT_TYPE, P_LOGGING_LEVEL, P_LOG_FILE, P_OUTPUT_LOCATION]
        for simulation_settings_key in simulation_settings_keys:
            if simulation_settings_key not in self.config_data[P_SIMULATION_SETTINGS]:
                raise KeyMissinginConfigError(simulation_settings_key)

        # Check if the simulation start time is less than the simulation end time
        if self.config_data[P_SIMULATION_SETTINGS][P_SIMULATION_START_TIME] >= self.config_data[P_SIMULATION_SETTINGS][P_SIMULATION_END_TIME]:
            raise ValueError("The simulation start time is greater than or equal to the simulation end time.")

        # Check if the simulation time step is greater than zero
        if self.config_data[P_SIMULATION_SETTINGS][P_SIMULATION_TIME_STEP] <= 0:
            raise ValueError("The simulation time step is less than or equal to zero.")

        # Check if the data streaming interval is greater than zero
        if self.config_data[P_SIMULATION_SETTINGS][P_DATA_STREAMING_INTERVAL] <= 0:
            raise ValueError("The data streaming interval is less than or equal to zero.")

    def _validate_ues(self):
        """
        Validate the UE settings.
        """
        # Check if the UE keys are integers
        for ue_id in self.config_data[P_UES]:
            # Convert the UE ID to integer
            try:
                int(ue_id)
            except ValueError:
                raise ValueError("The UE ID is not an integer.")
