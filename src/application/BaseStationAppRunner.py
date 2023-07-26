import logging

from src.application.Payload import VehiclePayload, BaseStationPayload, BaseStationResponse
from src.device.ComputingHardware import ComputingHardware

logger = logging.getLogger(__name__)


class BaseStationAppRunner:
    def __init__(self, device_id: int, hardware_settings: ComputingHardware):
        """
        Initialize the base station application runner model.
        """
        self._device_id: int = device_id
        self._hardware_settings: ComputingHardware = hardware_settings

    @property
    def device_id(self) -> int:
        """ Get the device id. """
        return self._device_id

    def generate_basestation_payload(self,
                                     current_time: int,
                                     incoming_data: dict[int, VehiclePayload]) -> BaseStationPayload:
        """
        Generate data request by running the applications.
        """
        logger.debug(f"Generating payload for base station {self._device_id} at time {current_time}")
        base_station_payload_request: BaseStationPayload = BaseStationPayload()
        base_station_payload_request.timestamp = current_time

        for vehicle_id, payload_request in incoming_data.items():
            base_station_payload_request.cpu_required += payload_request.cpu_required
            base_station_payload_request.memory_required += payload_request.memory_required
            base_station_payload_request.gpu_required += payload_request.gpu_required
            base_station_payload_request.battery_required += payload_request.battery_required
            base_station_payload_request.storage_required += payload_request.storage_required

            # Collect the uplink and downlink data
            base_station_payload_request.uplink_data.append(payload_request.uplink_data)
            base_station_payload_request.sources.append(vehicle_id)

        return base_station_payload_request

    def process_result(self, response: BaseStationResponse) -> None:
        """
        Process the result and send it to relevant applications.
        """
        # Applications are not interested in the response. They just want to know if the data was sent or not.
        if response.status:
            # logger.debug(f"Data transfer from {self._device_id} at time {response.timestamp} was successful.")
            pass
