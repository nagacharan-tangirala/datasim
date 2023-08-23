import logging
from dataclasses import dataclass

from core.common_constants import DeviceName
from core.exceptions import InvalidDataTargetError
from device.payload import (
    BaseStationPayload,
    BaseStationResponse,
    DataPayload,
    RSUPayload,
    VehiclePayload,
)

from src.core.constants import DataSourceKey, DataTargetType, ModelName

logger = logging.getLogger(__name__)


@dataclass
class DataSource:
    data_type: str = ""
    data_size: float = 0.0
    data_counts: float = 0.0
    data_priority: int = 0


class VehicleDataComposer:
    def __init__(self, data_source_params: dict):
        """
        Initialize the data composer.

        Parameters
        ----------
        data_source_params : dict
            The data source parameters from the config file.
        """
        self._v2r_data_sources: list[DataSource] = []
        self._v2v_data_sources: list[DataSource] = []
        self._v2b_data_sources: list[DataSource] = []

        self.previous_time: int = 0
        self._create_data_sources(data_source_params[ModelName.DATA_SOURCE])

    def _create_data_sources(self, data_source_params: dict) -> None:
        """
        Creates the data sources for the device.

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

            data_source.data_type = params[DataSourceKey.SOURCE_TYPE]
            data_source.data_counts = params[DataSourceKey.COUNTS]
            data_source.data_size = params[DataSourceKey.SIZE]
            data_source.data_priority = params[DataSourceKey.PRIORITY]
            data_source.data_target_type = params[DataSourceKey.TARGET_TYPE]

            match data_source.data_target_type:
                case DataTargetType.BASE_STATION:
                    self._v2b_data_sources.append(data_source)
                case DataTargetType.ROADSIDE_UNIT:
                    self._v2r_data_sources.append(data_source)
                case DataTargetType.VEHICLE:
                    self._v2v_data_sources.append(data_source)
                case _:
                    raise InvalidDataTargetError(
                        data_source.data_target_type, DeviceName.VEHICLES
                    )

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

        return vehicle_payload

    def compose_v2b_payload(self, current_time: int) -> VehiclePayload:
        """
        Compose v2b payload using all the data sources.

        Parameters
        ----------
        current_time : int
            The current time.

        Returns
        -------
        VehiclePayload
            The v2b payload.
        """
        v2b_payload = self.compose_payload_with_sources(
            current_time, self._v2b_data_sources
        )
        return v2b_payload

    def compose_v2v_payload(self, current_time: int) -> VehiclePayload:
        """
        Compose v2v payload using the data sources.

        Parameters
        ----------
        current_time : int
            The current time.

        Returns
        -------
        VehiclePayload
            The v2v payload.
        """
        v2v_payload = self.compose_payload_with_sources(
            current_time, self._v2v_data_sources
        )
        return v2v_payload

    def compose_v2r_payload(self, current_time: int) -> VehiclePayload:
        """
        Compose v2r payload using the data sources.

        Parameters
        ----------
        current_time : int
            The current time.

        Returns
        -------
        VehiclePayload
            The v2r payload.
        """
        v2r_payload = self.compose_payload_with_sources(
            current_time, self._v2r_data_sources
        )
        return v2r_payload


class BaseStationDataComposer:
    def __init__(self, data_source_params: dict):
        """
        Initialize the data composer.

        Parameters
        ----------
        data_source_params : dict
            The data source parameters from the config file.
        """
        self.model_data = data_source_params
        self._previous_time: int = 0

    def compose_basestation_payload(
        self, current_time: int, incoming_data: dict[int, VehiclePayload]
    ) -> BaseStationPayload:
        """
        Generate the base station payload.
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


class RSUDataComposer:
    def __init__(self, model_data: dict):
        """
        Initialize the data composer.
        """
        self.model_data = model_data
        self._r2r_data_sources: list[DataSource] = []
        self._r2b_data_sources: list[DataSource] = []

        self.previous_time: int = 0

    def _create_data_sources(self, data_source_params: dict) -> None:
        """
        Creates the data sources for the device.

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

            data_source.data_type = params[DataSourceKey.SOURCE_TYPE]
            data_source.data_counts = params[DataSourceKey.COUNTS]
            data_source.data_size = params[DataSourceKey.SIZE]
            data_source.data_priority = params[DataSourceKey.PRIORITY]
            data_source.data_target_type = params[DataSourceKey.TARGET_TYPE]

            match data_source.data_target_type:
                case DataTargetType.BASE_STATION:
                    self._r2b_data_sources.append(data_source)
                case _:
                    raise InvalidDataTargetError(
                        data_source.data_target_type, DeviceName.VEHICLES
                    )

    def _compose_payload_with_sources(
        self, current_time: int, data_sources: list[DataSource]
    ) -> RSUPayload:
        """
        Compose RSU payload using the data sources.

        Parameters
        ----------
        current_time : int
            The current time.
        data_sources : list[DataSource]
            The data sources.

        Returns
        -------
        RSUPayload
            The RSU payload.
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

        # Create the rsu payload
        rsu_payload = RSUPayload()
        rsu_payload.timestamp = current_time
        rsu_payload.total_data_size = all_data_size
        rsu_payload.data_payload_list = data_payloads

        return rsu_payload

    def compose_r2b_payload(self, current_time: int) -> RSUPayload:
        """
        Generate payload to send to the base station.
        """
        r2b_payload = self._compose_payload_with_sources(
            current_time, self._r2b_data_sources
        )
        return r2b_payload

    def compose_r2r_payload(self, current_time: int) -> RSUPayload:
        """
        Generate payload to send to the base station.
        """
        r2r_payload = self._compose_payload_with_sources(
            current_time, self._r2r_data_sources
        )
        return r2r_payload


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
