from collections import namedtuple

from mesa import Agent


class UEDataHandler(Agent):
    def __init__(self, source_ue: int, model_data: dict):
        """
        Initialize the data unit.
        """
        super().__init__(0, None)

        self._source_ue: int = source_ue
        self._bytes_per_second: int = model_data['bytes_per_second']

        self._time_stamp: int = -1
        self._previous_time_stamp: int = -1

        self._data_to_send: namedtuple = namedtuple('ue_data', ['ts', 'data_size'])
        self._data_cache: namedtuple = namedtuple('ue_data', ['ts', 'data_size'])
        self._data_received: namedtuple = namedtuple('ue_data', ['ts', 'data_size'])

    @property
    def time_stamp(self) -> int:
        """Get the time stamp."""
        return self._time_stamp

    @property
    def source_ue(self) -> int:
        """Get the data source."""
        return self._source_ue

    @property
    def data_to_send(self) -> namedtuple:
        """ Get the data to send. """
        return self._data_to_send

    @property
    def data_cache(self) -> namedtuple:
        """ Get the data cache. """
        return self._data_cache

    @time_stamp.setter
    def time_stamp(self, current_time: int) -> None:
        """Set the current time."""
        self._previous_time_stamp = self._time_stamp
        self._time_stamp = current_time

    def step(self) -> None:
        """
        Step the data unit.
        """
        self._generate_data()

    def _generate_data(self) -> None:
        """
        Generate data.
        """
        # Move current data to cache
        self._data_cache = self._data_to_send

        # Calculate the time since the last step
        time_since_last_step = self._time_stamp - self._previous_time_stamp

        # Calculate the size in bytes
        data_to_send = (time_since_last_step / 1000) * self._bytes_per_second

        self._data_to_send.ts = self._time_stamp
        self._data_to_send.data_size = data_to_send
