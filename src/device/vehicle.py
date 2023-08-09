import logging

from mesa import Agent
from numpy import ndarray
from pandas import DataFrame

import src.core.constants as constants
from src.device.activation import ActivationSettings
from src.device.hardware import *
from src.device.payload import VehiclePayload, VehicleResponse
from src.models.model_factory import ModelFactory

logger = logging.getLogger(__name__)


class Vehicle(Agent):
    def __init__(
        self,
        vehicle_id: int,
        computing_hardware: ComputingHardware,
        wireless_hardware: NetworkHardware,
        activation_settings: ActivationSettings,
        vehicle_models: dict,
    ) -> None:
        """
        Initialize the vehicle.

        Parameters
        ----------
        vehicle_id : int
            The id of the vehicle.
        computing_hardware : ComputingHardware
            The computing hardware of the vehicle.
        wireless_hardware : NetworkHardware
            The wireless hardware of the vehicle.
        activation_settings : ActivationSettings
            The activation settings of the vehicle.
        vehicle_models : dict
            The model data of the vehicle.
        """
        super().__init__(vehicle_id, None)

        self._location: list[float] = []
        self.sim_model = None

        self._uplink_payload: VehiclePayload | None = None
        self.sidelink_payload: VehiclePayload | None = None
        self._downlink_response: VehicleResponse | None = None

        # Received data from other vehicles
        self.sidelink_received_data: dict[int, VehiclePayload] = {}

        self._computing_hardware: ComputingHardware = computing_hardware
        self._network_hardware: NetworkHardware = wireless_hardware
        self._activation_settings: ActivationSettings = activation_settings

        self.selected_bs: int = -1
        self._previous_bs: int = -1

        self._create_models(vehicle_models)

    @property
    def uplink_payload(self) -> VehiclePayload:
        """Get the uplink payload."""
        return self._uplink_payload

    @property
    def downlink_response(self) -> VehicleResponse:
        """Get the downlink response."""
        return self._downlink_response

    @downlink_response.setter
    def downlink_response(self, response: VehicleResponse) -> None:
        """Set the downlink response."""
        self._downlink_response = response

    @property
    def location(self) -> list[float, float]:
        """Get the location of the vehicle."""
        return self._location

    @property
    def handover_count(self) -> int:
        """Check if the vehicle is in a handover."""
        return 1 if self._previous_bs != self.selected_bs else 0

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

    def _create_models(self, model_data: dict) -> None:
        """
        Create the models for this vehicle.
        """
        logger.debug(f"Creating models for vehicle {self.unique_id}")
        model_factory = ModelFactory()

        self._mobility_model = model_factory.create_mobility_model(
            model_data[constants.MOBILITY]
        )

        self._data_composer = model_factory.create_vehicle_data_composer(
            model_data[constants.DATA_COMPOSER]
        )

        self._data_simplifier = model_factory.create_vehicle_data_simplifier(
            model_data[constants.DATA_SIMPLIFIER]
        )

        self._data_collector = model_factory.create_vehicle_data_collector(
            model_data[constants.DATA_COLLECTOR]
        )

    def update_mobility_data(self, mobility_data: DataFrame | list[float]) -> None:
        """
        Update the mobility data depending on the mobility model.

        Parameters
        ----------
        mobility_data : DataFrame | list[float]
            The mobility data to update.
        """
        match self._mobility_model.type:
            case "static":
                logger.debug(f"Updating position for vehicle {self.unique_id}")
                self._mobility_model.update_position(mobility_data)
            case "trace":
                logger.debug(
                    f"Updating trace for vehicle {self.unique_id} with length {len(mobility_data)}"
                )
                self._mobility_model.update_positions(mobility_data)

    def activate_vehicle(self, time_step: int) -> None:
        """
        Activate the vehicle if the time step is correct.
        """
        # Set previous time for data composer
        self._data_composer.previous_time = time_step

    def deactivate_vehicle(self, time_step: int) -> None:
        """
        Deactivate the vehicle if the time step is correct.
        """
        pass

    def use_network_for_uplink(self) -> None:
        """
        Use the network hardware to transfer data in the uplink direction.
        """
        self._network_hardware.consume_capacity(self._uplink_payload.total_data_size)

    def use_network_for_sidelink(self, data_size: float) -> None:
        """
        Use the network hardware to transfer data in the sidelink direction.
        """
        self._network_hardware.consume_capacity(data_size)

    def use_network_for_downlink(self) -> None:
        """
        Use the network hardware to transfer data in the downlink direction.
        """
        self._network_hardware.consume_capacity(self._downlink_response.downlink_data)

    def uplink_stage(self) -> None:
        """
        Downlink stage for the vehicle.
        """
        logger.debug(
            f"Uplink stage for vehicle {self.unique_id} at time {self.sim_model.current_time}"
        )

        # Update the previous base station
        self._previous_bs = self.selected_bs

        # Propagate the mobility model and get the current location
        self._mobility_model.current_time = self.sim_model.current_time
        self._mobility_model.step()
        self._location = self._mobility_model.current_location

        # Compose the data using the data composer
        self._uplink_payload = self._data_composer.compose_uplink_payload(
            self.sim_model.current_time
        )
        self._uplink_payload.source = self.unique_id
        self._uplink_payload = self._data_simplifier.simplify_data(self._uplink_payload)

        # Compose the side link payload
        self.sidelink_payload = self._data_composer.compose_sidelink_payload(
            self.sim_model.current_time
        )

    def downlink_stage(self) -> None:
        """
        Downlink stage for the vehicle.
        """
        logger.debug(
            f"Downlink stage for vehicle {self.unique_id} at time {self.sim_model.current_time}"
        )

        self._data_collector.collect_data(self.sidelink_received_data)
