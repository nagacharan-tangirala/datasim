from abc import ABCMeta

from typing import Dict

from src.setup.SParticipantFactory import ParticipantFactory
from src.setup.SConfigXMLReader import ConfigReader

from src.device.BEntity import EntityBase

from src.output.SOutputFactory import OutputFactory


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
        self.entities: Dict[int, EntityBase] = {}

        # Keep track of the active entities
        self.active_entities = []

        # Create a dictionary to store the activation times of the entities
        self.update_time_entities_map = {}

        # Simulation parameters
        self.start_time = 0
        self.end_time = 0
        self.step_size = 0
        self.seed = 0
        self.update_step = 0
        self.output_dir = 0
        self.output_step = 0

        # Output dictionaries
        self.entities_output = {}
        self.nodes_output = {}

    def setup_simulation(self):
        """
        Set up the simulation. This includes following steps -

            1. Read the config file to parse parameters for the participants in the simulation.
            2. Create the participants in the simulation.
            3. Get the main participants required for the simulation. The sub-components are updated by the main participants.

        """
        # 1.
        self._read_config()

        # 2.
        self._create_participants()

        # 3.
        self._get_main_participants()

        # 4.
        self._get_simulation_parameters()

        # 5.
        self._do_initial_setup()

    def _read_config(self):
        """
        Read the config file and store the parsed parameters in the config dict.
        """
        # Create the config reader and read the config file
        config_reader = ConfigReader(self.config_xml)
        config_reader.read_config()

        # Get the parsed config params
        self.config_dict = config_reader.get_parsed_config_params()

    def _create_participants(self):
        """
        Create the participants in the simulation.
        """
        # Create the participant factory object to use for creating the participants. Pass the config dict to the factory.
        self.participant_factory = ParticipantFactory(self.config_dict)

        # Create the participants in the simulation.
        self.participant_factory.create_participants()

    def _get_main_participants(self):
        """
        Get the main participants required for the simulation. The subcomponents are updated by the main participants.
        """
        # Get the nodes and entities
        self.nodes = self.participant_factory.get_nodes()
        self.entities = self.participant_factory.get_entities()

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

    def _do_initial_setup(self):
        """
        Do the initial setup for the simulation. This includes following steps -

            1. Set the seed for the random number generator.
            2. Prepare a dictionary with time step as the key and the respective entities to activate in that time step.
            3. Prepare the output dictionaries to store the output of the simulation.
        """
        # 1.
        self._set_seed()

        # 2.
        self._prepare_active_entities_dict()

        # 3.
        self._prepare_output()

    def _set_seed(self):
        """
        Set the seed for the random number generator.
        """
        pass

    def _prepare_active_entities_dict(self):
        """
        Prepare a dictionary with time step as the key and the respective entities to activate in that time step.
        """
        for entity in self.entities.values():
            start_time, end_time = entity.get_start_and_end_time()
            # Add the entity to the dictionary with the start time as the key
            if start_time not in self.update_time_entities_map:
                self.update_time_entities_map[start_time] = [entity]
            else:
                self.update_time_entities_map[start_time].append(entity)

            # Add the entity to the dictionary with the end time as the key
            if end_time not in self.update_time_entities_map:
                self.update_time_entities_map[end_time] = [entity]
            else:
                self.update_time_entities_map[end_time].append(entity)

    def _prepare_output(self):
        """
        Prepare the output dictionaries to store the output of the simulation.
        """
        # Create the output helper object
        self.output_helper = OutputFactory().get_output_helper(self.config_dict)

        # Prepare the output dictionaries
        for time_step in range(self.start_time, self.end_time, self.step_size):
            self.entities_output[time_step] = {}
            self.nodes_output[time_step] = {}

    def run(self):
        """
        Run the simulation based on the parameters read from the config file.
        """
        for time_step in range(self.start_time, self.end_time, self.step_size):
            # Run a single step of the simulation
            self._run_step(time_step)

            # Run the update step if it is time to do so
            if time_step > 0 and time_step % self.update_step == 0:
                self._run_update_step(time_step)

            # Run the output step if it is time to do so
            if time_step > 0 and time_step % self.output_step == 0:
                self._run_output_step(time_step)

    def _run_step(self, time_step: int):
        """
        Run a single step of the simulation. All the regular steps are run in this method.
        - Update the active entities list for the current time step
        - Process the entities and nodes in the simulation

        Parameters
        ----------
        time_step : int
            The time step of the simulation.
        """
        # Update active entities
        self._update_active_entities(time_step)

        # Process the entities and nodes
        self._process_entities_and_nodes(time_step)

    def _process_entities_and_nodes(self, time_step: int):
        """
        Process the entities and nodes in the simulation at the given time step.

        Parameters
        ----------
        time_step : int
            The time step of the simulation.
        """
        # Update the entities and compute the total sensor data size collected by the entities
        for entity in self.active_entities:
            # Process this entity
            entity.process_entity(time_step)

            # Get the sensor data volume collected by this entity
            self.entities_output[time_step][entity.get_id()] = entity.get_total_sensor_data_size()

        # Update the nodes and compute the total sensor data size collected by the nodes
        for node in self.nodes.values():
            # Process this node
            node.process_node(time_step)

            # Get the sensor data volume collected by this node
            self.nodes_output[time_step][node.get_id()] = node.get_collected_data_size()

    def _update_active_entities(self, time_step: int):
        """
        Update the active entities in the simulation at the given time step.
        If the time for activation/deactivation of an entity has come, then activate/deactivate the entity.
        Only retain the active entities in the list of active entities and remove the inactive entities.

        Parameters
        ----------
        time_step : int
            The time step of the simulation.
        """
        # Only proceed if there are any updates to perform at the current time step.
        if time_step not in self.update_time_entities_map:
            return

        entities_to_update = self.update_time_entities_map[time_step]
        for entity in entities_to_update:
            entity.toggle_entity_status()
            if entity.is_entity_active():
                self.active_entities.append(entity)
            else:
                self.active_entities.remove(entity)

    def _run_update_step(self, time_step: int):
        """
        Run the update step of the simulation. All the update steps are run in this method. This method is called less frequently to reduce the computational load.
        1. Update the network topology. This includes associating the nodes with the entities.

        Parameters
        ----------
        time_step : int
            The time step of the simulation.
        """
        print('Update step: ' + str(time_step) + ' skipped for now')

    def _run_output_step(self, time_step: int):
        """
        Run the output step, all the outputs are written to the output directory. This method is called less frequently to reduce I/O bottleneck.

        Parameters
        ----------
        time_step : int
            The time step of the simulation.
        """
        # Write the output to the output directory
        self.output_helper.write_output(time_step, self.entities_output[time_step], self.nodes_output[time_step])
        print('Output step: ' + str(time_step))
