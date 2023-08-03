import logging

from src.application.application_settings import ApplicationSettings
from src.application.payload import *
from src.device.computing_hardware import ComputingHardware

logger = logging.getLogger(__name__)


class VehicleAppRunner:
    def __init__(
        self,
        device_id: int,
        application_settings: list[ApplicationSettings],
        hardware_settings: ComputingHardware,
    ):
        """
        Initialize the vehicle application runner model.
        """
        self._device_id: int = device_id
        self._application_settings: list[ApplicationSettings] = application_settings
        self._hardware_settings: ComputingHardware = hardware_settings

    @property
    def device_id(self) -> int:
        """Get the device id."""
        return self._device_id

    def generate_vehicle_payload(self, current_time: int) -> VehiclePayload:
        """
        Generate data request by running the applications.
        """
        logger.debug(
            f"Generating vehicle payload for device {self._device_id} at time {current_time}"
        )
        # Collect the hardware requirements for the applications
        payload_request: VehiclePayload = VehiclePayload()
        payload_request.timestamp = current_time
        payload_request.source = self._device_id

        for application in self._application_settings:
            if not application.is_active(current_time):
                continue
            payload_request.cpu_required += application.cpu_required
            payload_request.memory_required += application.memory_required
            payload_request.gpu_required += application.gpu_required
            payload_request.battery_required += application.battery_required
            payload_request.storage_required += application.storage_required

            # Collect the uplink and downlink data
            payload_request.uplink_data += application.uplink_data

        return payload_request

    def process_result(self, response: VehicleResponse) -> None:
        """
        Process the result and send it to relevant applications.
        """
        # Applications are not interested in the response. They just want to know if the data was sent or not.
        if response.status:
            logger.debug(
                f"Data transfer from vehicle {self._device_id} at time {response.timestamp} was successful."
            )
