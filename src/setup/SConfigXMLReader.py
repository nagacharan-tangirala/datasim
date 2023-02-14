from os.path import exists, dirname, join
import xml.etree.ElementTree as Et


class ConfigDict:
    def __init__(self):
        self.sensor_params = {}
        self.node_params = {}
        self.entity_params = {}


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
        """Read the config file."""
        for child in self.config_root:
            if child.tag == 'sensor_params':
                self._read_sensor_xml(child.text)
            elif child.tag == 'base_station':
                self._read_nodes_xml(child.text)
            elif child.tag == 'entity_params':
                self._read_entities_xml(child.text)
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
        """
        sensor_id = sensor_data.attrib['id']
        sensor_params = {'sensor_type': sensor_data.attrib['type'], 'sensor_mode': sensor_data.attrib['mode']}

        # Read the sensor parameters
        for child in sensor_data:
            if child.tag == 'data_size':
                sensor_params['data_size'] = child.text
            elif child.tag == 'start_time':
                sensor_params['start_time'] = child.text
            elif child.tag == 'end_time':
                sensor_params['end_time'] = child.text
            elif child.tag == 'collect_frequency':
                sensor_params['collect_frequency'] = child.text
            elif child.tag == 'transmit_frequency':
                sensor_params['transmit_frequency'] = child.text
            elif child.tag == ['custom_times'] and sensor_params['sensor_mode'] == 'custom':
                sensor_params['custom_times'] = child.text
            else:
                raise ValueError('Invalid tag in sensor config file: %s' % child.tag)

        # Store the sensor params
        self.config_dict.sensor_params[sensor_id] = sensor_params

    def _read_nodes_xml(self, nodes_xml: str):
        """
        Read the node_params xml file and parse the parameters of the nodes.

        Parameters
        ----------
        nodes_xml : str
            The relative path to the node_params config file.
        """
        nodes_xml = join(self.project_path, nodes_xml)
        if not exists(nodes_xml):
            raise FileNotFoundError('Base station config file not found: %s' % nodes_xml)
        root_xml = Et.parse(nodes_xml).getroot()
        for child in root_xml:
            if child.tag == 'base_station':
                self._read_node_params(child)
            else:
                raise ValueError('Invalid tag in base station config file: %s' % child.tag)

    def _read_node_params(self, node_data: Et.Element):
        """
        Read the parameters of a single node and store them in the config dict.

        Parameters
        ----------
        node_data : Et.Element
            The node data element from the config file.
        """
        node_id = node_data.attrib['id']
        node_params = {'node_type': node_data.attrib['type']}

        # Read the node parameters
        for child in node_data:
            if child.tag == 'location':
                node_params['location'] = child.text

        # Store the node params
        self.config_dict.node_params[node_id] = node_params

    def _read_entities_xml(self, entities_xml: str):
        """
        Read the entity_params xml file and parse the parameters of the entities.

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

