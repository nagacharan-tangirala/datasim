import logging

import models.model_factory as model_factory
from core.constants import MainKey, ModelName, ModelType
from device.activation import ActivationSettings
from device.payload import RSUPayload, RSUResponse, VehiclePayload
from mesa import Agent
from numpy import ndarray

from src.device.hardware import ComputingHardware, NetworkHardware

logger = logging.getLogger(__name__)


class RoadsideUnit(Agent):
    def __init__(
        self,
        rsu_id: int,
        hardware_settings: ComputingHardware,
        network_settings: NetworkHardware,
        activation_settings: ActivationSettings,
        rsu_models: dict,
    ):
        """
        Initialize the rsu.
        """
        super().__init__(rsu_id, None)
        self.model = None

        self._r2b_payload: RSUPayload | None = None
        self._r2r_payload: RSUPayload | None = None

        self._v2b_response: RSUResponse | None = None
        self._v2r_response: RSUResponse | None = None

        self._received_v2r_data: dict[int, VehiclePayload] = {}
        self._received_r2r_data: dict[int, RSUPayload] = {}

        self._hardware_settings: ComputingHardware = hardware_settings
        self._network_settings: NetworkHardware = network_settings
        self._activation_settings: ActivationSettings = activation_settings

        self._location: list[float] = []
        self._total_data_generated: float = 0

        self._create_models(rsu_models)

    @property
    def location(self) -> list[float]:
        """Get the location of the base station."""
        return self._location

    @property
    def r2b_payload(self) -> RSUPayload | None:
        """Get the payload from the vehicle to the base station."""
        return self._r2b_payload

    @property
    def r2r_payload(self) -> RSUPayload | None:
        """Get the payload from the vehicle to the base station."""
        return self._r2r_payload

    def get_activation_times(self) -> ndarray[int]:
        """
        Get the activation times of the roadside unit.
        """
        return self._activation_settings.enable_times

    def get_deactivation_times(self) -> ndarray[int]:
        """
        Get the deactivation times of the roadside unit.
        """
        return self._activation_settings.disable_times

    def _create_models(self, model_data: dict) -> None:
        """
        Create the models for the rsu.

        Parameters
        ----------
        model_data : dict
            The model data of the rsu.
        """
        self._mobility_model = model_factory.create_mobility_model(
            model_data[ModelName.MOBILITY],
        )

        self._data_composer = model_factory.create_rsu_data_composer(
            model_data[ModelName.DATA_COMPOSER]
        )

        self._data_simplifier = model_factory.create_rsu_data_simplifier(
            model_data[ModelName.DATA_SIMPLIFIER]
        )

        self._data_collector = model_factory.create_rsu_data_collector(
            model_data[ModelName.DATA_COLLECTOR]
        )

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

    def activate_roadside_unit(self, time_step: int) -> None:
        """
        Activate the roadside unit.
        """
        # Set previous time for data composer
        self._data_composer.previous_time = time_step

        # Get the current location of the vehicle
        self._mobility_model.current_time = self.model.current_time
        self._mobility_model.step()
        self._location = self._mobility_model.current_location

        self.model.space.place_agent(self, self._location)

    def deactivate_roadside_unit(self, time_step: int) -> None:
        """
        Deactivate the roadside unit.
        """
        pass

    def use_network_for_v2r_payload(self) -> None:
        """
        Use the network for a payload from a vehicle to a roadside unit.
        """
        # Calculate the total data size
        total_data_size = 0
        for payload in self._received_v2r_data.values():
            total_data_size += payload.total_data_size
        self._network_settings.consume_capacity(total_data_size)

    def use_network_for_r2b_payload(self) -> None:
        """
        Use the network for a payload from a roadside unit to the base station.
        """
        self._network_settings.consume_capacity(self._r2b_payload.total_data_size)

    def use_network_for_r2r_payload(self) -> None:
        """
        Use the network for a payload from a roadside unit to another roadside unit.
        """
        self._network_settings.consume_capacity(self._r2r_payload.total_data_size)

    def assign_v2r_data(self, payload: VehiclePayload) -> None:
        """
        Assign data from a vehicle.

        Parameters
        ----------
        payload : dict
            The payload of the vehicle.
        """
        self._received_v2r_data[payload.source] = payload

    def assign_r2r_data(self, payload: RSUPayload) -> None:
        """
        Assign r2r data from a roadside unit.

        Parameters
        ----------
        payload : dict
            The payload of the roadside unit.
        """
        self._received_r2r_data[payload.source] = payload

    def use_network_for_received_v2r(self) -> None:
        """
        Use the network for the received data from a vehicle.
        """
        # Calculate the total data size
        total_data_size = 0
        for payload in self._received_v2r_data.values():
            total_data_size += payload.total_data_size
        self._network_settings.consume_capacity(total_data_size)

    def uplink_stage(self) -> None:
        """
        The uplink stage of the roadside unit.
        """
        logger.debug(
            f"Uplink stage for RSU {self.unique_id} at time {self.model.current_time}"
        )

        # Propagate the mobility model and get the current location
        self._mobility_model.current_time = self.model.current_time
        self._mobility_model.step()

        if self._mobility_model.type != ModelType.STATIC:
            self._location = self._mobility_model.current_location
            self.model.space.move_agent(self, self._location)

        # Compose the payloads
        self._r2b_payload = self._data_composer.compose_r2b_payload(
            self.model.current_time
        )
        self._r2b_payload.source = self.unique_id
        self._r2b_payload = self._data_simplifier.simplify_data(self._r2b_payload)

        self._r2r_payload = self._data_composer.compose_r2r_payload(
            self.model.current_time
        )
        self._r2r_payload.source = self.unique_id
        self._r2r_payload = self._data_simplifier.simplify_data(self._r2r_payload)

        self._data_composer.previous_time = self.model.current_time

        self._total_data_generated = self._r2b_payload.total_data_size

    def downlink_stage(self) -> None:
        """
        The downlink stage of the roadside unit.
        """
        pass
