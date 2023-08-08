import logging

from mesa import Agent
from numpy import ndarray
from pandas import Series

import src.core.constants as constants
from src.device.activation import ActivationSettings
from src.device.hardware import *
from src.device.payload import BaseStationPayload, BaseStationResponse
from src.models.model_factory import ModelFactory

logger = logging.getLogger(__name__)


class CentralController(Agent):
    def __init__(
        self,
        controller_id: int,
        controller_position: ndarray[float],
        computing_hardware: ComputingHardware,
        wireless_hardware: NetworkHardware,
        activation_settings: ActivationSettings,
        controller_models: dict,
    ):
        """
        Initialize the central controller.

        Parameters
        ----------
        controller_id : int
            The id of the controller.
        controller_models : dict
            The model data of the controller.
        controller_position : Series
            The position of the controller.
        computing_hardware : ComputingHardware
            The computing hardware of the controller.
        wireless_hardware : NetworkHardware
            The wireless hardware of the controller.
        activation_settings : ActivationSettings
            The activation settings of the controller.
        """
        super().__init__(controller_id, None)

        self.sim_model = None
        self._location: ndarray[float] = []

        self._computing_hardware: ComputingHardware = computing_hardware
        self._networking_hardware: NetworkHardware = wireless_hardware
        self._activation_settings: ActivationSettings = activation_settings

        self._received_data: dict[int, BaseStationPayload] = {}
        self._downlink_response: dict[int, BaseStationResponse] = {}

        self.processed_base_station_data: dict[int, BaseStationPayload] = {}

        controller_models[constants.MOBILITY][constants.POSITION] = controller_position
        self._create_models(controller_models)

    @property
    def location(self) -> list[float, float]:
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
    def received_data(self) -> dict[int, BaseStationPayload]:
        """Get the received data."""
        return self._received_data

    @received_data.setter
    def received_data(self, data: dict[int, BaseStationPayload]) -> None:
        """Set the received data."""
        self._received_data = data

    @property
    def downlink_response(self) -> dict[int, BaseStationResponse]:
        """Get the downlink response."""
        return self._downlink_response

    @property
    def total_data_received(self) -> float:
        """Get the total data received."""
        return self._controller_collector.total_data_size

    @property
    def visible_vehicles(self) -> list[int]:
        """Get the visible vehicles."""
        return self._controller_collector.all_vehicles

    @property
    def data_sizes_by_type(self) -> dict[str, float]:
        """Get the data types and sizes."""
        return self._controller_collector.data_sizes_by_type

    @property
    def data_counts_by_type(self) -> dict[str, int]:
        """Get the data types and count."""
        return self._controller_collector.data_counts_by_type

    def activate_controller(self, time_step: int) -> None:
        """
        Activate the controller.
        """
        pass

    def deactivate_controller(self, time_step: int) -> None:
        """
        Deactivate the controller.
        """
        pass

    def _create_models(self, controller_models: dict) -> None:
        """
        Create the models for the base station.
        """
        model_factory = ModelFactory()
        self._mobility_model = model_factory.create_mobility_model(
            controller_models[constants.MOBILITY]
        )

        self._controller_collector = model_factory.create_controller_collector(
            controller_models[constants.DATA_COLLECTOR]
        )

        self._data_composer = model_factory.create_controller_data_composer(
            controller_models[constants.DATA_COMPOSER]
        )

    def use_network_for_uplink(self) -> None:
        """
        Use the network hardware to transfer data in the uplink direction.
        """
        # self._networking_hardware.consume_capacity(sum(self.received_data.uplink_data))
        pass

    def use_network_for_downlink(self) -> None:
        """
        Use the network hardware to transfer data in the downlink direction.
        """
        # self._networking_hardware.consume_capacity(sum(self._downlink_response.downlink_data))
        pass

    def uplink_stage(self) -> None:
        """
        Step through the central controller for the uplink stage.
        """
        logger.debug(
            f"Uplink stage for controller {self.unique_id} at time {self.sim_model.current_time}."
        )
        self._mobility_model.current_time = self.sim_model.current_time
        self._mobility_model.step()
        self._location = self._mobility_model.current_location

        self._controller_collector.collect_data(self._received_data)

        # Create base station response.
        self._downlink_response = self._data_composer.generate_basestation_response(
            self.sim_model.current_time, self._received_data
        )

    def downlink_stage(self) -> None:
        """
        Step through the central controller for the downlink stage.
        """
        logger.debug(
            f"Downlink stage for controller {self.unique_id} at time {self.sim_model.current_time}."
        )
        pass
