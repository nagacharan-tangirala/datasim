from src.data_unit.BDataUnit import DataUnitBase


class DynamicDataUnit(DataUnitBase):
    def __init__(self, bytes_per_second: int, data_source: list[int] | None, data_target: list[int] | None):
        """
        Initialize the dynamic data unit.
        """
        super().__init__(bytes_per_second, data_source, data_target)

    def add_origin(self, origin: int) -> None:
        """
        Add an origin.

        Parameters
        ----------
        origin : int
            The origin.
        """
        self.data_source.append(origin)

    def add_destination(self, destination: int) -> None:
        """
        Add a destination.

        Parameters
        ----------
        destination : int
            The destination.
        """
        self.data_target.append(destination)

    def step(self) -> None:
        """
        Step the data unit.
        """
        # Clear the origins and destinations
        self.data_source.clear()
        self.data_target.clear()

        self._generate_data()
