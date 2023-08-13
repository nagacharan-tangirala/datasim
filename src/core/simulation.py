import logging

from pandas import DataFrame
from tqdm import tqdm

import src.core.common_constants as cc
import src.core.constants as constants
from core.sim_model import SimModel
from output.agent_data import *
from output.model_data import *
from src.core.exceptions import UnsupportedInputFormatError
from src.orchestrator.cloud_orchestrator import CloudOrchestrator
from src.orchestrator.edge_orchestrator import EdgeOrchestrator
from src.output.writer_factory import OutputWriterFactory
from src.setup.device_factory import DeviceFactory
from src.setup.file_reader import ParquetDataReader, CSVDataReader
from src.setup.input_helper import SimulationInputHelper

logger = logging.getLogger(__name__)


class Simulation:
    def __init__(self, config_file: str) -> None:
        """
        Initialize the simulation object.

        Parameters
        ----------
        config_file : str
            The path to the config file.
        """
        self.config_file: str = config_file

        self._device_factory: DeviceFactory | None = None

        # Devices in the simulation
        self._vehicles: dict = {}
        self._base_stations: dict = {}
        self._controllers: dict = {}

        # Main simulation model
        self._simulation_model: SimModel | None = None

        # Orchestrators
        self.edge_orchestrator: EdgeOrchestrator | None = None
        self.cloud_orchestrator: CloudOrchestrator | None = None

        # Simulation parameters
        self.start_time: int = -1
        self.end_time: int = -1
        self.time_step: int = -1
        self.current_time: int = -1
        self.data_stream_interval: int = -1

        # Helper to read input data
        self.sim_input_helper: SimulationInputHelper | None = None

        # Activation data
        self._vehicle_activations_data: DataFrame = DataFrame()
        self._base_station_activations_data: DataFrame = DataFrame()
        self._controller_activations_data: DataFrame = DataFrame()

        # Progress bar
        self._progress_bar: tqdm | None = None

        # Output writers
        self._model_output_writer: ModelOutputParquet | ModelOutputCSV | None = None
        self._agent_output_writer: AgentOutputParquet | AgentOutputCSV | None = None

    def setup_simulation(self) -> None:
        """
        Set up the simulation.
        """
        self._read_config()
        self._perform_initial_setup()

        logger.info("Reading simulation parameters.")
        self._read_simulation_parameters()

        logger.info("Reading activation data from trace files.")
        self._read_activations_data()

        logger.info("Streaming the first chunk of the input data.")
        self._read_first_chunk_input_data()

        logger.info("Creating devices.")
        self._create_devices()

        logger.info("Creating edge and cloud orchestrators.")
        self._create_orchestrators()

        logger.info("Creating output writers.")
        self._create_output_writers()

        logger.info("Creating device model.")
        self._create_simulation_model()

        logger.info("Initializing simulation.")

    def _read_config(self) -> None:
        """
        Read the config file and store the parsed parameters in the config dict.
        """
        # Create the config reader and read the config file
        self.sim_input_helper = SimulationInputHelper(self.config_file)
        self.sim_input_helper.read_config_file()

    def _perform_initial_setup(self) -> None:
        """
        Perform the initial setup.
        """
        # Create the loggers
        self.sim_input_helper.create_loggers()

        # Read the simulation and model settings
        logger.debug("Reading simulation and model settings.")
        self.sim_input_helper.read_simulation_and_model_settings()

        # Create the output directory
        logger.debug("Creating the output directory.")
        self.sim_input_helper.create_output_directory()

        # Create the file readers
        logger.debug("Creating the file readers.")
        self.sim_input_helper.create_file_readers()

    def _read_simulation_parameters(self) -> None:
        """
        Read the simulation parameters.
        """
        # Get the simulation parameters
        simulation_data = self.sim_input_helper.simulation_data

        self.start_time: int = simulation_data[constants.SIMULATION_START_TIME]
        self.end_time: int = simulation_data[constants.SIMULATION_END_TIME]
        self.time_step: int = simulation_data[constants.SIMULATION_TIME_STEP]
        self.data_stream_interval: int = simulation_data[
            constants.DATA_STREAMING_INTERVAL
        ]

        self.current_time: int = self.start_time

        logger.debug("Simulation parameters: ")
        logger.debug(f"Start time: {self.start_time}")
        logger.debug(f"End time: {self.end_time}")
        logger.debug(f"Time step: {self.time_step}")
        logger.debug(f"Data streaming interval: {self.data_stream_interval}")
        logger.debug(f"Current time: {self.current_time}")

    def _read_activations_data(self) -> None:
        """
        Read the activation input data.
        """
        self._vehicle_activations_data = self._read_file(
            self.sim_input_helper.file_readers[cc.VEHICLE_ACTIVATIONS_FILE]
        )
        self._base_station_activations_data = self._read_file(
            self.sim_input_helper.file_readers[cc.BASE_STATION_ACTIVATIONS_FILE]
        )
        self._controller_activations_data = self._read_file(
            self.sim_input_helper.file_readers[cc.CONTROLLER_ACTIVATIONS_FILE]
        )

    def _read_file(
        self, data_reader: ParquetDataReader | CSVDataReader | None
    ) -> DataFrame:
        """
        Read the input data from the file.

        Parameters
        ----------
        data_reader: FileReader
            The file reader object.

        Returns
        ----------
        DataFrame
            The input data.
        """
        if data_reader is None:
            return DataFrame()

        if data_reader.type == cc.CSV:
            logger.debug(f"Reading the entire data from {data_reader.input_file} file.")
            return data_reader.read_all_data()
        elif data_reader.type == cc.PARQUET:
            logger.debug(
                f"Reading partial data from {data_reader.input_file} file until timestamp {self.data_stream_interval}."
            )
            return data_reader.read_data_until_timestamp(self.data_stream_interval)
        else:
            raise UnsupportedInputFormatError(data_reader.input_file)

    def _create_devices(self) -> None:
        """
        Create the devices in the simulation.
        """
        # Create the device factory object.
        logger.debug("Creating the device factory.")
        self._device_factory = DeviceFactory(
            self._vehicle_activations_data,
            self._base_station_activations_data,
            self._controller_activations_data,
            self.start_time,
            self.end_time,
        )

        # Create a device factory object and create the participants
        logger.debug("Creating the Vehicles")
        self._device_factory.create_vehicles(
            self.vehicle_trace_data, self.sim_input_helper.vehicle_models_data
        )

        logger.debug("Creating Base Stations.")
        self._device_factory.create_base_stations(
            self.base_stations_data, self.sim_input_helper.base_station_models_data
        )

        logger.debug("Creating the Controllers.")
        self._device_factory.create_controllers(
            self.controller_data, self.sim_input_helper.controller_models_data
        )

        # Get the devices from the factory
        self._vehicles = self._device_factory.vehicles
        self._base_stations = self._device_factory.base_stations
        self._controllers = self._device_factory.controllers

    def _create_orchestrators(self) -> None:
        """
        Create the orchestrators.
        """
        self.edge_orchestrator = EdgeOrchestrator(
            self.v2v_links_data,
            self.v2b_links_data,
            self.sim_input_helper.orchestrator_models_data[constants.EDGE_ORCHESTRATOR],
        )

        self.cloud_orchestrator = CloudOrchestrator(
            self.b2c_links_data,
            self.sim_input_helper.orchestrator_models_data[
                constants.CLOUD_ORCHESTRATOR
            ],
        )

    def _create_output_writers(self) -> None:
        """
        Create the output writers.
        """
        output_writer_factory = OutputWriterFactory(self.sim_input_helper.output_dir)
        self._model_output_writer = output_writer_factory.create_model_output_writer(
            self.sim_input_helper.output_data[constants.OUTPUT_TYPE]
        )

        self._agent_output_writer = output_writer_factory.create_agent_output_writer(
            self.sim_input_helper.output_data[constants.OUTPUT_TYPE]
        )

    def _create_simulation_model(self) -> None:
        """
        Create the main simulation model.
        """
        self._simulation_model = SimModel(
            self._vehicles,
            self._base_stations,
            self._controllers,
            self.edge_orchestrator,
            self.cloud_orchestrator,
            self.start_time,
            self.end_time,
        )

    def _create_progress_bar(self) -> None:
        """
        Create the progress bar.
        """
        self._progress_bar = tqdm(
            total=self.end_time,
            desc=constants.PROGRES_BAR_TITLE,
            ncols=constants.PROGRESS_BAR_WIDTH,
            unit=constants.PROGRESS_BAR_UNIT,
            position=0,
            colour=constants.PROGRESS_BAR_COLOUR,
        )

    def _refresh_simulation_data(self) -> None:
        """
        Refresh the simulation data by reading the next chunk of data.
        """
        self._stream_next_input_data()
        self._update_devices_with_new_data()
        self._update_orchestrators_with_new_data()

    def _read_first_chunk_input_data(self) -> None:
        """
        Read the input data for the first time.
        """
        self.vehicle_trace_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[cc.VEHICLE_TRACE_FILE]
        )
        self.v2v_links_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[cc.V2V_LINKS_FILE]
        )
        self.base_stations_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[cc.BASE_STATIONS_FILE]
        )
        self.v2b_links_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[cc.V2B_LINKS_FILE]
        )
        self.controller_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[cc.CONTROLLERS_FILE]
        )
        self.b2c_links_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[cc.B2C_LINKS_FILE]
        )

    def _read_first_chunk(
        self, data_reader: CSVDataReader | ParquetDataReader
    ) -> DataFrame:
        """
        Read the first chunk of the input data. CSVs are read completely while parquet
        files are read partially.

        Parameters
        ----------
        data_reader: InputDataReader
            The input data reader object.

        Returns
        ----------
        DataFrame
            The input data.
        """
        if data_reader.type == cc.CSV:
            return data_reader.read_all_data()
        elif data_reader.type == cc.PARQUET:
            return data_reader.read_data_until_timestamp(
                self.current_time + self.data_stream_interval
            )
        else:
            raise UnsupportedInputFormatError(data_reader.input_file)

    def _update_devices_with_new_data(self) -> None:
        """
        Update the devices with the newly streamed data.
        """
        if not self.vehicle_trace_data.empty:
            self._device_factory.create_new_vehicles(
                self.vehicle_trace_data, self.sim_input_helper.vehicle_models_data
            )
            updated_vehicles = self._device_factory.vehicles
            self._simulation_model.update_vehicles(updated_vehicles)

        if not self.base_stations_data.empty:
            self._device_factory.create_new_base_stations(
                self.base_stations_data, self.sim_input_helper.base_station_models_data
            )
            updated_base_stations = self._device_factory.base_stations
            self._simulation_model.update_base_stations(updated_base_stations)

        if not self.controller_data.empty:
            self._device_factory.create_new_controllers(
                self.controller_data, self.sim_input_helper.controller_models_data
            )
            updated_controllers = self._device_factory.controllers
            self._simulation_model.update_controllers(updated_controllers)

        self._simulation_model.save_device_activation_times()

    def _update_orchestrators_with_new_data(self) -> None:
        """
        Update the cloud and edge orchestrators with the newly streamed data.
        """
        if not self.v2v_links_data.empty:
            self.edge_orchestrator.update_v2v_links(self.v2v_links_data)

        if not self.v2b_links_data.empty:
            self.edge_orchestrator.update_v2b_links(self.v2b_links_data)

        if not self.b2c_links_data.empty:
            self.cloud_orchestrator.update_b2c_links(self.b2c_links_data)

    def _stream_next_input_data(self) -> None:
        """
        Refresh the input data until the next streaming interval.
        """
        self.vehicle_trace_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[cc.VEHICLE_TRACE_FILE]
        )
        self.v2v_links_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[cc.V2V_LINKS_FILE]
        )
        self.base_stations_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[cc.BASE_STATIONS_FILE]
        )
        self.v2b_links_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[cc.V2B_LINKS_FILE]
        )
        self.controller_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[cc.CONTROLLERS_FILE]
        )
        self.b2c_links_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[cc.B2C_LINKS_FILE]
        )

    def _read_next_chunk(
        self, data_reader: CSVDataReader | ParquetDataReader
    ) -> DataFrame:
        """
        Read the next chunk of the input data. Only parquet files are read partially.

        Parameters
        ----------
        data_reader: InputDataReader
            The input data reader object.

        Returns
        ----------
        DataFrame
            The input data.
        """
        if data_reader.type == cc.CSV:
            return DataFrame()
        elif data_reader.type == cc.PARQUET:
            return data_reader.read_data_until_timestamp(
                self.current_time + self.data_stream_interval
            )
        else:
            raise UnsupportedInputFormatError(data_reader.input_file)

    def run(self) -> None:
        """
        Run the simulation.
        """
        logger.info("Performing final setup.")
        self._simulation_model.perform_final_setup()

        logger.debug("Creating the progress bar.")
        self._create_progress_bar()

        logger.info("Starting the simulation.")
        while self.current_time < self.end_time:
            self._progress_bar.update(self.time_step)
            self.step()

        logger.info("Simulation completed.")

    def step(self) -> None:
        """
        Step the simulation.
        """
        self._simulation_model.current_time = self.current_time
        self._simulation_model.step()

        # Update the time.
        self.current_time += self.time_step

        # Refresh the simulation data if the current time is a multiple of the data stream interval.
        if self.current_time % self.data_stream_interval == 0:
            logger.info(f"Refreshing simulation data at time {self.current_time}.")
            self._refresh_simulation_data()

    def save_simulation_results(self) -> None:
        """
        Save the simulation results.
        """
        logger.info("Saving simulation results.")
        model_level_data = (
            self._simulation_model.data_collector.get_model_vars_dataframe()
        )

        agent_level_data = (
            self._simulation_model.data_collector.get_agent_vars_dataframe()
        )

        self._agent_output_writer.write_output(agent_level_data)
        self._model_output_writer.write_output(model_level_data)
