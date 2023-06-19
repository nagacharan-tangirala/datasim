from src.device.BDataUnit import DataUnitBase


class OnetoManyData(DataUnitBase):
    def __init__(self, origin_id: int, destination_ids: list[int], time_stamp: int, size_in_bits: int):
        """
        Initialize the uplink data unit.
        """
        super().__init__(time_stamp, size_in_bits)

        self.origin: int = origin_id
        self.destination: list[int] = destination_ids

    def get_origin(self) -> int:
        """
        Get the origin.

        Returns
        ----------
        int
            The origin.
        """
        return self.origin
