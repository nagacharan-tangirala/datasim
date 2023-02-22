from abc import ABCMeta

from src.setup.SParticipantFactory import ParticipantFactory
from src.setup.SConfigXMLReader import ConfigReader


class Simulation(metaclass=ABCMeta):
    def __init__(self, config_xml: str):
        """
        Initialize the simulation setup object. This class is responsible for setting up the simulation.
        """
        self.config_xml = config_xml
        self.participant_factory = None
        self.config_dict = None

        # Create the dictionaries to store the participants in the simulation
        self.nodes = {}
        self.entities = {}

        # Simulation parameters
        self.start_time = 0
        self.end_time = 0
        self.step_size = 0
        self.seed = 0
        self.lazy_step = 0
        self.output_dir = 0

    def setup_simulation(self):
        """
        Setup the simulation. This includes following steps -

            1. Read the config file to parse parameters for the participants in the simulation.
            2. Create the participants in the simulation.
            3. Get the main participants required for the simulation. The sub-components are updated by the main participants.

        """
        # 1.
        self.read_config()

        # 2.
        self.create_participants()

        # 3.
        self.get_main_participants()

        # 4.
        self.get_simulation_parameters()

    def read_config(self):
        """
        Read the config file and store the parsed parameters in the config dict.
        """
        # Create the config reader and read the config file
        config_reader = ConfigReader(self.config_xml)
        config_reader.read_config()

        # Get the parsed config params
        self.config_dict = config_reader.get_parsed_config_params()

    def create_participants(self):
        """
        Create the participants in the simulation.
        """
        # Create the participant factory object to use for creating the participants. Pass the config dict to the factory.
        self.participant_factory = ParticipantFactory(self.config_dict)

        # Create the participants in the simulation.
        self.participant_factory.create_participants()

    def get_main_participants(self):
        """
        Get the main participants required for the simulation. The sub-components are updated by the main participants.
        """
        # Get the nodes and entities
        self.nodes = self.participant_factory.get_nodes()
        self.entities = self.participant_factory.get_entities()

    def get_simulation_parameters(self):
        """
        Get the simulation parameters.
        """
        simulation_parameters = self.config_dict['simulation']

        self.start_time = simulation_parameters['start']
        self.end_time = simulation_parameters['end']
        self.step_size = simulation_parameters['step']
        self.seed = simulation_parameters['seed']
        self.lazy_step = simulation_parameters['lazy_step']
        self.output_dir = simulation_parameters['output_dir']

    def run(self):
        """
        Run a single step of the simulation.
        """
        for time_step in range(self.start_time, self.end_time, self.step_size):
            # Run a single step of the simulation
            self._run_step(time_step)

            # Run the lazy step if required
            if self.lazy_step % time_step == 0:
                self._run_lazy_step(time_step)

    def _run_step(self, time_step: int):
        """
        Run a single step of the simulation.
        """
        raise NotImplementedError

    def _run_lazy_step(self, time_step: int):
        """
        Run the lazy step of the simulation.
        """
        raise NotImplementedError
