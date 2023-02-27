from os import makedirs
from os.path import exists, dirname, join
import xml.etree.ElementTree as Et

from typing import List, Dict


class ConfigDict:
    def __init__(self):
        self.sensor_params = {}
        self.node_params = {}
        self.entity_params = {}
        self.controller_params = {}
        self.simulation_params = {}


class ConfigReader:
    def __init__(self, config_file: str):
        self.config_root = Et.parse(config_file).getroot()
        self.project_path = dirname(config_file)

        # Create the objects to read and store input params
        self.config_dict = ConfigDict()

    def read_config(self):
        """Read the config file."""
        self._read_config()

    def get_parsed_config_params(self) -> ConfigDict:
        """
        Return the parsed configs.
        """
        return self.config_dict

    def _read_config(self):
        """
        Read the config file.
        """
        for child in self.config_root:
            if child.tag == 'sensors':
                self._read_sensor_xml(child.text)
            elif child.tag == 'nodes':
                self._read_nodes_xml(child.text)
            elif child.tag == 'entities':
                self._read_entities_xml(child.text)
            elif child.tag == 'control':
                self._read_control_xml(child.text)
            elif child.tag == 'simulation':
                self._read_simulation_params(child)
            else:
                raise ValueError('Invalid tag in config file: %s' % child.tag)

    def _read_sensor_xml(self, sensor_xml: str):
        """
        Read the sensor xml file and parse the parameters of the sensors.

        Parameters
        ----------
        sensor_xml : str
            The relative path to the sensor config file.
        """
        # Check if the file exists
        sensor_xml = join(self.project_path, sensor_xml)
        if not exists(sensor_xml):
            raise FileNotFoundError('Sensor config file not found: %s' % sensor_xml)

        # Read the file
        sensor_root = Et.parse(sensor_xml).getroot()
        for child in sensor_root:
            if child.tag == 'sensor':
                self._read_sensor_params(child)
            else:
                raise ValueError('Invalid tag in sensor config file: %s' % child.tag)

    def _read_sensor_params(self, sensor_data: Et.Element):
        """
        Read the parameters of a single sensor and store them in the config dict.

        Parameters
        ----------
        sensor_data : Et.Element
            The xml element containing the sensor parameters.
        """
        sensor_id = int(sensor_data.attrib['id'])
        sensor_params = {'type': sensor_data.attrib['type'], 'mode': sensor_data.attrib['mode']}

        # Read the sensor parameters
        for child in sensor_data:
            if child.tag == 'data_size':
                sensor_params['data_size'] = float(child.text)
            elif child.tag == 'start_time':
                sensor_params['start_time'] = int(child.text)
            elif child.tag == 'end_time':
                sensor_params['end_time'] = int(child.text)
            elif child.tag == 'frequency':
                sensor_params['frequency'] = int(child.text)
            elif child.tag == ['custom_times'] and sensor_params['mode'] == 'custom':
                sensor_params['custom_times'] = child.text
            else:
                raise ValueError('Invalid tag in sensor config file: %s' % child.tag)

        # Store the sensor params
        self.config_dict.sensor_params[sensor_id] = sensor_params

    def _read_nodes_xml(self, nodes_xml: str):
        """
        Read the nodes xml file and parse the parameters of the nodes.

        Parameters
        ----------
        nodes_xml : str
            The relative path to the node_params config file.
        """
        nodes_xml = join(self.project_path, nodes_xml)
        if not exists(nodes_xml):
            raise FileNotFoundError('Node config file not found: %s' % nodes_xml)
        root_xml = Et.parse(nodes_xml).getroot()
        for child in root_xml:
            if child.tag == 'node':
                self._read_node_params(child)
            else:
                raise ValueError('Invalid tag in node config file: %s' % child.tag)

    def _read_node_params(self, node_data: Et.Element):
        """
        Read the parameters of a single node and store them in the config dict.

        Parameters
        ----------
        node_data : Et.Element
            The node data element from the config file.
        """
        node_id = int(node_data.attrib['id'])
        node_params = {'id': node_id, 'type': node_data.attrib['type']}

        # Read the node parameters
        for child in node_data:
            if child.tag == 'location':
                node_params['location'] = child.text

        # Store the node params
        self.config_dict.node_params[node_id] = node_params

    def _read_entities_xml(self, entities_xml: str):
        """
        Read the entities xml file and parse the parameters of the entities.

        Parameters
        ----------
        entities_xml : str
            The relative path to the entity_params config file.
        """
        entities_xml = join(self.project_path, entities_xml)
        if not exists(entities_xml):
            raise FileNotFoundError('Entities config file not found: %s' % entities_xml)
        root_xml = Et.parse(entities_xml).getroot()
        for child in root_xml:
            if child.tag == 'entity':
                self._read_entity_params(child)
            else:
                raise ValueError('Invalid tag in entity_params config file: %s' % child.tag)

    def _read_entity_params(self, entity_data: Et.Element):
        """
        Read the parameters of a single entity and store them in the config dict.

        Parameters
        ----------
        entity_data : Et.Element
            The entity data element from the config file.
        """
        entity_id = int(entity_data.attrib['id'])
        entity_params = {'id': entity_id, 'type': entity_data.attrib['type'], 'start_time': entity_data.attrib['start_time'], 'end_time': entity_data.attrib['end_time']}

        # Read the entity parameters
        for child in entity_data:
            if child.tag == 'sensors':
                sensor_list = self._convert_string_to_list(child.text)
                entity_params['sensors'] = sensor_list
            elif child.tag == 'positions':
                position_list = self._parse_positions(child)
                entity_params['positions'] = position_list
            else:
                raise ValueError('Invalid tag in entities config file: %s' % child.tag)

        # Store the entity params
        self.config_dict.entity_params[entity_id] = entity_params

    @staticmethod
    def _convert_string_to_list(ids_string: str) -> List[int]:
        """
        Parse the string to convert it to a list of numbers.

        Parameters
        ----------
        ids_string : str
            The ids in the form of a string.

        Returns
        -------
        List[int]
            The list of sensor ids.
        """
        if len(ids_string) == 0:
            return []
        ids_string = ids_string.split(' ')
        ids_list = [int(each_id.strip()) for each_id in ids_string]
        return ids_list

    @staticmethod
    def _parse_positions(positions: Et.Element) -> Dict[int, List[float]]:
        """
        Parse the positions from the config file.

        Parameters
        ----------
        positions : str
            The positions in the config file.

        Returns
        -------
        Dict[int, List[float]]
            The list of positions with the time as key.
        """
        timed_positions = {}
        for child in positions:
            if child.tag == 'xy':
                position_time = int(child.attrib['time'])
                position = [float(x) for x in child.text.split(',')]
                timed_positions[position_time] = position
            else:
                raise ValueError('Invalid tag in positions data: %s' % child.tag)

        return timed_positions

    def _read_control_xml(self, control_xml: str):
        """
        Read the control xml file and parse the parameters of the traffic controller.

        Parameters
        ----------
        control_xml : str
            The relative path to the controller config file.
        """
        control_xml = join(self.project_path, control_xml)
        if not exists(control_xml):
            raise FileNotFoundError('Control config file not found: %s' % control_xml)
        root_xml = Et.parse(control_xml).getroot()
        for child in root_xml:
            if child.tag == 'controller':
                self._read_control_params(child)
            else:
                raise ValueError('Invalid tag in control config file: %s' % child.tag)

    def _read_control_params(self, controller_data: Et.Element):
        """
        Read the parameters of the control and store them in the config dict.

        Parameters
        ----------
        controller_data : Et.Element
            The controller data element from the config file.
        """
        controller_id = int(controller_data.attrib['id'])
        controller_params = {'id': controller_id, 'type': controller_data.attrib['type']}

        for child in controller_data:
            if child.tag == 'location':
                controller_params['location'] = [float(x) for x in child.text.split(',')]
            elif child.tag == 'nodes':
                controller_params['nodes'] = self._convert_string_to_list(child.text)
            else:
                raise ValueError('Invalid tag in control config file: %s' % child.tag)

        # Store the controller params
        self.config_dict.controller_params[controller_id] = controller_params

    def _read_simulation_params(self, simulation_data: Et.Element):
        """
        Read the parameters of the simulation and store them in the config dict.

        Parameters
        ----------
        simulation_data : Et.Element
            The simulation data element from the config file.
        """
        sim_params = {}
        for child in simulation_data:
            if child.tag == 'step':
                sim_params['step'] = int(child.text)
            elif child.tag == 'start':
                sim_params['start'] = float(child.text)
            elif child.tag == 'end':
                sim_params['end'] = float(child.text)
            elif child.tag == 'seed':
                sim_params['seed'] = int(child.text)
            elif child.tag == 'update_step':
                sim_params['update_step'] = int(child.text)
            elif child.tag == 'output_step':
                sim_params['output_step'] = int(child.text)
            elif child.tag == 'output':
                sim_params['output_dir'] = self._create_output_dir(child.text)
            else:
                raise ValueError('Invalid tag in simulation config file: %s' % child.tag)

        # Store the simulation params
        self.config_dict.simulation_params = sim_params

    def _create_output_dir(self, output_dir: str):
        """
        Create the output directory if it does not exist.

        Parameters
        ----------
        output_dir : str
            The relative path to the output directory.
        """
        output_dir = join(self.project_path, output_dir)
        if not exists(output_dir):
            makedirs(output_dir)
        return output_dir
