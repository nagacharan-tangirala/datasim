import logging

from src.application.Payload import BaseStationResponse, BaseStationPayload
from src.device.ComputingHardware import ComputingHardware

logger = logging.getLogger(__name__)


class ControllerAppRunner:
    def __init__(self, device_id: int, computing_hardware: ComputingHardware):
        """
        Initialize the controller application runner model.

        Parameters
        ----------
        device_id : int
            The id of the device.
        computing_hardware : ComputingHardware
            The hardware settings of the device.
        """
        self._device_id: int = device_id
        self._hardware_settings: ComputingHardware = computing_hardware

    @property
    def device_id(self) -> int:
        """ Get the device id. """
        return self._device_id

    def generate_basestation_response(self,
                                      current_time: int,
                                      incoming_data: dict[int, BaseStationPayload]) -> dict[int, BaseStationResponse]:
        """
        Generate response by running the applications.

        Parameters
        ----------
        current_time : int
            The current time.
        incoming_data : dict[int, BaseStationPayload]
            The incoming data.

        Returns
        -------
        dict[int, BaseStationResponse]
            The response of the controller.
        """
        logger.debug(f"Generating response for base station {self._device_id} at time {current_time}")
        base_station_responses: dict[int, BaseStationResponse] = {}

        for station_id, base_station_payload in incoming_data.items():
            response: BaseStationResponse = BaseStationResponse()
            response.status = True
            response.timestamp = current_time
            response.destination_vehicles = base_station_payload.sources
            response.downlink_data = ([1.0 for _ in base_station_payload.uplink_data])
            base_station_responses[station_id] = response

        return base_station_responses
