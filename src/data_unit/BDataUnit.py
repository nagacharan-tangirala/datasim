from abc import abstractmethod

from mesa import Agent


class DataUnitBase(Agent):
    def __init__(self, bytes_per_second: int, data_source: list[int] | int | None, data_target: list[int] | None):
        """
        Initialize the data unit.
        """
        super().__init__(0, None)

        self.time_stamp: int = 0
        self.previous_time_stamp: int = 0
        self.bytes_per_second: int = bytes_per_second

        self.data_to_send: int = 0
        self.data_source: list[int] | int = data_source if data_source is not None else []
        self.data_target: list[int] = data_target if data_target is not None else []

        self.data_cache: int = 0

    def get_bytes_per_second(self) -> int:
        """
        Get the bytes per second.

        Returns
        ----------
        int
            The bytes per second.
        """
        return self.bytes_per_second

    def get_time_stamp(self) -> int:
        """
        Get the time stamp.

        Returns
        ----------
        int
            The time stamp.
        """
        return self.time_stamp

    def get_data_source(self) -> list[int]:
        """
        Get the data source.

        Returns
        ----------
        list[int]
            The data source.
        """
        return self.data_source

    def get_data_target(self) -> list[int]:
        """
        Get the data targets.

        Returns
        ----------
        list[int]
            The data targets.
        """
        return self.data_target

    def set_data_source(self, data_source: list[int]) -> None:
        """
        Set the data source.

        Parameters
        ----------
        data_source : list[int]
            The data source.
        """
        self.data_source = data_source

    def set_data_target(self, data_target: list[int]) -> None:
        """
        Set the data_target.

        Parameters
        ----------
        data_target : list[int]
            The data_target.
        """
        self.data_target = data_target

    def set_current_time(self, current_time: int) -> None:
        """
        Set the current time.

        Parameters
        ----------
        current_time : int
            The current time.
        """
        self.previous_time_stamp = self.time_stamp
        self.time_stamp = current_time

    @abstractmethod
    def step(self) -> None:
        """
        Step the data unit.
        """
        pass

    def _generate_data(self) -> None:
        """
        Generate data.
        """
        # Move current data to cache
        self.data_cache = self.data_to_send

        # Calculate the time since the last step
        time_since_last_step = self.time_stamp - self.previous_time_stamp

        # Calculate the size in bytes
        self.data_to_send = (time_since_last_step / 1000) * self.bytes_per_second

    def get_generated_data(self) -> int:
        """
        Get the generated data.

        Returns
        ----------
        int
            The generated data.
        """
        return self.data_to_send

    def get_cached_data(self) -> int:
        """
        Get the cached data.

        Returns
        ----------
        int
            The cached data.
        """
        return self.data_cache
