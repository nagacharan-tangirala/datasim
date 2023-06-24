import xml.etree.ElementTree as Et
from os import makedirs
from os.path import dirname, exists, join
from typing import Any, Dict, Tuple

import pyarrow.parquet as pq
from pandas import DataFrame, read_csv

from src.core.CustomExceptions import *


class SimulationSetup:
    def __init__(self, config_file: str):
        """
        Initialize the config reader.

        Parameters
        ----------
        config_file : str
            The path to the configuration file.
        """
        self.config_file: str = config_file
        self.project_path: str = dirname(config_file)

        self.ue_trace_data: DataFrame = DataFrame()
        self.cell_tower_data: DataFrame = DataFrame()
        self.controller_data: DataFrame = DataFrame()

        self.ue_trace_file: str = ''
        self.ue_links_file: str = ''
        self.cell_tower_file: str = ''
        self.tower_links_file: str = ''
        self.controller_file: str = ''
        self.controller_links_file: str = ''

        self.ue_links_data: DataFrame = DataFrame()
        self.cell_tower_links_data: DataFrame = DataFrame()
        self.controller_links_data: DataFrame = DataFrame()

        self.ue_models_data: dict = {}
        self.cell_tower_models_data: dict = {}
        self.controller_models_data: dict = {}

        self.channel_model_data: dict = {}
        self.simulation_data: dict = {}

    def read_input_file(self) -> None:
        """
        Read the config file.
        """
        config_root = Et.parse(self.config_file).getroot()
        for child in config_root:
            if child.tag == 'input_files':
                self._read_input_files(child)
            elif child.tag == 'simulation':
                self._read_simulation_settings(child)
            elif child.tag == 'channels':
                self._read_all_channel_models(child)
            elif child.tag == 'ues':
                self._read_ue_models(child)
            elif child.tag == 'cell_towers':
                self._read_cell_tower_models(child)
            elif child.tag == 'controllers':
                self._read_controller_models(child)
            else:
                raise InvalidXMLTagError(child.tag)

    def _read_input_files(self, input_files) -> None:
        """
        Read the input files.

        Parameters
        ----------
        input_files : Element
            The input files element.
        """
        for child in input_files:
            if child.tag == 'ue_trace':
                self._read_ue_trace(child)
            elif child.tag == 'ue_links':
                self.read_ue_links(child)
            elif child.tag == 'cell_towers':
                self._read_cell_towers(child)
            elif child.tag == 'tower_links':
                self._read_tower_links(child)
            elif child.tag == 'controllers':
                self._read_controllers(child)
            elif child.tag == 'controller_links':
                self._read_controller_links(child)
            else:
                raise InvalidXMLTagError(child.tag)

    def _read_ue_trace(self, ue_trace_element: Et.Element) -> None:
        """
        Read the ues trace data from the parquet file.

        Parameters
        ----------
        ue_trace_element : Et.Element
            The ue trace element.
        """
        # Get the path to the ue trace file
        self.ue_trace_file = join(self.project_path, ue_trace_element.text)

        # Check if this has to be streamed
        if ue_trace_element.attrib['stream'].lower() != 'true':
            # Read and sort the data.
            self.ue_trace_data = pq.read_table(self.ue_trace_file).to_pandas()
            self.ue_trace_data.sort_values(by=['vehicle_id', 'time'], inplace=True)

    def read_ue_links(self, ue_links_element: Et.Element) -> None:
        """
        Read the coverage data from the parquet file.

        Parameters
        ----------
        ue_links_element : Et.Element
            The ue links element.
        """
        # Get the path to the coverage file
        self.ue_links_file = join(self.project_path, ue_links_element.text)

        if ue_links_element.attrib['stream'].lower() != 'true':
            # Read and sort the data.
            self.ue_links_data = pq.read_table(self.ue_links_file).to_pandas()
            self.ue_links_data.sort_values(by=['vehicle_id', 'time'], inplace=True)

    def _read_cell_towers(self, cell_tower_file: Et.Element) -> None:
        """
        Read the cell towers data from the CSV file.

        Parameters
        ----------
        cell_tower_file : Et.Element
            The cell towers element.
        """
        # Get the path to the cell towers file
        self.cell_tower_file = join(self.project_path, cell_tower_file.text)

        if cell_tower_file.attrib['stream'].lower() != 'true':
            # Get the cell towers data as a pandas dataframe
            self.cell_tower_data = read_csv(self.cell_tower_file, dtype={'cell_tower_id': int, 'x': float, 'y': float, 'type': str}, usecols=['cell_tower_id', 'x', 'y', 'type'])

    def _read_controllers(self, controller_file: Et.Element) -> None:
        """
        Read the controllers data from the CSV file.

        Parameters
        ----------
        controller_file : Et.Element
            The controllers element.
        """
        # Get the path to the controllers file
        self.controller_file = join(self.project_path, controller_file.text)

        if controller_file.attrib['stream'].lower() != 'true':
            # Get the controllers data as a pandas dataframe
            self.controller_data = read_csv(self.controller_file, dtype={'controller_id': int, 'x': float, 'y': float}, usecols=['controller_id', 'x', 'y'])

    def _read_controller_links(self, link_file: Et.Element) -> None:
        """
        Read the links data from the links CSV file.

        Parameters
        ----------
        link_file : Et.Element
            The links element.
        """
        # Get the path to the links file
        self.controller_links_file = join(self.project_path, link_file.text)

        if link_file.attrib['stream'].lower() != 'true':
            # Get the links data as a pandas dataframe
            self.controller_links_data = read_csv(self.controller_links_file,
                                                  dtype={'link_id': int, 'cell_tower': int, 'controller': int, 'bandwidth_in': float, 'bandwidth_out': float},
                                                  usecols=['link_id', 'cell_tower', 'controller', 'bandwidth_in', 'bandwidth_out'])

    def _read_tower_links(self, tower_links_file: Et.Element) -> None:
        """
        Read the tower links data from the CSV file.

        Parameters
        ----------
        tower_links_file : Et.Element
            The tower links element.
        """
        # Get the path to the tower links file
        self.tower_links_file = join(self.project_path, tower_links_file.text)

        if tower_links_file.attrib['stream'].lower() != 'true':
            # Get the tower links data as a pandas dataframe
            self.tower_links_data = pq.read_table(self.tower_links_file).to_pandas()

            # Sort the tower links data by vehicle id and time
            self.tower_links_data.sort_values(by=['agent_id', 'time'], inplace=True)

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

        output_settings['output_dir'] = self._create_output_dir(child.attrib['location'])
        output_settings['output_step'] = int(child.attrib['step'])
        output_settings['output_type'] = child.attrib['type']
        return output_settings

    def _read_simulation_settings(self, simulation_data: Et.Element) -> None:
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
                raise InvalidXMLTagError(child.tag)

        # Store the simulation settings
        self.simulation_data = simulation_settings

    def _read_all_channel_models(self, model_element: Et.Element) -> None:
        """
        Read the model data from the config file.

        Parameters
        ----------
        model_element : Et.Element
            The channel data element from the config file.
        """
        allowed_device_types = ['ue', 'cell_tower', 'controller']
        for child in model_element:
            if child.tag != 'channel':
                raise InvalidXMLTagError(child.tag)

            parsed_model_data, device_type = self._read_channel_model(child)

            if device_type not in allowed_device_types:
                raise InvalidXMLAttributeError('device', device_type, allowed_device_types)
            self.channel_model_data[device_type] = parsed_model_data

    @staticmethod
    def _read_channel_model(channel_element: Et.Element) -> Tuple[Dict[str, Any], str]:
        """
        Read the channel model data from the config file.

        Parameters
        ----------
        model_element Et.Element
            The channel model data element from the config file.

        Returns
        -------
        Dict[str, Any]
            The model data.
        """
        channel_data = {}

        # Read attributes
        channel_data['name'] = channel_element.attrib['name']
        device_type = channel_element.attrib['device']

        # Read model parameters
        for child in channel_element:
            if child.tag != 'parameter':
                raise InvalidXMLTagError(child.tag)
            channel_data[child.attrib['name']] = child.attrib['value']

        return channel_data, device_type

    def _read_ue_models(self, ues_element: Et.Element) -> None:
        """
        Read the types of UEs from the config file.
        """
        for child in ues_element:
            ue_info = {}
            if child.tag != 'ue':
                raise InvalidXMLTagError(child.tag)

            ue_info['id'] = int(child.attrib['id'])
            ue_info['type'] = child.attrib['type']
            ue_info['weight'] = child.attrib['weight']

            if ue_info['type'] not in ['vehicle']:
                raise InvalidXMLAttributeError('type', ue_info['type'], ['vehicle'])

            ue_info['models'] = self._read_all_models(child)

            self.ue_models_data[ue_info['id']] = ue_info

    def _read_cell_tower_models(self, cell_towers_element: Et.Element) -> None:
        """
        Read the types of cell towers from the config file.

        Parameters
        ----------
        cell_towers_element : Et.Element
            The element with all the cell tower data from the config file.
        """
        for child in cell_towers_element:
            cell_tower_info = {}
            if child.tag != 'cell_tower':
                raise InvalidXMLTagError(child.tag)

            cell_tower_info['id'] = int(child.attrib['id'])
            cell_tower_info['type'] = child.attrib['type']
            cell_tower_info['weight'] = child.attrib['weight']

            if cell_tower_info['type'] not in ['basic']:
                raise InvalidXMLAttributeError('type', cell_tower_info['type'], ['basic'])

            cell_tower_info['models'] = self._read_all_models(child)

            self.cell_tower_models_data[cell_tower_info['id']] = cell_tower_info

    def _read_controller_models(self, controllers_element: Et.Element) -> None:
        """
        Read the types of controllers from the config file.

        Parameters
        ----------
        controllers_element : Et.Element
            The element with all the controller data from the config file.
        """
        for child in controllers_element:
            controller_info = {}
            if child.tag != 'controller':
                raise InvalidXMLTagError(child.tag)

            controller_info['id'] = int(child.attrib['id'])
            controller_info['type'] = child.attrib['type']
            controller_info['weight'] = child.attrib['weight']

            if controller_info['type'] not in ['central']:
                raise InvalidXMLAttributeError('type', controller_info['type'], ['central'])

            controller_info['models'] = self._read_all_models(child)

            self.controller_models_data[controller_info['id']] = controller_info

    def _read_all_models(self, all_models_element: Et.Element) -> Dict[int, Dict[str, Any]]:
        """
        Read the types of models from the config file.

        Parameters
        ----------
        all_models_element : Et.Element
            The element with all the model data from the config file.
        """
        all_models_data = {}
        for model_child in all_models_element:
            if model_child.tag != 'model':
                raise InvalidXMLTagError(model_child.tag)

            model_data = self._read_model_data(model_child)
            if model_data['type'] in all_models_data:
                raise DuplicateDeviceModelError(model_data['type'])

            all_models_data[model_data['type']] = model_data

        return all_models_data

    @staticmethod
    def _read_model_data(model_element: Et.Element) -> Dict[str, Any]:
        """
        Read the model data from the config file.

        Parameters
        ----------
        model_element : Et.Element
            The model data element from the config file.
        """
        model_data = {}
        model_data['type'] = model_element.attrib['type']
        model_data['name'] = model_element.attrib['name']

        for child in model_element:
            if child.tag != 'parameter':
                raise InvalidXMLTagError(child.tag)

            model_data[child.attrib['name']] = child.attrib['value']

        return model_data

    def _create_output_dir(self, output_dir: str) -> str:
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
