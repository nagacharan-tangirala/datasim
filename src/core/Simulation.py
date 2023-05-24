from src.setup.SParticipantFactory import ParticipantFactory
from src.setup.SConfigReader import ConfigHDF5Reader
from src.device.MAgent import AgentModel


class Simulation:
    def __init__(self, config_file: str):
        """
        Initialize the simulation setup object. This class is responsible for setting up the simulation.
        """
        self.config_file = config_file
        self.config_dict = None

        # Create the dictionaries to store the participants in the simulation
        self.nodes = {}
        self.sensors = {}

        # Simulation parameters
        self.start_time = 0
        self.end_time = 0
        self.step_size = 0
        self.seed = 0
        self.update_step = 0
        self.output_dir = 0
        self.output_step = 0

    def setup_simulation(self):
        """
        Set up the simulation.
        """
        self._perform_initial_steps()
        self._create_participants()
        self._create_simulation()

    def _perform_initial_steps(self):
        """
        Set up the simulation according to the type of simulation.
        """
        self._read_config()
        self._get_simulation_parameters()

    def _read_config(self):
        """
        Read the config file and store the parsed parameters in the config dict.
        """
        # Create the config reader and read the config file
        config_reader = ConfigHDF5Reader(self.config_file)

        config_reader.read_config()

        # Get the parsed config params
        self.config_dict = config_reader.get_config_dict()

    def _get_simulation_parameters(self):
        """
        Get the simulation parameters.
        """
        simulation_parameters = self.config_dict.simulation_params

        self.start_time = int(simulation_parameters['start'] * 3600 * 1000)
        self.end_time = int(simulation_parameters['end'] * 3600 * 1000)
        self.step_size = simulation_parameters['step']
        self.seed = simulation_parameters['seed']
        self.update_step = simulation_parameters['update_step']
        self.output_dir = simulation_parameters['output_dir']
        self.output_step = simulation_parameters['output_step']

    def _create_participants(self):
        """
        Create the participants in the simulation. These are the non-mesa agents.
        """
        # Create a participant factory object and create the participants
        participant_factory = ParticipantFactory(self.config_dict)
        participant_factory.create_participants_of_type('node')
        participant_factory.create_participants_of_type('agent')
        participant_factory.create_participants_of_type('controller')

        # Get the nodes and agents
        self.nodes = participant_factory.get_nodes()
        self.agents = participant_factory.get_agents()

    def _create_simulation(self):
        """
        Create the agent model.
        """
        self.model = AgentModel(self.config_dict.simulation_params, self.agents)

    def run(self):
        """
        Run the simulation.
        """
        self.model.run()
