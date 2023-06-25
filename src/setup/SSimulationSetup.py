import xml.etree.ElementTree as Et
from os import makedirs
from os.path import dirname, exists, join
from typing import Any, Dict

from src.core.CustomExceptions import *
from src.setup.SCSVDataReader import CSVDataReader
from src.setup.SInputDataReader import InputDataReader
from src.setup.SParquetDataReader import ParquetDataReader


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

        self.file_readers: dict[str, InputDataReader] = {}

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
                self._read_input_files(child, child.attrib['read_chunks'].lower())
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

    def _read_input_files(self, input_files: Et.Element, read_in_chunks: str) -> None:
        """
        Read the input files.

        Parameters
        ----------
        input_files : Element
            The input files element.
        """
        self.read_in_chunks: bool = True if read_in_chunks == 'true' else False
        for child in input_files:
            if child.tag == 'ue_trace':
                self._read_ue_trace(child)
            elif child.tag == 'ue_links':
                self._read_ue_links(child)
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
        ue_trace_file = join(self.project_path, ue_trace_element.text)
        column_names = ['vehicle_id', 'time', 'x', 'y']
        column_dtypes = {'vehicle_id': int, 'time': int, 'x': float, 'y': float}

        # Get the file type
        file_type = ue_trace_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers['ue_trace'] = ParquetDataReader(ue_trace_file, column_names, column_dtypes)
            case 'csv':
                self.file_readers['ue_trace'] = CSVDataReader(ue_trace_file, column_names, column_dtypes)
            case _:
                raise UnsupportedInputFormatError(file_type)

    def _read_ue_links(self, ue_links_element: Et.Element) -> None:
        """
        Read the coverage data from the parquet file.

        Parameters
        ----------
        ue_links_element : Et.Element
            The ue links element.
        """
        # Get the path to the coverage file
        ue_links_file = join(self.project_path, ue_links_element.text)
        column_names = ['vehicle_id', 'time', 'neighbours', 'neighbour_distances']
        column_dtypes = {'vehicle_id': int, 'time': int, 'neighbours': str, 'neighbour_distances': str}

        # Get the file type
        file_type = ue_links_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers['ue_links'] = ParquetDataReader(ue_links_file, column_names, column_dtypes)
            case 'csv':
                self.file_readers['ue_links'] = CSVDataReader(ue_links_file, column_names, column_dtypes)
            case _:
                raise UnsupportedInputFormatError(file_type)

    def _read_cell_towers(self, cell_towers_element: Et.Element) -> None:
        """
        Read the cell towers data from the CSV file.

        Parameters
        ----------
        cell_towers_element : Et.Element
            The cell towers element.
        """
        cell_towers_file = join(self.project_path, cell_towers_element.text)
        column_names = ['cell_tower_id', 'x', 'y', 'type']
        column_dtypes = {'cell_tower_id': int, 'x': float, 'y': float, 'type': str}

        # Get the file type
        file_type = cell_towers_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers['cell_towers'] = ParquetDataReader(cell_towers_file, column_names, column_dtypes)
            case 'csv':
                self.file_readers['cell_towers'] = CSVDataReader(cell_towers_file, column_names, column_dtypes)
            case _:
                raise UnsupportedInputFormatError(file_type)

    def _read_controllers(self, controller_element: Et.Element) -> None:
        """
        Read the controllers data from the CSV file.

        Parameters
        ----------
        controller_element : Et.Element
            The controllers element.
        """
        controller_file = join(self.project_path, controller_element.text)
        column_names = ['controller_id', 'x', 'y']
        column_dtypes = {'controller_id': int, 'x': float, 'y': float}

        # Get the file type
        file_type = controller_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers['controllers'] = ParquetDataReader(controller_file, column_names, column_dtypes)
            case 'csv':
                self.file_readers['controllers'] = CSVDataReader(controller_file, column_names, column_dtypes)
            case _:
                raise UnsupportedInputFormatError(file_type)

    def _read_controller_links(self, controller_links_element: Et.Element) -> None:
        """
        Read the links data from the links CSV file.

        Parameters
        ----------
        controller_links_element : Et.Element
            The links element.
        """
        controller_links_file = join(self.project_path, controller_links_element.text)
        column_names = ['link_id', 'source_type', 'source_id', 'target_type', 'target_id']
        column_dtypes = {'link_id': int, 'source_type': str, 'source_id': int, 'target_type': str, 'target_id': int}

        # Get the file type
        file_type = controller_links_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers['controller_links'] = ParquetDataReader(controller_links_file, column_names, column_dtypes)
            case 'csv':
                self.file_readers['controller_links'] = CSVDataReader(controller_links_file, column_names, column_dtypes)
            case _:
                raise UnsupportedInputFormatError(file_type)

    def _read_tower_links(self, tower_links_element: Et.Element) -> None:
        """
        Read the tower links data from the CSV file.

        Parameters
        ----------
        tower_links_element : Et.Element
            The tower links element.
        """
        tower_links_file = join(self.project_path, tower_links_element.text)
        column_names = ['link_id', 'source_type', 'source_id', 'target_type', 'target_id']
        column_dtypes = {'link_id': int, 'source_type': str, 'source_id': int, 'target_type': str, 'target_id': int}

        # Get the file type
        file_type = tower_links_file.split('.')[-1]

        match file_type:
            case 'parquet':
                self.file_readers['tower_links'] = ParquetDataReader(tower_links_file, column_names, column_dtypes)
            case 'csv':
                self.file_readers['tower_links'] = CSVDataReader(tower_links_file, column_names, column_dtypes)
            case _:
                raise UnsupportedInputFormatError(file_type)

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
            elif child.tag == 'chunk_ts':
                simulation_settings['chunk_ts'] = int(child.text)
            elif child.tag == 'output':
                simulation_settings.update(self._read_output_settings(child))
            else:
                raise InvalidXMLTagError(child.tag)

        # Store the simulation settings
        self.simulation_data = simulation_settings

    def _read_all_channel_models(self, channels_element: Et.Element) -> None:
        """
        Read the model data from the config file.

        Parameters
        ----------
        channels_element : Et.Element
            The channel data element from the config file.
        """
        allowed_device_types = ['ue', 'cell_tower', 'controller']
        for channel in channels_element:
            if channel.tag != 'channel':
                raise InvalidXMLTagError(channel.tag)

            device_type = channel.attrib['device']
            parsed_model_data = self._read_all_models(channel)

            if device_type not in allowed_device_types:
                raise InvalidXMLAttributeError('device', device_type, allowed_device_types)
            self.channel_model_data[device_type] = parsed_model_data

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

    def _read_all_models(self, all_models_element: Et.Element) -> Dict[str, Dict[str, Any]]:
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
