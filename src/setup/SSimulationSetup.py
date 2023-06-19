import xml.etree.ElementTree as Et
from os import makedirs
from os.path import dirname, exists, join

import pyarrow.parquet as pq
from pandas import DataFrame, read_csv


class SimulationSetup:
    def __init__(self, config_file: str):
        """
        Initialize the config reader.
        """
        self.config_file: str = config_file
        self.project_path: str = dirname(config_file)

        # Create the objects to read and store input data
        self.ue_data: DataFrame = DataFrame()
        self.coverage_data: DataFrame = DataFrame()
        self.cell_tower_data: DataFrame = DataFrame()
        self.controller_data: DataFrame = DataFrame()

        self.simulation_data: dict = {}
        self.ue_type_data: list[dict] = []

        self.cell_tower_link_data: DataFrame = DataFrame()
        self.ue_link_data: DataFrame = DataFrame()
        self.controller_link_data: DataFrame = DataFrame()

        self.model_data: dict = {}

    def read_input_file(self):
        """
        Read the config file.
        """
        config_root = Et.parse(self.config_file).getroot()
        for child in config_root:
            if child.tag == 'input_files':
                self._read_input_files(child)
            elif child.tag == 'simulation':
                self._read_simulation_settings(child)
            elif child.tag == 'models':
                self._read_model_data(child)
            elif child.tag == 'ues':
                self._read_ue_data(child)
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
                self._read_ues_coverage(child.text)
            elif child.tag == 'cell_towers':
                self._read_cell_towers(child.text)
            elif child.tag == 'controllers':
                self._read_controllers(child.text)
            elif child.tag == 'controller_links':
                self._read_controller_links(child.text)
            else:
                raise ValueError('Invalid tag in config file: %s' % child.tag)

    def _read_trace(self, ue_file):
        """
        Read the ues trace data from the parquet file.
        """
        # Get the ues data as a pandas dataframe
        self.ue_data = pq.read_table(join(self.project_path, ue_file)).to_pandas()

        # Sort the ues data by ue id and time
        self.ue_data.sort_values(by=['ue_id', 'time'], inplace=True)

    def _read_ues_coverage(self, coverage_file: str):
        """
        Read the coverage data from the parquet file.
        """
        # Get the coverage data as a pandas dataframe
        self.coverage_data = pq.read_table(join(self.project_path, coverage_file)).to_pandas()

        # Sort the coverage data by ue id and time
        self.coverage_data.sort_values(by=['vehicle_id', 'time'], inplace=True)

    def _read_cell_towers(self, cell_tower_file: str):
        """
        Read the cell towers data from the CSV file.
        """
        # Get the cell towers data as a pandas dataframe
        self.cell_tower_data = read_csv(join(self.project_path, cell_tower_file), dtype={'cell_tower_id': int, 'x': float, 'y': float, 'type': str}, usecols=['cell_tower_id', 'x', 'y', 'type'])

    def _read_controllers(self, controller_file: str):
        """
        Read the controllers data from the CSV file.
        """
        # Get the controllers data as a pandas dataframe
        self.controller_data = read_csv(join(self.project_path, controller_file), dtype={'controller_id': int, 'x': float, 'y': float}, usecols=['controller_id', 'x', 'y'])

    def _read_controller_links(self, link_file: str):
        """
        Read the links data from the links CSV file.
        """
        # Read the links csv file as a pandas dataframe
        self.controller_link_data = read_csv(join(self.project_path, link_file),
                                             dtype={'link_id': int, 'cell_tower': int, 'controller': int, 'bandwidth_in': float, 'bandwidth_out': float},
                                             usecols=['link_id', 'cell_tower', 'controller', 'bandwidth_in', 'bandwidth_out'])

    def _read_output_settings(self, child):
        """
        Parse the output settings from the config file.

        Parameters
        ----------
        child : Et.Element
            The output element from the config file.

        Returns
        -------
        Dict[str, Any]
            The output settings.
        """
        output_settings = {}

        output_settings['output_dir'] = self._create_output_dir(child.attrib['path'])
        output_settings['output_step'] = int(child.attrib['step'])
        output_settings['output_type'] = child.attrib['type']
        return output_settings

    def _read_simulation_settings(self, simulation_data: Et.Element):
        """
        Read the parameters of the simulation and store them in the config dict.

        Parameters
        ----------
        simulation_data : Et.Element
            The simulation data element from the config file.
        """
        simulation_settings = {}
        for child in simulation_data:
            if child.tag == 'step':
                simulation_settings['step'] = int(child.text)
            elif child.tag == 'start':
                simulation_settings['start'] = float(child.text)
            elif child.tag == 'end':
                simulation_settings['end'] = float(child.text)
            elif child.tag == 'seed':
                simulation_settings['seed'] = int(child.text)
            elif child.tag == 'update_step':
                simulation_settings['update_step'] = int(child.text)
            elif child.tag == 'output':
                simulation_settings.update(self._read_output_settings(child))
            else:
                raise ValueError('Invalid tag in simulation config file: %s' % child.tag)

        # Store the simulation settings
        self.simulation_data = simulation_settings

    def _read_model_data(self, model_element: Et.Element):
        """
        Read the model data from the config file.

        Parameters
        ----------
        model_element : Et.Element
            The model data element from the config file.
        """
        self.model_data = {'ue': {}, 'cell_tower': {}, 'controller': {}}
        for child in model_element:
            if child.tag == 'model':
                parsed_model_data, device_type = self._read_model(child)
                if device_type not in self.model_data:
                    raise ValueError('Invalid device type in model config file: %s' % device_type)
                if parsed_model_data['id'] in self.model_data[device_type]:
                    raise ValueError('Duplicate model id: %s' % parsed_model_data['id'])
                self.model_data[device_type][parsed_model_data['id']] = parsed_model_data
            else:
                raise ValueError('Invalid tag in model config file: %s' % child.tag)

    @staticmethod
    def _read_model(model_element: Et.Element):
        """
        Read the model data from the config file.

        Parameters
        ----------
        model_element Et.Element
            The model data element from the config file.

        Returns
        -------
        Dict[str, Any]
            The model data.
        """
        model_data = {}

        # Read attributes
        model_data['id'] = model_element.attrib['id']
        model_data['type'] = model_element.attrib['type']
        model_data['name'] = model_element.attrib['name']
        device_type = model_element.attrib['device']

        # Read model parameters
        for child in model_element:
            if child.tag == 'parameter':
                model_data[child.attrib['name']] = child.attrib['value']
            else:
                raise ValueError('Invalid tag in model config file: %s' % child.tag)

        return model_data, device_type

    def _read_ue_data(self, ues_element: Et.Element):
        """
        Read the types of UEs from the config file.
        """
        self.ue_type_data = []
        for child in ues_element:
            ue_type_info = {}
            if child.tag == 'ue':
                ue_type_info['id'] = child.attrib['id']
                ue_type_info['type'] = child.attrib['type']

                if ue_type_info['type'] not in ['vehicle']:
                    raise ValueError('Invalid type parameter in ue config file: %s' % ue_type_info['type'])

                for param_child in child:
                    if param_child.tag == 'parameter':
                        ue_type_info[param_child.attrib['name']] = param_child.attrib['value']
                    else:
                        raise ValueError('Invalid tag in ue config file: %s' % param_child.tag)
                self.ue_type_data.append(ue_type_info)

        # Validate the UE types
        for ue_type in self.ue_type_data:
            if 'id' not in ue_type:
                raise ValueError('Missing id parameter in ue config file')

        ue_weights = [float(ue_type['weight']) for ue_type in self.ue_type_data]
        if sum(ue_weights) < 1.0:
            raise ValueError("The sum of the weights of the ue types must be 1.")

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
