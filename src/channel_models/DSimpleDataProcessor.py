from random import shuffle

from src.channel_models.BDataProcessor import DataProcessorBase
from src.device.BUE import UEData


class SimpleDataReduction(DataProcessorBase):
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

        # Shuffle the ue data keys
        ue_shuffled_keys = list(ue_data.keys())
        shuffle(ue_shuffled_keys)

        for ue_id in ue_shuffled_keys:
            ue_data = ue_data[ue_id]
            simplified_ue_data[ue_id] = UEData(ue_data.ts, ue_data.data_size * self._compression_factor)

        return simplified_ue_data
