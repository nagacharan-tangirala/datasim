from src.application.payload import BaseStationPayload
from src.core.constants import C_REDUCTION_FACTOR


class ControllerDataProcessor:
    def __init__(self, model_data: dict):
        """
        Initialize the controller data reduction.
        """
        self._compression_factor: float = float(model_data[C_REDUCTION_FACTOR])

    def simplify_controller_data(
        self, base_station_data: dict[int, BaseStationPayload]
    ) -> dict[int, BaseStationPayload]:
        """
        Simplify the controller data by applying the data processing techniques.

        Parameters
        ----------
        base_station_data : dict[int, BaseStationPayload]
            The base station data to simplify.

        Returns
        -------
        dict[int, BaseStationPayload]
            The simplified base station data.
        """
        simplified_base_station_data: dict[int, BaseStationPayload] = {}
        for station_id, station_data in base_station_data.items():
            station_data.uplink_data = [
                x * self._compression_factor for x in station_data.uplink_data
            ]
            simplified_base_station_data[station_id] = station_data
            # TODO: Add more data processing techniques here.

        return simplified_base_station_data
