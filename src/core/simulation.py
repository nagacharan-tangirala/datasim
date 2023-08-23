import logging
from pathlib import Path

from core.sim_model import SimModel
from pandas import DataFrame
from tqdm import tqdm

from output.agent_data import AgentOutputCSV, AgentOutputParquet
from output.model_data import ModelOutputCSV, ModelOutputParquet
from src.core.common_constants import FileExtension, FilenameKey
from src.core.constants import (
    MainKey,
    OutputKey,
    ProgressBar,
    ProgressBarWidth,
    SimTimes,
)
from src.core.exceptions import UnsupportedInputFormatError
from src.orchestrator.cloud_orchestrator import CloudOrchestrator
from src.orchestrator.edge_orchestrator import EdgeOrchestrator
from src.output.writer_factory import OutputWriterFactory
from src.setup.device_factory import DeviceFactory
from src.setup.file_reader import CSVDataReader, ParquetDataReader
from src.setup.input_helper import SimulationInputHelper

logger = logging.getLogger(__name__)


class Simulation:
    def __init__(self, config_filepath: Path) -> None:
        """
        Initialize the simulation object.

        Parameters
        ----------
        config_filepath : Path
            The path to the config file.
        """
        self.config_filepath: Path = config_filepath

        self._device_factory: DeviceFactory | None = None

        self._vehicles: dict = {}
        self._base_stations: dict = {}
        self._controllers: dict = {}
        self._roadside_units: dict = {}

        self._simulation_model: SimModel | None = None

        self.edge_orchestrator: EdgeOrchestrator | None = None
        self.cloud_orchestrator: CloudOrchestrator | None = None

        self.start_time: int = -1
        self.end_time: int = -1
        self.time_step: int = -1
        self.current_time: int = -1
        self.data_stream_interval: int = -1

        self.sim_input_helper: SimulationInputHelper | None = None

        self._vehicle_activations_data: DataFrame = DataFrame()
        self._base_station_activations_data: DataFrame = DataFrame()
        self._controller_activations_data: DataFrame = DataFrame()

        self._progress_bar: tqdm | None = None

        self._model_output_writer: ModelOutputParquet | ModelOutputCSV | None = None
        self._agent_output_writer: AgentOutputParquet | AgentOutputCSV | None = None

    def setup_simulation(self) -> None:
        """
        Set up the simulation.
        """
        self._read_config()
        self._perform_initial_setup()
        self._read_input_data()
        self._create_simulation_entities()
        self._create_simulation_model()
        self._simulation_model.do_model_setup()

    def _read_config(self) -> None:
        """
        Creates the input helper and reads the config file.
        """
        self.sim_input_helper = SimulationInputHelper(self.config_filepath)
        self.sim_input_helper.read_config_file()

    def _perform_initial_setup(self) -> None:
        """
        Carry out initial setup tasks.
        """
        self.sim_input_helper.create_loggers()

        logger.debug("Reading simulation and model settings.")
        self.sim_input_helper.read_simulation_and_model_settings()

        logger.debug("Creating the output directory.")
        self.sim_input_helper.create_output_directory()

        logger.debug("Creating the file readers.")
        self.sim_input_helper.create_file_readers()

    def _read_input_data(self) -> None:
        """
        Read the input data.
        """
        logger.info("Reading simulation parameters.")
        self._read_simulation_parameters()

        logger.info("Reading activation data from trace files.")
        self._read_activations_data()

        logger.info("Streaming the first chunk of the input data.")
        self._read_first_chunk_input_data()

    def _create_simulation_entities(self) -> None:
        """
        Create the entities in the simulation.
        """
        logger.info("Creating devices.")
        self._create_devices()

        logger.info("Creating edge and cloud orchestrators.")
        self._create_orchestrators()

        logger.info("Creating output writers.")
        self._create_output_writers()

    def _read_simulation_parameters(self) -> None:
        """
        Read the simulation parameters.
        """
        simulation_data = self.sim_input_helper.simulation_data

        self.start_time: int = simulation_data[SimTimes.START]
        self.end_time: int = simulation_data[SimTimes.END]
        self.time_step: int = simulation_data[SimTimes.STEP]
        self.data_stream_interval: int = simulation_data[
            SimTimes.DATA_STREAMING_INTERVAL
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
            self.sim_input_helper.file_readers[FilenameKey.VEHICLE_ACTIVATIONS]
        )
        self._base_station_activations_data = self._read_file(
            self.sim_input_helper.file_readers[FilenameKey.BASE_STATION_ACTIVATIONS]
        )
        self._controller_activations_data = self._read_file(
            self.sim_input_helper.file_readers[FilenameKey.CONTROLLER_ACTIVATIONS]
        )
        self._rsu_activations_data = self._read_file(
            self.sim_input_helper.file_readers[FilenameKey.RSU_ACTIVATIONS]
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
        -------
        DataFrame
            The input data.
        """
        if data_reader is None:
            return DataFrame()

        if data_reader.type == FileExtension.CSV:
            logger.debug(f"Reading the entire data from {data_reader.input_file} file.")
            return data_reader.read_all_data()
        elif data_reader.type == FileExtension.PARQUET:
            logger.debug(
                f"Reading partial data from {data_reader.input_file} file "
                f"until timestamp {self.data_stream_interval}."
            )
            return data_reader.read_data_until_timestamp(self.data_stream_interval)
        else:
            raise UnsupportedInputFormatError(data_reader.input_file)

    def _create_devices(self) -> None:
        """
        Create the devices in the simulation.
        """
        logger.debug("Creating the device factory.")
        self._device_factory = DeviceFactory(
            self._vehicle_activations_data,
            self._base_station_activations_data,
            self._controller_activations_data,
            self._rsu_activations_data,
            self.start_time,
            self.end_time,
        )

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

        logger.debug("Creating the RSUs.")
        self._device_factory.create_roadside_units(
            self.rsu_data, self.sim_input_helper.rsu_models_data
        )

        self._vehicles = self._device_factory.vehicles
        self._base_stations = self._device_factory.base_stations
        self._controllers = self._device_factory.controllers
        self._roadside_units = self._device_factory.roadside_units

    def _create_orchestrators(self) -> None:
        """
        Create the orchestrators.
        """
        self.edge_orchestrator = EdgeOrchestrator(
            self.v2v_links_data,
            self.v2b_links_data,
            self.v2r_links_data,
            self.r2b_links_data,
            self.r2r_links_data,
            self.sim_input_helper.orchestrator_models_data[MainKey.EDGE_ORCHESTRATOR],
        )

        self.cloud_orchestrator = CloudOrchestrator(
            self.b2c_links_data,
            self.sim_input_helper.orchestrator_models_data[MainKey.CLOUD_ORCHESTRATOR],
        )

    def _create_output_writers(self) -> None:
        """
        Create the output writers.
        """
        output_writer_factory = OutputWriterFactory(self.sim_input_helper.output_dir)
        self._model_output_writer = output_writer_factory.create_model_output_writer(
            self.sim_input_helper.output_data[OutputKey.TYPE]
        )

        self._agent_output_writer = output_writer_factory.create_agent_output_writer(
            self.sim_input_helper.output_data[OutputKey.TYPE]
        )

    def _create_simulation_model(self) -> None:
        """
        Create the main simulation model.
        """
        logger.info("Creating simulation model.")
        self._simulation_model = SimModel(
            self._vehicles,
            self._base_stations,
            self._controllers,
            self._roadside_units,
            self.edge_orchestrator,
            self.cloud_orchestrator,
            self.sim_input_helper.space_settings,
            self.start_time,
            self.end_time,
        )

    def _create_progress_bar(self) -> None:
        """
        Create the progress bar.
        """
        self._progress_bar = tqdm(
            total=self.end_time,
            desc=ProgressBar.SIM_RUNNING_MESSAGE,
            unit=ProgressBar.SIM_PROGRESS_UNIT,
            ncols=ProgressBarWidth.SIM,
            position=0,
            colour=ProgressBar.RUNNING_COLOUR,
        )

    def _refresh_simulation_data(self) -> None:
        """
        Refresh the simulation data by reading the next chunk of data.
        """
        logger.info(f"Refreshing simulation data at time {self.current_time}.")
        self._pause_progress_bar()
        self._stream_next_input_data()
        self._update_devices_with_new_data()
        self._update_orchestrators_with_new_data()
        self._resume_progress_bar()

    def _read_first_chunk_input_data(self) -> None:
        """
        Read the input data for the first time.
        """
        self.vehicle_trace_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[FilenameKey.VEHICLE_TRACE]
        )
        self.v2v_links_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[FilenameKey.V2V_LINKS]
        )
        self.base_stations_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[FilenameKey.BASE_STATIONS]
        )
        self.v2b_links_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[FilenameKey.V2B_LINKS]
        )
        self.controller_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[FilenameKey.CONTROLLERS]
        )
        self.b2c_links_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[FilenameKey.B2C_LINKS]
        )
        self.rsu_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[FilenameKey.ROADSIDE_UNITS]
        )
        self.v2r_links_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[FilenameKey.V2R_LINKS]
        )
        self.r2r_links_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[FilenameKey.R2R_LINKS]
        )
        self.r2b_links_data = self._read_first_chunk(
            self.sim_input_helper.file_readers[FilenameKey.R2B_LINKS]
        )

    def _read_first_chunk(
        self, data_reader: CSVDataReader | ParquetDataReader
    ) -> DataFrame:
        """
        Read the first chunk of the input data.

        CSVs are read completely while parquet files are read partially.

        Parameters
        ----------
        data_reader: InputDataReader
            The input data reader object.

        Returns
        -------
        DataFrame
            The input data.
        """
        if data_reader.type == FileExtension.CSV:
            return data_reader.read_all_data()
        elif data_reader.type == FileExtension.PARQUET:
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
            new_vehicles = self._device_factory.vehicles
            self._simulation_model.append_new_vehicles(new_vehicles)

        if not self.rsu_data.empty:
            self._device_factory.create_new_roadside_units(
                self.rsu_data, self.sim_input_helper.rsu_models_data
            )
            new_roadside_units = self._device_factory.roadside_units
            self._simulation_model.append_new_roadside_units(new_roadside_units)

        if not self.base_stations_data.empty:
            self._device_factory.create_new_base_stations(
                self.base_stations_data, self.sim_input_helper.base_station_models_data
            )
            new_base_stations = self._device_factory.base_stations
            self._simulation_model.append_new_base_stations(new_base_stations)

        if not self.controller_data.empty:
            self._device_factory.create_new_controllers(
                self.controller_data, self.sim_input_helper.controller_models_data
            )
            new_controllers = self._device_factory.controllers
            self._simulation_model.append_new_controllers(new_controllers)

        self._simulation_model.save_device_activation_times()

    def _update_orchestrators_with_new_data(self) -> None:
        """
        Update the cloud and edge orchestrators with the newly streamed data.
        """
        if not self.v2v_links_data.empty:
            self.edge_orchestrator.update_v2v_links(self.v2v_links_data)

        if not self.v2b_links_data.empty:
            self.edge_orchestrator.update_v2b_links(self.v2b_links_data)

        if not self.v2r_links_data.empty:
            self.edge_orchestrator.update_v2r_links(self.v2r_links_data)

        if not self.b2c_links_data.empty:
            self.cloud_orchestrator.update_b2c_links(self.b2c_links_data)

    def _stream_next_input_data(self) -> None:
        """
        Refresh the input data until the next streaming interval.
        """
        self.vehicle_trace_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[FilenameKey.VEHICLE_TRACE]
        )
        self.v2v_links_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[FilenameKey.V2V_LINKS]
        )
        self.base_stations_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[FilenameKey.BASE_STATIONS]
        )
        self.v2b_links_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[FilenameKey.V2B_LINKS]
        )
        self.v2r_links_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[FilenameKey.V2R_LINKS]
        )
        self.controller_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[FilenameKey.CONTROLLERS]
        )
        self.rsu_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[FilenameKey.ROADSIDE_UNITS]
        )
        self.b2c_links_data = self._read_next_chunk(
            self.sim_input_helper.file_readers[FilenameKey.B2C_LINKS]
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
        -------
        DataFrame
            The input data.
        """
        if data_reader.type == FileExtension.CSV:
            return DataFrame()
        elif data_reader.type == FileExtension.PARQUET:
            return data_reader.read_data_until_timestamp(
                self.current_time + self.data_stream_interval
            )
        else:
            raise UnsupportedInputFormatError(data_reader.input_file)

    def run(self) -> None:
        """
        Run the simulation.
        """
        logger.debug("Creating the progress bar.")
        self._create_progress_bar()

        logger.info("Starting the simulation.")
        while self.current_time < self.end_time:
            self._progress_bar.update(self.time_step)
            self.step()

        self._close_progress_bar()

    def step(self) -> None:
        """
        Step the simulation.
        """
        self._simulation_model.current_time = self.current_time
        self._simulation_model.step()

        # Update the time.
        self.current_time += self.time_step

        # Refresh the simulation data if it is time to do so.
        if self.current_time % self.data_stream_interval == 0:
            self._refresh_simulation_data()

    def _pause_progress_bar(self) -> None:
        """
        Pause the progress bar.
        """
        self._progress_bar.colour = ProgressBar.PAUSED_COLOUR
        self._progress_bar.set_description_str(ProgressBar.SIM_PAUSED_MESSAGE)
        self._progress_bar.disable = True

    def _resume_progress_bar(self) -> None:
        """
        Resume the progress bar.
        """
        self._progress_bar.disable = False
        self._progress_bar.colour = ProgressBar.RUNNING_COLOUR
        self._progress_bar.set_description_str(ProgressBar.SIM_RUNNING_MESSAGE)

    def _close_progress_bar(self) -> None:
        """
        Close the progress bar.
        """
        self._progress_bar.set_description_str(ProgressBar.SIM_DONE_MESSAGE)
        self._progress_bar.colour = ProgressBar.DONE_COLOUR
        self._progress_bar.close()

    def save_simulation_results(self) -> None:
        """
        Save the simulation results.
        """
        logger.info("Last step - Saving simulation results.")
        file_progress_bar = self._create_file_progress_bar()

        model_level_data = (
            self._simulation_model.data_collector.get_model_vars_dataframe()
        )
        self._model_output_writer.write_output(model_level_data)

        agent_level_data = (
            self._simulation_model.data_collector.get_agent_vars_dataframe()
        )
        self._agent_output_writer.write_output(agent_level_data)
        file_progress_bar.update(n=1)

        file_progress_bar.set_description_str(ProgressBar.SAVE_DONE_MESSAGE)
        file_progress_bar.colour = ProgressBar.DONE_COLOUR
        file_progress_bar.close()
        logger.info("Done.")

    @staticmethod
    def _create_file_progress_bar() -> tqdm:
        """
        Create the file progress bar.
        """
        return tqdm(
            total=2,
            desc=ProgressBar.SAVE_STARTING_MESSAGE,
            ncols=ProgressBarWidth.FILE_SAVE,
            unit=str(ProgressBar.SAVE_PROGRESS_UNIT),
            smoothing=1,
            initial=1,
            colour=str(ProgressBar.RUNNING_COLOUR),
        )
