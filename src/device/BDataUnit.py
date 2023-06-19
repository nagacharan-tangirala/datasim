class DataUnitBase:
    def __init__(self, time_stamp: int, size_in_bits: int):
        """
        Initialize the data unit.
        """
        self.time_stamp: int = time_stamp
        self.size_in_bits: int = size_in_bits

    def get_size_in_bits(self) -> int:
        """
        Get the size in bits.

        Returns
        ----------
        int
            The size in bits.
        """
        return self.size_in_bits

    def get_time_stamp(self) -> int:
        """
        Get the time stamp.

        Returns
        ----------
        int
            The time stamp.
        """
        return self.time_stamp
