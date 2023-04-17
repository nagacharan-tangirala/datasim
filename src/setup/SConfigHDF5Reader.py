import h5py

from os.path import join

from src.setup.BConfigReader import ConfigReader


class ConfigHDF5Reader(ConfigReader):
    def __init__(self, config_file: str):
        """
        Initialize the HDF5 config reader.
        """
        super().__init__(config_file)

    def _read_sensors(self, sensor_file):
        """
        Read the sensor HDF5 file and parse the parameters of the sensors.
        In our case, the nodes are stored in entities file. So, we do nothing here.
        """
        pass

    def _read_nodes(self, node_file):
        """
        Read the node HDF5 file and parse the parameters of the nodes.
        In our case, the nodes are stored in entities file. So, we do nothing here.
        """
        pass

    def _read_entities(self, entity_file):
        """
        Read the entity HDF5 file and parse the parameters of the entities.
        """
        # Get the entities group
        self.h5_file = h5py.File(join(self.project_path, entity_file), 'r')

        # Get the entities group
        entities_group = self.h5_file['entities']

        # Read the entities
        for entity_id, entity in entities_group.items():
            # Create a dict to store the entity parameters
            entity_params = {'id': int(entity_id),
                             'type': entity.attrs['type'],
                             'start_time': int(entity.attrs['start_time']),
                             'end_time': int(entity.attrs['end_time']),
                             'sensors': entity.get('sensor_ids'),
                             'positions': entity.get('positions')}

            # Add the entity parameters to the config dict
            self.config_dict.device_params[int(entity_id)] = entity_params

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

    def _read_control(self, control_file):
        pass
