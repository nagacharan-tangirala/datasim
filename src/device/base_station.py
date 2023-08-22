import logging

from mesa import Agent
from numpy import ndarray

from src.core.constants import MainKey, ModelName, ModelType
from src.device.activation import ActivationSettings
from src.device.hardware import ComputingHardware, NetworkHardware
from src.device.payload import (
    BaseStationPayload,
    BaseStationResponse,
    VehiclePayload,
    VehicleResponse,
)
import src.models.model_factory as model_factory

logger = logging.getLogger(__name__)


class BaseStation(Agent):
    def __init__(
        self,
        base_station_id,
        computing_hardware: ComputingHardware,
        wireless_hardware: NetworkHardware,
        wired_hardware: NetworkHardware,
        activation_settings: ActivationSettings,
        base_station_models_data: dict,
    ):
        """
        Initialize the base station.

        Parameters
        ----------
        base_station_id : int
            The id of the base station.
        computing_hardware : ComputingHardware
            The computing hardware of the base station.
        wireless_hardware : NetworkHardware
            The wireless hardware of the base station.
        wired_hardware : NetworkHardware
            The wired hardware of the base station.
        activation_settings : ActivationSettings
            The activation settings of the base station.
        base_station_models_data : dict
            The model data of the base station.
        """
        super().__init__(base_station_id, None)
        self.type: str = MainKey.BASE_STATIONS
        self.model = None

        self._location: list[float] = []

        self._wired_hardware: NetworkHardware = wired_hardware
        self._computing_hardware: ComputingHardware = computing_hardware
        self._wireless_hardware: NetworkHardware = wireless_hardware
        self._activation_settings: ActivationSettings = activation_settings

        # Incoming vehicle data from the vehicles, set by the edge orchestrator
        self._uplink_vehicle_data: dict[int, VehiclePayload] = {}

        # Uplink payload generated at the base station after receiving the vehicle data
        self._uplink_payload: BaseStationPayload | None = None

        # Downlink response received from the controllers
        self.downlink_response: BaseStationResponse | None = None

        # Downlink responses generated at the base station
        # after receiving the controller response
        self._downlink_vehicle_data: dict[int, VehicleResponse] = {}

        self._create_models(base_station_models_data)

        # These are the output metrics
        self._received_veh_data_size: float = 0
        self._simplified_veh_data_size: float = 0
        self._vehicles_in_range: int = 0

        logger.debug(f"Base station {self.unique_id} created.")

    @property
    def location(self) -> list[float]:
        """Get the location of the base station."""
        return self._location

    @property
    def uplink_payload(self) -> BaseStationPayload:
        """Get the uplink payload."""
        return self._uplink_payload

    @property
    def downlink_vehicle_data(self) -> dict[int, VehicleResponse]:
        """Get the downlink vehicle data."""
        return self._downlink_vehicle_data

    @property
    def received_veh_data_size(self) -> float:
        """Get the received vehicle data size."""
        return self._received_veh_data_size

    @property
    def simplified_veh_data_size(self) -> float:
        """Get the simplified vehicle data size."""
        return self._simplified_veh_data_size

    @property
    def vehicles_in_range(self) -> int:
        """Get the number of vehicles in range."""
        return self._vehicles_in_range

    @property
    def data_generated_at_device(self) -> float:
        """Get the data generated at the device."""
        return -1.0

    def get_activation_times(self) -> ndarray[int]:
        """
        Get the activation times of the vehicle.
        """
        return self._activation_settings.enable_times

    def get_deactivation_times(self) -> ndarray[int]:
        """
        Get the deactivation times of the vehicle.
        """
        return self._activation_settings.disable_times

    def update_mobility_data(self, mobility_data: dict | list[float]) -> None:
        """
        Update the mobility data of the base station.
        """
        match self._mobility_model.type:
            case ModelType.STATIC:
                logger.debug(f"Updating position for base station {self.unique_id}")
                self._mobility_model.update_position(mobility_data)
            case ModelType.SIMPLE:
                logger.debug(
                    f"Updating trace for base station {self.unique_id} with "
                    f"length {len(mobility_data)}"
                )
                self._mobility_model.update_mobility_data(mobility_data)

    def activate_base_station(self, time_step: int) -> None:
        """
        Activate the base station.
        """
        # Place the base station at the correct position
        self._mobility_model.current_time = time_step
        self._mobility_model.step()
        self._location = self._mobility_model.current_location
        self.model.space.place_agent(self, self._location)

    def deactivate_base_station(self, time_step: int) -> None:
        """
        Deactivate the base station.
        """
        pass

    def set_uplink_vehicle_data(self, incoming_data: dict[int, VehiclePayload]) -> None:
        """
        Set the incoming data for the base station.
        """
        self._uplink_vehicle_data = incoming_data
        logger.debug(
            f"Vehicles near base station {self.unique_id} are "
            f"{[x.source for x in self._uplink_vehicle_data.values()]}"
            f" at time {self.model.current_time}."
        )

    def _create_models(self, base_station_models_data: dict) -> None:
        """
        Create the models for the base station.
        """
        self._mobility_model = model_factory.create_mobility_model(
            base_station_models_data[ModelName.MOBILITY]
        )

        self._data_composer = model_factory.create_base_station_data_composer(
            base_station_models_data[ModelName.DATA_COMPOSER]
        )

        self._data_simplifier = model_factory.create_base_station_data_simplifier(
            base_station_models_data[ModelName.DATA_SIMPLIFIER]
        )

    def use_wired_for_uplink(self) -> None:
        """
        Use the network hardware to transfer data in the uplink direction.
        """
        self._wired_hardware.consume_capacity(self._uplink_payload.uplink_data_size)

    def use_wired_for_downlink(self) -> None:
        """
        Use the network hardware to transfer data in the downlink direction.
        """
        self._wired_hardware.consume_capacity(sum(self.downlink_response.downlink_data))

    def use_wireless_for_uplink(self) -> None:
        """
        Use the network hardware to transfer data in the uplink direction.
        """
        # Find the data size of the uplink data
        uplink_data_size = 0.0
        for vehicle_payload in self._uplink_vehicle_data.values():
            uplink_data_size += vehicle_payload.total_data_size

        self._wireless_hardware.consume_capacity(uplink_data_size)

    def use_wireless_for_downlink(self) -> None:
        """
        Use the network hardware to transfer data in the downlink direction.
        """
        self._wireless_hardware.consume_capacity(
            sum(self.downlink_response.downlink_data)
        )

    def uplink_stage(self) -> None:
        """
        Uplink stage of the base station.

        Create data to be sent to the central controller.
        """
        self.downlink_response = None
        self._downlink_vehicle_data.clear()

        logger.debug(
            f"Uplink stage for base station {self.unique_id} "
            f"at time {self.model.current_time}."
        )

        self._mobility_model.current_time = self.model.current_time
        self._mobility_model.step()

        if self._mobility_model.type != ModelType.STATIC:
            self._location = self._mobility_model.current_location
            self.model.space.move_agent(self, self._location)

        # Create base station payload if the bs has received data from the vehicles.
        self._uplink_payload = self._data_composer.compose_basestation_payload(
            self.model.current_time, self._uplink_vehicle_data
        )
        self._received_veh_data_size = self._uplink_payload.uplink_data_size
        self._vehicles_in_range = len(self._uplink_payload.sources)

        # Use the data processor to process the data.
        self._uplink_payload = self._data_simplifier.simplify_data(self._uplink_payload)
        self._simplified_veh_data_size = self._uplink_payload.uplink_data_size

    def downlink_stage(self) -> None:
        """
        Downlink stage of the base station.
        """
        self._uplink_vehicle_data.clear()

        logger.debug(
            f"Downlink stage for base station {self.unique_id}"
            f" at time {self.model.current_time}."
        )
        vehicle_index_in_data = 0
        for vehicle_id in self.downlink_response.destination_vehicles:
            if vehicle_id == -1:
                vehicle_index_in_data += 1
                continue

            # Create the downlink vehicle response.
            self._downlink_vehicle_data[vehicle_id] = VehicleResponse(
                destination=vehicle_id,
                status=True,
                timestamp=self.model.current_time,
                downlink_data=self.downlink_response.downlink_data[
                    vehicle_index_in_data
                ],
            )
            vehicle_index_in_data += 1
