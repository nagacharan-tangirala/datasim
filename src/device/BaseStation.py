from mesa import Agent

from src.application.Payload import VehiclePayload, BaseStationPayload, BaseStationResponse, VehicleResponse
from src.device.ActivationSettings import ActivationSettings
from src.device.ComputingHardware import ComputingHardware
from src.device.NetworkHardware import NetworkHardware
from src.models.ModelFactory import ModelFactory


class BaseStation(Agent):
    def __init__(self,
                 base_station_id,
                 base_station_position: list[float],
                 computing_hardware: ComputingHardware,
                 wireless_hardware: NetworkHardware,
                 wired_hardware: NetworkHardware,
                 activation_settings: ActivationSettings,
                 base_station_models_data: dict):
        """
        Initialize the base station.

        Parameters
        ----------
        base_station_id : int
            The id of the base station.
        base_station_position : list[float]
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

        self._location: list[float] = []
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
        base_station_models_data['mobility_model']['position'] = base_station_position
        self._create_models(base_station_models_data)

    @property
    def location(self) -> list[float, float]:
        """ Get the location of the base station. """
        return self._location

    @property
    def uplink_payload(self) -> BaseStationPayload:
        """ Get the uplink payload. """
        return self._uplink_payload

    @property
    def downlink_response(self) -> BaseStationResponse:
        """ Get the downlink response. """
        return self._downlink_response

    @downlink_response.setter
    def downlink_response(self, response: BaseStationResponse) -> None:
        """ Set the downlink response. """
        self._downlink_response = response

    @property
    def downlink_vehicle_data(self) -> dict[int, VehicleResponse]:
        """ Get the downlink vehicle data. """
        return self._downlink_vehicle_data

    def set_uplink_vehicle_data(self, incoming_data: dict[int, VehiclePayload]) -> None:
        """
        Set the incoming data for the base station.
        """
        self._uplink_vehicle_data = incoming_data

    def _create_models(self, base_station_models_data: dict) -> None:
        """
        Create the models for the base station.
        """
        model_factory = ModelFactory()
        self._mobility_model = model_factory.create_mobility_model(base_station_models_data['mobility_model'])
        self._base_station_data_processor = model_factory.create_base_station_data_processor(
            base_station_models_data['data_processor_model'])
        self.base_station_app_runner = model_factory.create_basestation_app_runner(self.unique_id,
                                                                                   self._computing_hardware)

    def use_wired_for_uplink(self) -> None:
        """
        Use the network hardware to transfer data in the uplink direction.
        """
        self._wired_hardware.consume_capacity(sum(self._uplink_payload.uplink_data))

    def use_wired_for_downlink(self) -> None:
        """
        Use the network hardware to transfer data in the downlink direction.
        """
        self._wired_hardware.consume_capacity(sum(self._downlink_response.downlink_data))

    def use_wireless_for_uplink(self) -> None:
        """
        Use the network hardware to transfer data in the uplink direction.
        """
        self._wireless_hardware.consume_capacity(sum(self._uplink_payload.uplink_data))

    def use_wireless_for_downlink(self) -> None:
        """
        Use the network hardware to transfer data in the downlink direction.
        """
        self._wireless_hardware.consume_capacity(sum(self._downlink_response.downlink_data))

    def uplink_stage(self) -> None:
        """
            Uplink stage of the base station. Create data to be sent to the central controller.
            This is the third step in the overall simulation.
            """
        self._mobility_model.current_time = self.sim_model.current_time
        self._mobility_model.step()
        self._location = self._mobility_model.current_location

        # Create base station payload.
        self._uplink_payload = self.base_station_app_runner.generate_basestation_payload(self.sim_model.current_time,
                                                                                         self._uplink_vehicle_data)

        # Use the data processor to process the data.
        self._uplink_payload = self._base_station_data_processor.simplify_base_station_data(self._uplink_payload)

    def downlink_stage(self) -> None:
        """
        Downlink stage of the base station.
        """
        # Use the base station app runner to process the data.
        self.base_station_app_runner.process_result(self._downlink_response)

        # Create the downlink vehicle response.
        for vehicle_id in self._downlink_response.destination_vehicles:
            # Create the downlink vehicle response.
            self._downlink_vehicle_data[vehicle_id] = VehicleResponse(destination=vehicle_id,
                                                                      status=True,
                                                                      timestamp=self.sim_model.current_time,
                                                                      downlink_data=
                                                                      self._downlink_response.downlink_data[vehicle_id])
