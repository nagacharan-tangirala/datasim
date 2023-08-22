import logging

from mesa import Agent
from numpy import ndarray
from pandas import DataFrame

from src.core.constants import MainKey, ModelName, ModelType
from src.device.activation import ActivationSettings
from src.device.hardware import ComputingHardware, NetworkHardware
from src.device.payload import VehiclePayload, VehicleResponse
import src.models.model_factory as model_factory

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
        self.model = None

        self._location: list[float] = []
        self._velocity: float = 0.0
        self.type: str = MainKey.VEHICLES

        self._v2b_payload: VehiclePayload | None = None
        self._v2v_payload: VehiclePayload | None = None
        self._v2r_payload: VehiclePayload | None = None

        self._v2b_response: VehicleResponse | None = None
        self._v2r_response: VehicleResponse | None = None
        self._v2v_response: VehicleResponse | None = None

        self._received_v2v_data: dict[int, VehiclePayload] = {}

        self._computing_hardware: ComputingHardware = computing_hardware
        self._network_hardware: NetworkHardware = wireless_hardware
        self._activation_settings: ActivationSettings = activation_settings

        self.selected_bs: int = -1
        self._previous_bs: int = -1
        self._total_data_generated: float = 0.0
        self._vehicles_in_range: int = 0

        self._create_models(vehicle_models)

    @property
    def v2b_payload(self) -> VehiclePayload:
        """Get the v2b payload."""
        return self._v2b_payload

    @property
    def v2v_payload(self) -> VehiclePayload:
        """Get the v2v payload."""
        return self._v2v_payload

    @property
    def v2r_payload(self) -> VehiclePayload:
        """Get the v2r payload."""
        return self._v2r_payload

    @property
    def data_generated_at_device(self) -> float:
        """Get the total data generated by the vehicle."""
        return self._total_data_generated

    @property
    def vehicles_in_range(self) -> int:
        """Get the number of vehicles in range."""
        return self._vehicles_in_range

    @property
    def location(self) -> list[float]:
        """Get the location of the vehicle."""
        return self._location

    @property
    def velocity(self) -> float:
        """Get the velocity of the vehicle."""
        return self._velocity

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
        self._mobility_model = model_factory.create_mobility_model(
            model_data[ModelName.MOBILITY]
        )

        self._data_composer = model_factory.create_vehicle_data_composer(
            model_data[ModelName.DATA_COMPOSER]
        )

        self._data_simplifier = model_factory.create_vehicle_data_simplifier(
            model_data[ModelName.DATA_SIMPLIFIER]
        )

        self._data_collector = model_factory.create_vehicle_data_collector(
            model_data[ModelName.DATA_COLLECTOR]
        )

    def update_mobility_data(self, mobility_data: dict | list[float]) -> None:
        """
        Update the mobility data depending on the mobility model.

        Parameters
        ----------
        mobility_data : DataFrame | list[float]
            The mobility data to update.
        """
        match self._mobility_model.type:
            case ModelType.STATIC:
                logger.debug(f"Updating position for vehicle {self.unique_id}")
                self._mobility_model.update_position(mobility_data)
            case ModelType.SIMPLE:
                logger.debug(
                    f"Updating trace for vehicle {self.unique_id} with "
                    f"length {len(mobility_data)}"
                )
                self._mobility_model.update_mobility_data(mobility_data)

    def activate_vehicle(self, time_step: int) -> None:
        """
        Activate the vehicle.
        """
        # Set previous time for data composer
        self._data_composer.previous_time = time_step

        # Get the current location of the vehicle
        self._mobility_model.current_time = self.model.current_time
        self._mobility_model.step()
        self._location = self._mobility_model.current_location

        self.model.space.place_agent(self, self._location)

    def deactivate_vehicle(self, time_step: int) -> None:
        """
        Deactivate the vehicle.
        """
        pass

    def use_network_for_v2b_payload(self) -> None:
        """
        Use the network hardware to transfer v2b payload.
        """
        self._network_hardware.consume_capacity(self._v2b_payload.total_data_size)

    def use_network_for_v2v_payload(self) -> None:
        """
        Use the network hardware to transfer v2v payload.
        """
        self._network_hardware.consume_capacity(self._v2v_payload.total_data_size)

    def use_network_for_v2r_payload(self) -> None:
        """
        Use the network hardware to transfer v2r payload.
        """
        self._network_hardware.consume_capacity(self._v2r_payload.total_data_size)

    def use_network_for_v2v_response(self, data_size: float) -> None:
        """
        Use the network hardware to receive v2v response.
        """
        self._network_hardware.consume_capacity(data_size)

    def use_network_for_v2r_response(self) -> None:
        """
        Use the network hardware to receive v2v response.
        """
        self._network_hardware.consume_capacity(self._v2b_response.downlink_data)

    def assign_v2v_data(self, payload: VehiclePayload) -> None:
        """
        Add received data from another vehicle.

        Parameters
        ----------
        payload : VehiclePayload
            The payload of the vehicle.
        """
        self._received_v2v_data[payload.source] = payload

    def use_network_for_received_v2v(self) -> None:
        """
        Use the network hardware for receiving v2v data.
        """
        # Find the data size of the uplink data
        uplink_data_size = 0.0
        for vehicle_payload in self._received_v2v_data.values():
            uplink_data_size += vehicle_payload.total_data_size

        self._network_hardware.consume_capacity(uplink_data_size)

    def uplink_stage(self) -> None:
        """
        Downlink stage for the vehicle.
        """
        logger.debug(
            f"Uplink stage for vehicle {self.unique_id} at time {self.model.current_time}"
        )

        # Update the previous base station
        self._previous_bs = self.selected_bs

        # Propagate the mobility model and get the current location
        self._mobility_model.current_time = self.model.current_time
        self._mobility_model.step()

        if self._mobility_model.type != ModelType.STATIC:
            self._location = self._mobility_model.current_location
            self.model.space.move_agent(self, self._location)

        # Compose the payloads
        self._v2b_payload = self._data_composer.compose_v2b_payload(
            self.model.current_time
        )
        self._v2b_payload.source = self.unique_id
        self._v2b_payload = self._data_simplifier.simplify_data(self._v2b_payload)

        self._v2r_payload = self._data_composer.compose_v2r_payload(
            self.model.current_time
        )
        self._v2r_payload.source = self.unique_id
        self._v2r_payload = self._data_simplifier.simplify_data(self._v2r_payload)

        self._v2v_payload = self._data_composer.compose_v2v_payload(
            self.model.current_time
        )

        self._data_composer.previous_time = self.model.current_time

        self._total_data_generated = (
            self._v2b_payload.total_data_size
            + self._v2v_payload.total_data_size
            + self._v2r_payload.total_data_size
        )

    def downlink_stage(self) -> None:
        """
        Downlink stage for the vehicle.
        """
        logger.debug(
            f"Downlink stage for vehicle {self.unique_id} at time"
            f" {self.model.current_time}"
        )

        self._vehicles_in_range = len(self._received_v2v_data)
        self._data_collector.collect_data(self._received_v2v_data)
