import src.core.constants as constants
from src.device.payload import VehiclePayload, BaseStationPayload


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
        for idx in range(len(veh_payload.uplink_payload)):
            veh_payload.uplink_payload[idx].data_size = (
                veh_payload.uplink_payload[idx].data_size * self._compression_ratio
            )
            veh_payload.uplink_payload[idx].count = (
                veh_payload.uplink_payload[idx].count * self._compression_ratio
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
