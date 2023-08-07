import logging

import src.core.constants as constants
from src.device.payload import *

logger = logging.getLogger(__name__)


@dataclass
class DataSource:
    data_type: str = ""
    data_size: float = 0.0
    data_counts: float = 0.0


class VehicleDataComposer:
    def __init__(self, data_source_params: dict[dict]):
        """
        Initialize the data composer.
        """
        self._data_sources: list[DataSource] = []

        self.previous_time: int = 0
        self._create_data_sources(data_source_params[constants.DATA_SOURCE])

    def _create_data_sources(self, data_source_params: dict) -> None:
        """
        Create the data sources.
        """
        for params in data_source_params:
            data_source = DataSource()

            data_source.data_type = params[constants.DATA_SOURCE_TYPE]
            data_source.data_counts = params[constants.DATA_COUNTS]
            data_source.data_size = params[constants.DATA_SIZE]

            self._data_sources.append(data_source)

    def compose_vehicle_payload(self, current_time: int) -> VehiclePayload:
        """
        Generate data request by running the applications.
        """
        # Collect data from all the data sources and create data payload
        data_payloads = []
        for data_source in self._data_sources:
            data_payload = DataPayload()
            data_payload.type = data_source.data_type

            # Calculate the number of units generated in the time interval
            data_counts = data_source.data_counts * (current_time - self.previous_time)
            data_payload.count = int(data_counts)

            # Calculate the data size and add to the payload
            data_payload.data_size = data_source.data_size * data_counts
            data_payloads.append(data_payload)

        # Create the vehicle payload
        vehicle_payload = VehiclePayload()
        vehicle_payload.timestamp = current_time
        vehicle_payload.uplink_data_size = sum(
            [data.data_size for data in data_payloads]
        )
        vehicle_payload.uplink_payload = data_payloads

        assert vehicle_payload.uplink_data_size >= 0, "Uplink data size is negative."

        self.previous_time = current_time
        return vehicle_payload


class BaseStationDataComposer:
    def __init__(self, model_data: dict):
        """
        Initialize the data composer.
        """
        self.model_data = model_data
        self._previous_time: int = 0

    def compose_basestation_payload(
        self, current_time: int, incoming_data: dict[int, VehiclePayload]
    ) -> BaseStationPayload:
        """
        Generate data request by running the applications.
        """
        base_station_payload: BaseStationPayload = BaseStationPayload()
        base_station_payload.timestamp = current_time

        for vehicle_id, vehicle_payload in incoming_data.items():
            base_station_payload.uplink_data_size += vehicle_payload.uplink_data_size
            base_station_payload.sources.append(vehicle_id)

            # Collect the uplink and downlink data
            base_station_payload.uplink_data.append(vehicle_payload)

        self._previous_time = current_time
        return base_station_payload


class ControllerDataComposer:
    def __init__(self, model_data: dict):
        """
        Initialize the data composer.
        """
        self.model_data = model_data
        self._previous_time: int = 0

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
        base_station_responses: dict[int, BaseStationResponse] = {}

        for station_id, base_station_payload in incoming_data.items():
            response: BaseStationResponse = BaseStationResponse()
            response.status = True
            response.timestamp = current_time
            response.destination_vehicles = base_station_payload.sources
            response.downlink_data = [1.0 for _ in base_station_payload.uplink_data]
            base_station_responses[station_id] = response

        self._previous_time = current_time
        return base_station_responses
