from mesa import Agent
from pandas import Series

from src.application.ApplicationSettings import ApplicationSettings
from src.application.Payload import BaseStationPayload, BaseStationResponse
from src.device.ActivationSettings import ActivationSettings
from src.device.ComputingHardware import ComputingHardware
from src.device.NetworkHardware import NetworkingHardware
from src.models.ModelFactory import ModelFactory


class CentralController(Agent):
    def __init__(self,
                 controller_id: int,
                 controller_models: dict,
                 controller_position: Series,
                 computing_hardware: ComputingHardware,
                 wireless_hardware: NetworkingHardware,
                 activation_settings: ActivationSettings,
                 application_settings: list[ApplicationSettings]):
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
        wireless_hardware : NetworkingHardware
            The wireless hardware of the controller.
        activation_settings : ActivationSettings
            The activation settings of the controller.
        application_settings : list[ApplicationSettings]
            The application settings of the controller.
        """
        super().__init__(controller_id, None)

        self.sim_model = None
        self._location: list[float] = []

        self._computing_hardware: ComputingHardware = computing_hardware
        self._networking_hardware: NetworkingHardware = wireless_hardware
        self._activation_settings: ActivationSettings = activation_settings
        self._application_settings: list[ApplicationSettings] = application_settings

        self._received_data: dict[int, BaseStationPayload] = {}
        self._downlink_response: dict[int, BaseStationResponse] = {}

        self.processed_base_station_data: dict[int, BaseStationPayload] = {}

        controller_models['mobility_model']['position'] = [controller_position['x'], controller_position['y']]
        self._create_models(controller_models)

    @property
    def location(self) -> list[float, float]:
        """ Get the location of the base station. """
        return self._location

    @property
    def received_data(self) -> dict[int, BaseStationPayload]:
        """ Get the received data. """
        return self._received_data

    @received_data.setter
    def received_data(self, data: dict[int, BaseStationPayload]) -> None:
        """ Set the received data. """
        self._received_data = data

    @property
    def downlink_response(self) -> dict[int, BaseStationResponse]:
        """ Get the downlink response. """
        return self._downlink_response

    def _create_models(self, controller_models: dict) -> None:
        """
        Create the models for the base station.
        """
        model_factory = ModelFactory()
        self._mobility_model = model_factory.create_mobility_model(controller_models['mobility_model'])
        self._controller_data_processor = model_factory.create_controller_data_processor(
            controller_models['data_processor_model'])
        self._controller_app_runner = model_factory.create_controller_app_runner(self.unique_id,
                                                                                 self._computing_hardware)

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
        self._mobility_model.current_time = self.sim_model.current_time
        self._mobility_model.step()
        self._location = self._mobility_model.current_location

        # Use the data processor to process the data.
        self.processed_base_station_data = self._controller_data_processor.simplify_controller_data(self._received_data)

        # Create base station response.
        self._downlink_response = self._controller_app_runner.generate_basestation_response(self.sim_model.current_time,
                                                                                            self.processed_base_station_data)

    def downlink_stage(self) -> None:
        """
        Step through the central controller for the downlink stage.
        """
        pass
