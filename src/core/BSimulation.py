from abc import ABCMeta, abstractmethod

from typing import Dict

from src.setup.SConfigHDF5Reader import ConfigHDF5Reader

from src.core.SSimModelFactory import SimModelFactory


class SimulationBase(metaclass=ABCMeta):
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

    def _create_models(self):
        """
        Create the models required for the simulation.
        """
        # Create the model factory
        model_factory = SimModelFactory()

        # Create the coverage model
        self.coverage_model = model_factory.create_coverage_model(self.config_dict.model_params['coverage'])

    @abstractmethod
    def run(self):
        """
        Run the simulation based on the parameters read from the config file.
        """
        pass
