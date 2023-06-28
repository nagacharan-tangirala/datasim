from src.device.BUE import UEData


class DataProcessorBase:
    def __init__(self):
        """
        Initialize the data reduction.
        """
        pass

    def simplify_ue_data(self, ue_data: dict[int, UEData]) -> dict[int, UEData]:
        """
        Simplify the ue data by applying data reduction methods. By default, no data reduction is applied.

        Parameters
        ----------
        ue_data : dict[int, UEData]
            The ue data to simplify.

        Returns
        -------
        dict[int, UEData]
            The simplified ue data.
        """
        return ue_data
