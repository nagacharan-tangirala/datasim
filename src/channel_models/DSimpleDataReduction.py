from src.channel_models.BDataReduction import DataReductionBase
from src.device.BUE import UEData


class SimpleDataReduction(DataReductionBase):
    def __init__(self, model_data: dict):
        """
        Initialize the simple data reduction.
        """
        super().__init__()
        self._compression_factor: float = float(model_data['compression'])

    def simplify_ue_data(self, ue_data: dict[int, UEData]) -> dict[int, UEData]:
        """
        Overriding the base method. Simplify the ue data by applying compression.

        Parameters
        ----------
        ue_data : dict[int, UEData]
            The ue data to simplify.

        Returns
        -------
        dict[int, UEData]
            The simplified ue data.
        """
        simplified_ue_data: dict[int, UEData] = {}
        for ue_id, ue_data in ue_data.items():
            simplified_ue_data[ue_id] = UEData(ue_data.ts, ue_data.data_size * self._compression_factor)

        return simplified_ue_data
