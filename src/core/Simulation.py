from src.channel.MAgentChannelModel import AgentChannelModel
from src.channel.MControllerChannelModel import ControllerChannelModel
from src.channel.MNodeChannelModel import NodeChannelModel
from src.device.MAgentModel import AgentModel
from src.device.MControllerModel import ControllerModel
from src.device.MNodeModel import NodeModel
from src.setup.SDeviceFactory import DeviceFactory
from src.setup.SSimulationSetup import SimulationSetup


class Simulation:
    def __init__(self, config_file: str):
        """
        Initialize the simulation setup object. This class is responsible for setting up the simulation.
        """
        self.config_file: str = config_file

        # Create the dictionaries to store the agents in the simulation
        self.agents: dict = {}
        self.nodes: dict = {}
        self.controllers: dict = {}

        # Create objects to store device models
        self.agent_model: AgentModel | None = None
        self.node_model: NodeModel | None = None
        self.controller_model: ControllerModel | None = None

        # Create objects to store channel models
        self.node_channel_model: NodeChannelModel | None = None
        self.agent_channel_model: AgentChannelModel | None = None
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
        device_factory.create_nodes(self.sim_config.node_data)
        device_factory.create_agents(self.sim_config.agent_data, self.sim_config.coverage_data)
        device_factory.create_controllers(self.sim_config.controller_data)

        # Get the devices from the factory
        self.nodes = device_factory.get_nodes()
        self.agents = device_factory.get_agents()
        self.controllers = device_factory.get_controllers()

    def _create_device_models(self) -> None:
        """
        Create the device models.
        """
        self.agent_model = AgentModel(self.agents, self.sim_config.model_data['agent'])
        self.node_model = NodeModel(self.nodes, self.sim_config.node_link_data, self.sim_config.model_data['node'])
        self.controller_model = ControllerModel(self.controllers, self.sim_config.controller_link_data, self.sim_config.model_data['controller'])

    def _create_channel_models(self) -> None:
        """
        Create the channel models.
        """
        # Create the channel models
        self.agent_channel_model = AgentChannelModel(self.nodes)
        self.node_channel_model = NodeChannelModel(self.nodes)
        self.controller_channel_model = ControllerChannelModel(self.nodes)

        # Get the channels from the device models and add them to the channel models.
        self.agent_channel_model.add_channel(self.agent_model.get_agent_channel())
        self.node_channel_model.add_channel(self.node_model.get_node_channel())
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
        self.agent_model.step(self.time_step)
        self.agent_channel_model.step()

        self.node_model.step()
        self.node_channel_model.step()
        self.controller_channel_model.step()

        self.controller_model.step()

        self.current_time += self.time_step
