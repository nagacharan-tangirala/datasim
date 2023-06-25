import pandas as pd
from pandas import DataFrame

from src.channel.MCellTowerChannelModel import CellTowerChannelModel
from src.channel.MControllerChannelModel import ControllerChannelModel
from src.channel.MUEChannelModel import UEChannelModel
from src.core.CustomExceptions import UnsupportedInputFormatError
from src.device.MCellTowerModel import CellTowerModel
from src.device.MControllerModel import ControllerModel
from src.device.MUEModel import UEModel
from src.setup.SDeviceFactory import DeviceFactory
from src.setup.SInputDataReader import InputDataReader
from src.setup.SSimulationSetup import SimulationSetup


class Simulation:
    def __init__(self, config_file: str):
        """
        Initialize the simulation setup object. This class is responsible for setting up the simulation.
        """
        self.config_file: str = config_file

        # Create the dictionaries to store the devices in the simulation
        self.device_factory: DeviceFactory = DeviceFactory()
        self.ues: dict = {}
        self.cell_towers: dict = {}
        self.controllers: dict = {}

        # Create objects to store device models
        self.ue_model: UEModel | None = None
        self.cell_tower_model: CellTowerModel | None = None
        self.controller_model: ControllerModel | None = None

        # Create objects to store channel models
        self.cell_tower_channel_model: CellTowerChannelModel | None = None
        self.ue_channel_model: UEChannelModel | None = None
        self.controller_channel_model: ControllerChannelModel | None = None

    def setup_simulation(self) -> None:
        """
        Set up the simulation.
        """
        self._read_config()
        self._read_simulation_parameters()
        self._read_initial_input_data()
        self._create_devices_and_models()
        self._create_channel_models()

    def _read_config(self) -> None:
        """
        Read the config file and store the parsed parameters in the config dict.
        """
        # Create the config reader and read the config file
        self.sim_config = SimulationSetup(self.config_file)
        self.sim_config.read_input_file()

    def _read_simulation_parameters(self) -> None:
        """
        Initialize the controller model.
        """
        # Get the simulation parameters
        simulation_data = self.sim_config.simulation_data

        self.start_time: int = simulation_data['start']
        self.end_time: int = simulation_data['end']
        self.time_step: int = simulation_data['step']
        self.output_dir: str = simulation_data['output_dir']
        self.chunk_time_step: int = simulation_data['chunk_ts']

        self.current_time: int = self.start_time

    def _read_initial_input_data(self) -> None:
        """
        Read the CSV input data.
        """
        self.ue_trace_data = self._read_file(self.sim_config.file_readers['ue_trace'])
        self.ue_links_data = self._read_file(self.sim_config.file_readers['ue_links'])
        self.cell_tower_data = self._read_file(self.sim_config.file_readers['cell_tower'])
        self.cell_tower_links_data = self._read_file(self.sim_config.file_readers['cell_tower_links'])
        self.controller_data = self._read_file(self.sim_config.file_readers['controller'])
        self.controller_links_data = self._read_file(self.sim_config.file_readers['controller_links'])

    def _read_file(self, data_reader: InputDataReader) -> DataFrame:
        """
        Read the input data.

        Parameters
        ----------
        data_reader: FileReader
            The data reader object.

        Returns
        ----------
        DataFrame
            The input data.
        """
        match data_reader.get_type():
            case 'csv':
                return data_reader.read_all_data()
            case 'parquet':
                return data_reader.read_data_until_timestamp(self.chunk_time_step)
            case _:
                raise UnsupportedInputFormatError(data_reader.get_input_file())

    def _create_devices_and_models(self) -> None:
        """
        Create the devices in the simulation.
        """
        # Create a device factory object and create the participants
        self.device_factory.create_ues(self.ue_trace_data, self.sim_config.ue_models_data)
        self.device_factory.create_cell_towers(self.cell_tower_data, self.sim_config.cell_tower_models_data)
        self.device_factory.create_controllers(self.controller_data, self.sim_config.controller_models_data)

        # Get the devices from the factory
        self.ues = self.device_factory.get_ues()
        self.cell_towers = self.device_factory.get_cell_towers()
        self.controllers = self.device_factory.get_controllers()

        self.ue_model = UEModel(self.ues)
        self.cell_tower_model = CellTowerModel(self.cell_towers)
        self.controller_model = ControllerModel(self.controllers)

    def _create_channel_models(self) -> None:
        """
        Create the channel models.
        """
        # Create the channel models
        self.ue_channel_model = UEChannelModel(self.ue_links_data)
        self.cell_tower_channel_model = CellTowerChannelModel(self.cell_tower_links_data)
        self.controller_channel_model = ControllerChannelModel(self.controller_links_data)

    def _refresh_simulation(self) -> None:
        """
        Refresh the simulation.
        """
        self._get_next_input_data()
        self._update_devices_and_models()
        self._update_channel_models()

    def _get_next_input_data(self) -> None:
        """
        Refresh the input data.
        """
        self.ue_trace_data = self._read_next_chunk(self.sim_config.file_readers['ue_trace'])
        self.ue_links_data = self._read_next_chunk(self.sim_config.file_readers['ue_links'])
        self.cell_tower_data = self._read_next_chunk(self.sim_config.file_readers['cell_tower'])
        self.cell_tower_links_data = self._read_next_chunk(self.sim_config.file_readers['cell_tower_links'])
        self.controller_data = self._read_next_chunk(self.sim_config.file_readers['controller'])
        self.controller_links_data = self._read_next_chunk(self.sim_config.file_readers['controller_links'])

    def _update_devices_and_models(self) -> None:
        """
        Update the devices.
        """
        if not self.ue_trace_data.empty:
            self.device_factory.update_ues(self.ue_trace_data, self.sim_config.ue_models_data)
            updated_ues = self.device_factory.get_ues()
            self.ue_model.update_ues(updated_ues)

        if not self.cell_tower_data.empty:
            self.device_factory.update_cell_towers(self.cell_tower_data, self.sim_config.cell_tower_models_data)
            updated_cell_towers = self.device_factory.get_cell_towers()
            self.cell_tower_model.update_cell_towers(updated_cell_towers)

        if not self.controller_data.empty:
            self.device_factory.update_controllers(self.controller_data, self.sim_config.controller_models_data)
            updated_controllers = self.device_factory.get_controllers()
            self.controller_model.update_controllers(updated_controllers)

    def _update_channel_models(self) -> None:
        """
        Update the channel models.
        """
        if not self.ue_links_data.empty:
            self.ue_channel_model.update_ue_links(self.ue_links_data)

        if not self.cell_tower_links_data.empty:
            self.cell_tower_channel_model.update_cell_tower_links(self.cell_tower_links_data)

        if not self.controller_links_data.empty:
            self.controller_channel_model.update_controller_links(self.controller_links_data)

    def _read_next_chunk(self, data_reader: InputDataReader) -> DataFrame:
        """
        Read the next chunk of the input data.

        Parameters
        ----------
        data_reader: InputDataReader
            The input data reader object.

        Returns
        ----------
        DataFrame
            The input data.
        """
        match data_reader.get_type():
            case 'csv':
                return pd.DataFrame()
            case 'parquet':
                return data_reader.read_data_until_timestamp(self.current_time + self.chunk_time_step)
            case _:
                raise UnsupportedInputFormatError(data_reader.get_input_file())

    def run(self) -> None:
        """
        Run the simulation.
        """
        while self.current_time <= self.end_time:
            self.step()

    def step(self) -> None:
        """
        Step the simulation.
        """
        self.ue_model.step(self.current_time)
        self.ue_channel_model.step(self.current_time)

        self.cell_tower_model.step()
        self.cell_tower_channel_model.step()
        self.controller_channel_model.step()

        self.controller_model.step()

        self.current_time += self.time_step

        if self.current_time % self.chunk_time_step == 0:
            self._refresh_simulation()
