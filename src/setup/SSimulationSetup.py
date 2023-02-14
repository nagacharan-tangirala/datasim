from abc import ABCMeta, abstractmethod

from src.setup.SParticipantFactory import ParticipantFactory
from src.setup.SConfigXMLReader import ConfigReader


class SimulationSetup(metaclass=ABCMeta):
    def __init__(self, config_xml: str):
        """
        Initialize the simulation setup object. This class is responsible for setting up the simulation.
        """
        self.config_xml = config_xml
        self.lead_factory = None
        self.config_dict = None

        # Create the dictionaries to store the participants in the simulation
        self.sensors = {}
        self.nodes = {}
        self.entities = {}

    def setup_simulation(self):
        """
        Setup the simulation. This includes following steps -

            1. Read the config file to parse parameters for the participants in the simulation.
            2. Create the participants in the simulation.

        """
        # 1.
        self.read_config()

        # 2.
        self.create_participants()

    def read_config(self):
        """
        Read the config file.
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
        # Create the lead factory object to use for creating the participants.
        self.lead_factory = ParticipantFactory()

        # Create the participants
        self._create_sensors()
        self._create_nodes()
        self._create_entities()

    def _create_sensors(self):
        """
        Create the sensors in the simulation.
        """
        for sensor_id, sensor_params in self.config_dict.sensor_params.items():
            self.sensors[sensor_id] = self.lead_factory.create_sensor(sensor_params)

    def _create_nodes(self):
        """
        Create the nodes in the simulation.
        """
        for node_id, node_params in self.config_dict.node_params.items():
            self.nodes[node_id] = self.lead_factory.create_node(node_params)

    def _create_entities(self):
        """
        Create the entities in the simulation.
        """
        for entity_id, entity_params in self.config_dict.entity_params.items():
            self.entities[entity_id] = self.lead_factory.create_entity(entity_params)
