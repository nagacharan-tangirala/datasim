import logging

from mesa import Agent
from numpy import ndarray

import src.core.constants as constants
from src.core.exceptions import (
    WrongActivationTimeError,
    WrongDeactivationTimeError,
)
from src.device.activation import ActivationSettings
from src.device.hardware import ComputingHardware, NetworkHardware
from src.device.payload import (
    VehiclePayload,
    BaseStationPayload,
    BaseStationResponse,
    VehicleResponse,
)
from src.models.model_factory import ModelFactory

logger = logging.getLogger(__name__)


class BaseStation(Agent):
    def __init__(
        self,
        base_station_id,
        base_station_position: ndarray[float],
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
        base_station_position : ndarray[float]
            The position of the base station.
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

        self._location: ndarray[float] = []
        self.sim_model = None

        self._wired_hardware: NetworkHardware = wired_hardware
        self._computing_hardware: ComputingHardware = computing_hardware
        self._wireless_hardware: NetworkHardware = wireless_hardware
        self._activation_settings: ActivationSettings = activation_settings

        # Incoming vehicle data from the vehicles, set by the edge orchestrator
        self._uplink_vehicle_data: dict[int, VehiclePayload] = {}

        # Uplink payload generated at the base station after receiving the vehicle data
        self._uplink_payload: BaseStationPayload | None = None

        # Downlink response received from the controllers
        self._downlink_response: BaseStationResponse | None = None

        # Downlink responses generated at the base station after receiving the controller response
        self._downlink_vehicle_data: dict[int, VehicleResponse] = {}

        # Add the position to the base station models data
        base_station_models_data[constants.MOBILITY][
            constants.POSITION
        ] = base_station_position
        self._create_models(base_station_models_data)

        logger.debug(f"Base station {self.unique_id} created.")

    @property
    def location(self) -> ndarray[float]:
        """Get the location of the base station."""
        return self._location

    @property
    def start_time(self) -> int:
        """Get the start time."""
        return self._activation_settings.start_time

    @property
    def end_time(self) -> int:
        """Get the end time."""
        return self._activation_settings.end_time

    @property
    def uplink_payload(self) -> BaseStationPayload:
        """Get the uplink payload."""
        return self._uplink_payload

    @property
    def downlink_response(self) -> BaseStationResponse:
        """Get the downlink response."""
        return self._downlink_response

    @downlink_response.setter
    def downlink_response(self, response: BaseStationResponse) -> None:
        """Set the downlink response."""
        self._downlink_response = response

    @property
    def downlink_vehicle_data(self) -> dict[int, VehicleResponse]:
        """Get the downlink vehicle data."""
        return self._downlink_vehicle_data

    def activate_base_station(self, time_step: int) -> None:
        """
        Activate the base station.
        """
        if self._activation_settings.start_time != time_step:
            raise WrongActivationTimeError(
                self._activation_settings.start_time, time_step
            )

    def deactivate_base_station(self, time_step: int) -> None:
        """
        Deactivate the base station.
        """
        if self._activation_settings.end_time != time_step:
            raise WrongDeactivationTimeError(
                self._activation_settings.end_time, time_step
            )

    def set_uplink_vehicle_data(self, incoming_data: dict[int, VehiclePayload]) -> None:
        """
        Set the incoming data for the base station.
        """
        self._uplink_vehicle_data = incoming_data
        logger.debug(
            f"Vehicles near base station {self.unique_id} are "
            f"{[x.source for x in self._uplink_vehicle_data.values()]} at time {self.sim_model.current_time}."
        )

    def _create_models(self, base_station_models_data: dict) -> None:
        """
        Create the models for the base station.
        """
        model_factory = ModelFactory()
        self._mobility_model = model_factory.create_mobility_model(
            base_station_models_data[constants.MOBILITY]
        )

        self._data_composer = model_factory.create_base_station_data_composer(
            base_station_models_data[constants.DATA_COMPOSER]
        )

        self._data_simplifier = model_factory.create_base_station_data_simplifier(
            base_station_models_data[constants.DATA_SIMPLIFIER]
        )

    def use_wired_for_uplink(self) -> None:
        """
        Use the network hardware to transfer data in the uplink direction.
        """
        self._wired_hardware.consume_capacity(sum(self._uplink_payload.uplink_data))

    def use_wired_for_downlink(self) -> None:
        """
        Use the network hardware to transfer data in the downlink direction.
        """
        self._wired_hardware.consume_capacity(
            sum(self._downlink_response.downlink_data)
        )

    def use_wireless_for_uplink(self) -> None:
        """
        Use the network hardware to transfer data in the uplink direction.
        """
        self._wireless_hardware.consume_capacity(sum(self._uplink_payload.uplink_data))

    def use_wireless_for_downlink(self) -> None:
        """
        Use the network hardware to transfer data in the downlink direction.
        """
        self._wireless_hardware.consume_capacity(
            sum(self._downlink_response.downlink_data)
        )

    def uplink_stage(self) -> None:
        """
        Uplink stage of the base station. Create data to be sent to the central controller.
        This is the third step in the overall simulation.
        """
        logger.debug(
            f"Uplink stage for base station {self.unique_id} at time {self.sim_model.current_time}."
        )
        self._mobility_model.current_time = self.sim_model.current_time
        self._mobility_model.step()
        self._location = self._mobility_model.current_location

        logger.debug(f"Generating base station payload for {self.unique_id}.")
        # Create base station payload if the base station has received data from the vehicles.
        self._uplink_payload = self._data_composer.compose_basestation_payload(
            self.sim_model.current_time, self._uplink_vehicle_data
        )

        # Use the data processor to process the data.
        self._uplink_payload = self._data_simplifier.simplify_data(self._uplink_payload)
        logger.debug(
            f"Uplink payload for base station {self.unique_id} is {self._uplink_payload}."
        )

    def downlink_stage(self) -> None:
        """
        Downlink stage of the base station.
        """
        # Clear the uplink vehicle data as the transfer is complete.
        self._uplink_vehicle_data.clear()

        logger.debug(
            f"Downlink stage for base station {self.unique_id} at time {self.sim_model.current_time}."
        )

        # Create the downlink vehicle response.
        vehicle_index_in_data = 0
        for vehicle_id in self._downlink_response.destination_vehicles:
            if vehicle_id == -1:
                vehicle_index_in_data += 1
                continue

            # Create the downlink vehicle response.
            self._downlink_vehicle_data[vehicle_id] = VehicleResponse(
                destination=vehicle_id,
                status=True,
                timestamp=self.sim_model.current_time,
                downlink_data=self._downlink_response.downlink_data[
                    vehicle_index_in_data
                ],
            )

            logger.debug(
                f"Downlink response for vehicle {vehicle_id} is {self._downlink_vehicle_data[vehicle_id]}."
            )
            vehicle_index_in_data += 1
