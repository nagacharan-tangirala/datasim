from src.device.BDataUnit import DataUnitBase


class ManytoOneData(DataUnitBase):
    def __init__(self, time_stamp: int, size_in_bits: int, origin_ids: list[int], destination_id: int):
        """
        Initialize the uplink data unit.
        """
        super().__init__(time_stamp, size_in_bits)

        self.origin: list[int] = origin_ids
        self.destination: int = destination_id

    def get_origin(self) -> int:
        """
        Get the origin.

        Returns
        ----------
        int
            The origin.
        """
        return self.origin
