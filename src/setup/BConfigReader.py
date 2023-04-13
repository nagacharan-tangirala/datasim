import xml.etree.ElementTree as Et

from abc import ABCMeta, abstractmethod
from os import makedirs
from os.path import dirname, join, exists


class ConfigDict:
    def __init__(self):
        self.sensor_params = {}
        self.node_params = {}
        self.entity_params = {}
        self.controller_params = {}
        self.simulation_params = {}
        self.model_params = {}


class ConfigReader(metaclass=ABCMeta):
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.project_path = dirname(config_file)

        # Create the objects to read and store input params
        self.config_dict = ConfigDict()

    def read_config(self):
        """
        Read the config file.
        """
        config_root = Et.parse(self.config_file).getroot()
        for child in config_root:
            if child.tag == 'sensors':
                self._read_sensors(child.text)
            elif child.tag == 'nodes':
                self._read_nodes(child.text)
            elif child.tag == 'entities':
                self._read_entities(child.text)
            elif child.tag == 'control':
                self._read_control(child.text)
            elif child.tag == 'simulation':
                self._read_simulation_params(child)
            elif child.tag == 'model':
                self._read_model_params(child)
            else:
                raise ValueError('Invalid tag in config file: %s' % child.tag)

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
            elif child.tag == 'output':
                sim_params = self._parse_output_params(child, sim_params)
            else:
                raise ValueError('Invalid tag in simulation config file: %s' % child.tag)

        # Store the simulation params
        self.config_dict.simulation_params = sim_params

    @abstractmethod
    def _read_sensors(self, sensor_file):
        pass

    @abstractmethod
    def _read_nodes(self, node_file):
        pass

    @abstractmethod
    def _read_entities(self, entity_file):
        pass

    @abstractmethod
    def _read_control(self, control_file):
        pass

    def _read_model_params(self, model_data: Et.Element):
        """
        Read the parameters of the model and store them in the config dict.

        Parameters
        ----------
        model_data : Et.Element
            The model data element from the config file.
        """
        for child in model_data:
            model_name = child.tag
            model_params = {'type': child.attrib['type']}
            # Get the model parameters
            for param in child:
                model_params[param.attrib['name']] = param.attrib['value']

            # Store the model params
            self.config_dict.model_params[model_name] = model_params

    def _parse_output_params(self, child, sim_params):
        """
        Parse the output parameters from the config file.

        Parameters
        ----------
        child : Et.Element
            The output element from the config file.
        sim_params : Dict[str, Any]
            The simulation parameters parsed from the config file.

        Returns
        -------
        Dict[str, Any]
            The simulation output parameters with the output parameters added.
        """
        sim_params['output_dir'] = self._create_output_dir(child.attrib['path'])
        sim_params['output_step'] = int(child.attrib['step'])
        sim_params['output_level'] = child.attrib['level']
        sim_params['output_type'] = child.attrib['type']
        return sim_params

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

    def get_config_dict(self) -> ConfigDict:
        """
        Get the config dict.

        Returns
        -------
        ConfigDict
            The config dict.
        """
        return self.config_dict
