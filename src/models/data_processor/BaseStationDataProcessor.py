from src.application.Payload import BaseStationPayload
from src.core.Constants import C_REDUCTION_FACTOR


class BaseStationDataProcessor:
    def __init__(self, model_data: dict):
        """
        Initialize the base station data reduction.
        """
        self._compression_factor: float = float(model_data[C_REDUCTION_FACTOR])

    def simplify_base_station_data(self, base_station_payload: BaseStationPayload) -> BaseStationPayload:
        """
        Simplify the base station data by applying the data processing techniques.

        Parameters
        ----------
        base_station_payload : BaseStationPayload
            The vehicle data to simplify.

        Returns
        -------
        BaseStationPayload
            The simplified base station data.
        """
        base_station_payload.uplink_data = [x * self._compression_factor for x in base_station_payload.uplink_data]
        # TODO: Add more data processing techniques here.

        return base_station_payload
