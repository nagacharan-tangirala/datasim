import pyarrow.parquet as pq

import xml.etree.ElementTree as Et

from os import makedirs
from os.path import dirname, join, exists


class ConfigDict:
    def __init__(self):
        self.sensor_params = {}
        self.node_params = {}
        self.agent_params = {}
        self.controller_params = {}
        self.simulation_params = {}


class ConfigReaderParquet:
    def __init__(self, config_file: str):
        """
        Initialize the HDF5 config reader.
        """
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
            if child.tag == 'input_files':
                self._read_input_files(child)
            elif child.tag == 'simulation':
                self._read_simulation_params(child)
            else:
                raise ValueError('Invalid tag in config file: %s' % child.tag)

    def _read_input_files(self, input_files):
        """
        Read the input files.
        """
        for child in input_files:
            if child.tag == 'agents':
                self._read_agents(child.text)
            elif child.tag == 'sensor':
                self._read_sensors(child.text)
            elif child.tag == 'node':
                self._read_nodes(child.text)
            elif child.tag == 'coverage':
                self._read_agents_coverage(child.text)
            else:
                raise ValueError('Invalid tag in config file: %s' % child.tag)

    def _read_agents(self, agent_file):
        """
        Read the agent HDF5 file and parse the parameters of the agents.
        """
        # Create the parquet file object.
        self.agent_file = pq.ParquetFile(join(self.project_path, agent_file))

        # Get the agents group
        agents_group = self.h5_file['agents']

        agent_count = 0
        # Read the agents
        for agent_id, agent in agents_group.items():
            # Create a dict to store the agent parameters
            agent_params = {'id': int(agent_id),
                            'type': agent.attrs['type'],
                            'start_time': int(agent.attrs['start_time']),
                            'end_time': int(agent.attrs['end_time']),
                            'sensors': agent.get('sensor_ids'),
                            'positions': agent.get('positions')}

            agent_count += 1
            # Add the agent parameters to the config dict
            self.config_dict.agent_params[int(agent_id)] = agent_params

        # Get the sensors group
        sensors_group = self.h5_file['sensors']

        # Read the sensors
        for sensor_id, sensor in sensors_group.items():
            # Create a dict to store the sensor parameters
            sensor_params = {'id': int(sensor_id),
                             'data_size': float(sensor.attrs['data_size']),
                             'type': sensor.attrs['type'],
                             'start_time': int(sensor.attrs['start_time']),
                             'end_time': int(sensor.attrs['end_time']),
                             'frequency': int(sensor.attrs['frequency']),
                             'mode': sensor.attrs['mode']}

            # Add the sensor parameters to the config dict
            self.config_dict.sensor_params[int(sensor_id)] = sensor_params

    def _read_agents_coverage(self, coverage_file: str):
        """
        Read the coverage HDF5 file and parse the parameters of the coverage.
        """
        # Get the coverage group
        self.h5_file = h5py.File(join(self.project_path, coverage_file), 'r')
        agents_group = self.h5_file['agents']

        # Read the coverage
        for agent_id, _ in agents_group.items():
            # Store the reference to the coverage data
            self.config_dict.agent_params[int(agent_id)]['coverage_file'] = join(self.project_path, coverage_file)

    def get_config_dict(self) -> ConfigDict:
        """
        Get the config dict.

        Returns
        -------
        ConfigDict
            The config dict.
        """
        return self.config_dict

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
