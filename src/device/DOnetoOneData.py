from src.device.BDataUnit import DataUnitBase


class OnetoOneData(DataUnitBase):
    def __init__(self, time_stamp: int, size_in_bits: int, origin_id: int, destination_id: int):
        """
        Initialize the uplink data unit.
        """
        super().__init__(time_stamp, size_in_bits)

        self.origin: int = origin_id
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

    def get_destination(self) -> int:
        """
        Get the destination.

        Returns
        ----------
        int
            The destination.
        """
        return self.destination
