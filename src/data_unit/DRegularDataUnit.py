from src.data_unit.BDataUnit import DataUnitBase


class RegularDataUnit(DataUnitBase):
    def __init__(self, bytes_per_second: int, data_source: list[int] | None, data_target: list[int] | None):
        """
        Initialize the regular data unit.

        Parameters
        ----------
        bytes_per_second : int
            The size in bytes.
        """
        super().__init__(bytes_per_second, data_source, data_target)

    def step(self) -> None:
        """
        Step the data unit.
        """
        self._generate_data()
