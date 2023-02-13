from abc import ABCMeta, abstractmethod
from os.path import exists
from xml.etree.ElementTree import ElementTree as et


class ConfigReader(metaclass=ABCMeta):
    def __init__(self, input_params: dict):
        """Initialize the config reader."""
        self.config_xml = input_params.get('config_xml', None)
        self._read_config()

    def _read_config(self):
        """Read the config file."""
        root_xml = et.getroot(self.config_xml)
        for child in root_xml:
            if child.tag == 'sensors':
                self._read_sensor_config(child.text)
            elif child.tag == 'base_station':
                self._read_base_stations(child.text)
            elif child.tag == 'entities':
                self._read_sensor(child.text)
            else:
                raise ValueError('Invalid tag in config file: %s' % child.tag)

    def _read_sensor_config(self, sensor_xml: str):
        """Read the sensor config."""
        if not exists(sensor_xml):
            raise FileNotFoundError('Sensor config file not found: %s' % sensor_xml)
        root_xml = et.getroot(sensor_xml)
        for child in root_xml:
            if child.tag == 'sensor':
                self._read_sensor(child)
            else:
                raise ValueError('Invalid tag in sensor config file: %s' % child.tag)

    def _read_base_stations(self, base_station_xml: str):
        """Read the base stations."""
        if not exists(base_station_xml):
            raise FileNotFoundError('Base station config file not found: %s' % base_station_xml)
        root_xml = et.getroot(base_station_xml)
        for child in root_xml:
            if child.tag == 'base_station':
                self._read_base_station(child)
            else:
                raise ValueError('Invalid tag in base station config file: %s' % child.tag)
            
    def _read_sensor(self, sensor_xml: str):
        """Read the sensor."""
