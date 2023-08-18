import logging
from dataclasses import dataclass

from device.payload import (
    BaseStationPayload,
    BaseStationResponse,
    DataPayload,
    VehiclePayload,
)

import src.core.constants as constants

logger = logging.getLogger(__name__)


@dataclass
class DataSource:
    data_type: str = ""
    data_size: float = 0.0
    data_counts: float = 0.0
    data_priority: int = 0
    side_link: str = "no"


class VehicleDataComposer:
    def __init__(self, data_source_params: dict[dict]):
        """
        Initialize the data composer.

        Parameters
        ----------
        data_source_params : dict[dict]
            The data source parameters from the config file.
        """
        self._all_data_sources: list[DataSource] = []
        self._side_links_sources: list[DataSource] = []

        self.previous_time: int = 0
        self._create_data_sources(data_source_params[constants.DATA_SOURCE])

    def _create_data_sources(self, data_source_params: dict) -> None:
        """
        Create the data sources.

        Parameters
        ----------
        data_source_params : dict
            The data source parameters from the config file.

        Returns
        -------
        None
        """
        for params in data_source_params:
            data_source = DataSource()

            data_source.data_type = params[constants.DATA_SOURCE_TYPE]
            data_source.data_counts = params[constants.DATA_COUNTS]
            data_source.data_size = params[constants.DATA_SIZE]
            data_source.data_priority = params[constants.DATA_PRIORITY]
            data_source.side_link = params[constants.DATA_SIDE_LINK]

            self._all_data_sources.append(data_source)
            if data_source.side_link == "yes":
                self._side_links_sources.append(data_source)

    def compose_uplink_payload(self, current_time: int) -> VehiclePayload:
        """
        Compose uplink payload using all the data sources.

        Parameters
        ----------
        current_time : int
            The current time.

        Returns
        -------
        VehiclePayload
            The uplink payload.
        """
        uplink_payload = self.compose_payload_with_sources(
            current_time, self._all_data_sources
        )
        return uplink_payload

    def compose_sidelink_payload(self, current_time: int):
        """
        Compose sidelink payload using all the side link data sources.

        Parameters
        ----------
        current_time : int
            The current time.

        Returns
        -------
        VehiclePayload
            The sidelink payload.
        """
        sidelink_payload = self.compose_payload_with_sources(
            current_time, self._side_links_sources
        )
        self.previous_time = current_time
        return sidelink_payload

    def compose_payload_with_sources(
        self, current_time: int, data_sources: list[DataSource]
    ) -> VehiclePayload:
        """
        Compose vehicle payload using the data sources.

        Parameters
        ----------
        current_time : int
            The current time.
        data_sources : list[DataSource]
            The data sources.

        Returns
        -------
        VehiclePayload
            The vehicle payload.
        """
        # Collect data from all the data sources and create data payload
        data_payloads = []
        all_data_size = 0.0
        for data_source in data_sources:
            data_payload = DataPayload()
            data_payload.type = data_source.data_type

            # Calculate the number of units generated in the time interval
            data_counts = data_source.data_counts * (current_time - self.previous_time)
            data_payload.count = int(data_counts)

            # Calculate the data size and add to the payload
            data_payload.data_size = data_source.data_size * data_counts
            all_data_size += data_payload.data_size
            data_payloads.append(data_payload)

        # Create the vehicle payload
        vehicle_payload = VehiclePayload()
        vehicle_payload.timestamp = current_time
        vehicle_payload.total_data_size = all_data_size
        vehicle_payload.data_payload_list = data_payloads

        assert vehicle_payload.total_data_size >= 0, "Uplink data size is negative."
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
            base_station_payload.uplink_data_size += vehicle_payload.total_data_size
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
