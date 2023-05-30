from src.setup.SConfigReaderH5 import ConfigDict

from src.setup.SDeviceFactory import DeviceFactory
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
        self._device_factory = DeviceFactory()
        self._controller_factory = ControllerFactory()

        # Create the dictionaries to store the participants in the simulation
        self.sensors = {}
        self.nodes = {}
        self.agents = {}
        self.controllers = {}

    def get_nodes(self) -> dict:
        """
        Get the nodes in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the nodes.
        """
        return self.nodes

    def create_participants_of_type(self, participant_type: str):
        """
        Create the participants of the given type in the simulation.

        Parameters
        ----------
        participant_type : str
            The type of participant to create.
        """
        if participant_type == 'node':
            self._create_nodes()
        elif participant_type == 'controller':
            self._create_controllers()
        elif participant_type == 'agent':
            self._create_agents()
        else:
            raise ValueError("Participant type not valid.")

    def get_controllers(self) -> dict:
        """
        Get the controllers in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the controllers.
        """
        return self.controllers

    def get_agents(self) -> dict:
        """
        Get the agents in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the agents in the simulation.
        """
        return self.agents

    def get_sensors(self) -> dict:
        """
        Get the sensors in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the sensors in the simulation.
        """
        return self.sensors

    def _create_nodes(self):
        """
        Create the nodes in the simulation.
        """
        for node_id, node_params in self.config_dict.node_params.items():
            self.nodes[node_id] = self._node_factory.create_node(node_params)

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

    def _create_agents(self):
        """
        Create the agents in the simulation.
        """
        for agent_id, agent_params in self.config_dict.agent_params.items():
            # Check if the sensors specified for the agent are present in the simulation.
            sensor_list = agent_params.get('sensors', None)
            if sensor_list is None:
                raise ValueError("No sensors specified for agent {}".format(agent_id))

            # Get the list of sensors for the agent.
            sensor_params = {}
            for sensor_id in sensor_list:
                if sensor_id not in self.config_dict.sensor_params:
                    raise ValueError("Sensor {} not found in the input data.".format(sensor_id))
                sensor_params[sensor_id] = self.config_dict.sensor_params[sensor_id]

            # Create the agent.
            self.agents[agent_id] = self._device_factory.create_agent(agent_params, sensor_params)

