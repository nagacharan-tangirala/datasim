from src.setup.SConfigXMLReader import ConfigDict

from src.setup.SEntityFactory import EntityFactory
from src.setup.SSensorFactory import SensorFactory
from src.setup.SNodeFactory import NodeFactory
from src.setup.SControllerFactory import ControllerFactory


class ParticipantFactory:
    def __init__(self, config_dict: ConfigDict):
        """
        Initialize the participant factory object.

        Parameters
        ----------
        config_dict : ConfigDict
            Dictionary containing the parameters for the participants in the simulation.
        """
        self.config_dict = config_dict

        # Create the factories needed to create the participants.
        self._node_factory = NodeFactory()
        self._sensor_factory = SensorFactory()
        self._entity_factory = EntityFactory()
        self._controller_factory = ControllerFactory()

        # Create the dictionaries to store the participants in the simulation
        self.sensors = {}
        self.nodes = {}
        self.entities = {}
        self.controllers = {}

    def create_participants(self):
        """
        Create the participants in the simulation.
        """
        # First create the sensors and nodes.
        self._create_sensors()
        self._create_nodes()

        # Create the nodes and entities in the simulation. Order does not matter for these.
        self._create_entities()
        self._create_controllers()

    def get_nodes(self) -> dict:
        """
        Get the nodes in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the nodes.
        """
        return self.nodes

    def get_entities(self) -> dict:
        """
        Get the entities in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the entities in the simulation.
        """
        return self.entities

    def _create_sensors(self):
        """
        Create the sensors in the simulation.
        """
        for sensor_id, sensor_params in self.config_dict.sensor_params.items():
            self.sensors[sensor_id] = self._sensor_factory.create_sensor(sensor_params)

    def _create_nodes(self):
        """
        Create the nodes in the simulation.
        """
        for node_id, node_params in self.config_dict.node_params.items():
            self.nodes[node_id] = self._node_factory.create_node(node_params)

    def _create_entities(self):
        """
        Create the entities in the simulation.
        """
        for entity_id, entity_params in self.config_dict.entity_params.items():
            # Check if the sensors specified for the entity are present in the simulation.
            sensor_list = entity_params.get('sensors', None)
            if sensor_list is None:
                raise ValueError("No sensors specified for entity {}".format(entity_id))

            # Get the list of sensors for the entity.
            entity_sensors = {}
            for sensor_id in sensor_list:
                if sensor_id not in self.sensors:
                    raise ValueError("Sensor {} not found in the simulation.".format(sensor_id))
                entity_sensors[sensor_id] = self.sensors[sensor_id]

            self.entities[entity_id] = self._entity_factory.create_entity(entity_params, entity_sensors)

    def _create_controllers(self):
        """
        Create the controllers in the simulation.
        """
        for controller_id, controller_params in self.config_dict.controller_params.items():
            # Check if the nodes specified for the controller are present in the simulation.
            node_list = controller_params.get('nodes', None)
            if node_list is None:
                raise ValueError("No nodes specified for controller {}".format(controller_id))

            # If node list is empty, then the controller is centralized and is associated with all the nodes in the simulation.
            controller_nodes = {}
            if len(node_list) > 0:
                controller_nodes = self.nodes
            else:
                # Get the list of nodes for the controller.
                for node_id in node_list:
                    if node_id not in self.nodes:
                        raise ValueError("Node {} not found in the simulation.".format(node_id))
                    controller_nodes[node_id] = self.nodes[node_id]

            self.controllers[controller_id] = self._controller_factory.create_controller(controller_params, controller_nodes)