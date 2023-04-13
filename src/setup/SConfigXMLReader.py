from os.path import exists, join
import xml.etree.ElementTree as Et

from src.setup.BConfigReader import ConfigReader

from typing import List, Dict


class ConfigXMLReader(ConfigReader):
    def __init__(self, config_file: str):
        super().__init__(config_file)
        self.config_root = Et.parse(config_file).getroot()

    def _read_sensors(self, sensors_file: str):
        """
        Read the sensor xml file and parse the parameters of the sensors.

        Parameters
        ----------
        sensors_file : str
            The relative path to the sensor config file.
        """
        # Check if the file exists
        sensors_file = join(self.project_path, sensors_file)
        if not exists(sensors_file):
            raise FileNotFoundError('Sensor config file not found: %s' % sensors_file)

        # Read the file
        sensor_root = Et.parse(sensors_file).getroot()
        for child in sensor_root:
            if child.tag == 'sensor':
                self._read_sensor_params_xml(child)
            else:
                raise ValueError('Invalid tag in sensor config file: %s' % child.tag)

    def _read_sensor_params_xml(self, sensor_data: Et.Element):
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

    def _read_nodes(self, nodes_xml: str):
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

    def _read_entities(self, entities_file: str):
        """
        Read the entities xml file and parse the parameters of the entities.

        Parameters
        ----------
        entities_file : str
            The relative path to the entity_params config file.
        """
        entities_file = join(self.project_path, entities_file)

        if not exists(entities_file):
            raise FileNotFoundError('Entities config file not found: %s' % entities_file)
        root_xml = Et.parse(entities_file).getroot()
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
        entity_params = {'type': entity_data.attrib['type'], 'start_time': entity_data.attrib['start_time'], 'end_time': entity_data.attrib['end_time']}

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

    def _read_control(self, control_xml: str):
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
