import xml.etree.ElementTree as Et
from os import makedirs
from os.path import dirname, exists, join

import pandas as pd
import pyarrow.parquet as pq


class SimulationSetup:
    def __init__(self, config_file: str):
        """
        Initialize the config reader.
        """
        self.config_file: str = config_file
        self.project_path: str = dirname(config_file)

        # Create the objects to read and store input data
        self.agent_data: pd.DataFrame = pd.DataFrame()
        self.coverage_data: pd.DataFrame = pd.DataFrame()
        self.node_data: pd.DataFrame = pd.DataFrame()
        self.controller_data: pd.DataFrame = pd.DataFrame()

        self.simulation_data: dict = {}

        self.node_link_data: pd.DataFrame = pd.DataFrame()
        self.agent_link_data: pd.DataFrame = pd.DataFrame()
        self.controller_link_data: pd.DataFrame = pd.DataFrame()

    def read_input_file(self):
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
            if child.tag == 'trace':
                self._read_trace(child.text)
            elif child.tag == 'coverage':
                self._read_agents_coverage(child.text)
            elif child.tag == 'nodes':
                self._read_nodes(child.text)
            elif child.tag == 'controllers':
                self._read_controllers(child.text)
            elif child.tag == 'controller_links':
                self._read_controller_links(child.text)
            else:
                raise ValueError('Invalid tag in config file: %s' % child.tag)

    def _read_trace(self, agent_file):
        """
        Read the agents trace data from the parquet file.
        """
        # Get the agents data as a pandas dataframe
        self.agent_data = pq.read_table(join(self.project_path, agent_file)).to_pandas()

        # Sort the agents data by agent id and time
        self.agent_data.sort_values(by=['vehicle_id', 'time'], inplace=True)

    def _read_agents_coverage(self, coverage_file: str):
        """
        Read the coverage data from the parquet file.
        """
        # Get the coverage data as a pandas dataframe
        self.coverage_data = pq.read_table(join(self.project_path, coverage_file)).to_pandas()

        # Sort the coverage data by agent id and time
        self.coverage_data.sort_values(by=['vehicle_id', 'time'], inplace=True)

    def _read_nodes(self, node_file: str):
        """
        Read the nodes data from the CSV file.
        """
        # Get the nodes data as a pandas dataframe
        self.node_data = pd.read_csv(join(self.project_path, node_file), dtype={'node_id': int, 'x': float, 'y': float, 'type': str}, usecols=['node_id', 'x', 'y', 'type'])

        # Set the node id as the index
        self.node_data.set_index('node_id', inplace=True)

        # Sort the nodes data by node id
        self.node_data.sort_index(inplace=True)

    def _read_controllers(self, controller_file: str):
        """
        Read the controllers data from the CSV file.
        """
        # Get the controllers data as a pandas dataframe
        self.controller_data = pd.read_csv(join(self.project_path, controller_file), dtype={'controller_id': int, 'x': float, 'y': float}, usecols=['controller_id', 'x', 'y'])

        # Set the node id as the index
        self.controller_data.set_index('controller_id', inplace=True)

        # Sort the controllers data by node id
        self.controller_data.sort_index(inplace=True)

    def _read_controller_links(self, link_file: str):
        """
        Read the links data from the links CSV file.
        """
        # Read the links csv file as a pandas dataframe
        self.controller_link_data = pd.read_csv(join(self.project_path, link_file),
                                                dtype={'link_id': int, 'node': int, 'controller': int, 'bandwidth_in': float, 'bandwidth_out': float},
                                                usecols=['link_id', 'node', 'controller', 'bandwidth_in', 'bandwidth_out'])

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
        self.simulation_data = sim_params

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
