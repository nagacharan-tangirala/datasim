from src.channel.MCellTowerChannelModel import CellTowerChannelModel
from src.channel.MControllerChannelModel import ControllerChannelModel
from src.channel.MUEChannelModel import UEChannelModel
from src.device.MCellTowerModel import CellTowerModel
from src.device.MControllerModel import ControllerModel
from src.device.MUEModel import UEModel
from src.setup.SDeviceFactory import DeviceFactory
from src.setup.SSimulationSetup import SimulationSetup


class Simulation:
    def __init__(self, config_file: str):
        """
        Initialize the simulation setup object. This class is responsible for setting up the simulation.
        """
        self.config_file: str = config_file

        # Create the dictionaries to store the devices in the simulation
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
        self._create_devices()
        self._create_device_models()
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

        self.start_time: int = simulation_data['start'] * 3600 * 1000
        self.end_time: int = simulation_data['end'] * 3600 * 1000
        self.time_step: int = simulation_data['step']
        self.output_dir: str = simulation_data['output_dir']

        self.current_time: int = self.start_time

    def _create_devices(self) -> None:
        """
        Create the devices in the simulation.
        """
        # Create a device factory object and create the participants
        device_factory = DeviceFactory()
        device_factory.create_cell_towers(self.sim_config.cell_tower_data)
        device_factory.create_ues(self.sim_config.ue_data, self.sim_config.coverage_data, self.sim_config.ue_type_data)
        device_factory.create_controllers(self.sim_config.controller_data)

        # Get the devices from the factory
        self.cell_towers = device_factory.get_cell_towers()
        self.ues = device_factory.get_ues()
        self.controllers = device_factory.get_controllers()

    def _create_device_models(self) -> None:
        """
        Create the device models.
        """
        self.ue_model = UEModel(self.ues, self.sim_config.model_data['ue'])
        self.cell_tower_model = CellTowerModel(self.cell_towers, self.sim_config.cell_tower_link_data, self.sim_config.model_data['cell_tower'])
        self.controller_model = ControllerModel(self.controllers, self.sim_config.controller_link_data, self.sim_config.model_data['controller'])

    def _create_channel_models(self) -> None:
        """
        Create the channel models.
        """
        # Create the channel models
        self.ue_channel_model = UEChannelModel(self.cell_towers)
        self.cell_tower_channel_model = CellTowerChannelModel(self.cell_towers)
        self.controller_channel_model = ControllerChannelModel(self.cell_towers)

        # Get the channels from the device models and add them to the channel models.
        self.ue_channel_model.add_channel(self.ue_model.get_ue_channel())
        self.cell_tower_channel_model.add_channel(self.cell_tower_model.get_cell_tower_channel())
        self.controller_channel_model.add_channel(self.controller_model.get_controller_channel())

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
        self.ue_channel_model.step()

        self.cell_tower_model.step()
        self.cell_tower_channel_model.step()
        self.controller_channel_model.step()

        self.controller_model.step()

        self.current_time += self.time_step
