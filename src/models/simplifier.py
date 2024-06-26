import src.core.constants as constants
from src.device.payload import VehiclePayload, BaseStationPayload

__all__ = ["VehicleDataSimplifier", "BaseStationDataSimplifier"]


class VehicleDataSimplifier:
    def __init__(self, model_data: dict):
        """
        Simplify the vehicle data.
        """
        self._retention_ratio: float = model_data[constants.RETENTION_FACTOR]
        self._compression_ratio: float = model_data[constants.COMPRESSION_FACTOR]

    def simplify_data(self, veh_payload: VehiclePayload) -> VehiclePayload:
        """
        Simplify the vehicle data.
        """
        # Simplify the data.
        for idx in range(len(veh_payload.data_payload_list)):
            veh_payload.data_payload_list[idx].data_size = (
                veh_payload.data_payload_list[idx].data_size * self._compression_ratio
            )
            veh_payload.data_payload_list[idx].count = (
                veh_payload.data_payload_list[idx].count * self._compression_ratio
            )

        return veh_payload


class BaseStationDataSimplifier:
    def __init__(self, model_data: dict):
        """
        Simplify the vehicle data.
        """
        pass

    def simplify_data(
        self, base_station_payload: BaseStationPayload
    ) -> BaseStationPayload:
        """
        Simplify the base station payload.
        """
        # Simplify the data.
        return base_station_payload
