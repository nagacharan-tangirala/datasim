import logging

from src.application.payload import BaseStationResponse, BaseStationPayload
from src.device.computing_hardware import ComputingHardware

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

        self._vehicle_count: int = 0
        self._data_count: int = 0

    @property
    def device_id(self) -> int:
        """Get the device id."""
        return self._device_id

    @property
    def vehicle_count(self) -> int:
        """Get the vehicle count."""
        return self._vehicle_count

    @property
    def data_count(self) -> int:
        """Get the data count."""
        return self._data_count

    def process_incoming_data(
        self, incoming_data: dict[int, BaseStationPayload]
    ) -> None:
        """
        Process the incoming data.

        Parameters
        ----------
        incoming_data : dict[int, BaseStationPayload]
            The incoming data.
        """
        self._vehicle_count: int = 0
        self._data_count: int = 0
        # Count the number of vehicles
        for _, payload in incoming_data.items():
            valid_sources = [source for source in payload.sources if source != -1]
            self._vehicle_count += len(valid_sources)

        # Count the incoming data
        for _, payload in incoming_data.items():
            self._data_count += sum(payload.uplink_data)

    def generate_basestation_response(
        self, current_time: int, incoming_data: dict[int, BaseStationPayload]
    ) -> dict[int, BaseStationResponse]:
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
        logger.debug(
            f"Generating response for base station {self._device_id} at time {current_time}"
        )
        base_station_responses: dict[int, BaseStationResponse] = {}

        for station_id, base_station_payload in incoming_data.items():
            response: BaseStationResponse = BaseStationResponse()
            response.status = True
            response.timestamp = current_time
            response.destination_vehicles = base_station_payload.sources
            response.downlink_data = [1.0 for _ in base_station_payload.uplink_data]
            base_station_responses[station_id] = response

        return base_station_responses
