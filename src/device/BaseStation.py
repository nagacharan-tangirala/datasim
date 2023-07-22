from mesa import Agent
from pandas import Series

from src.application.ApplicationSettings import ApplicationSettings
from src.application.Payload import VehiclePayload, BaseStationPayload, BaseStationResponse, VehicleResponse
from src.device.ActivationSettings import ActivationSettings
from src.device.ComputingHardware import ComputingHardware
from src.device.NetworkHardware import NetworkingHardware
from src.models.ModelFactory import ModelFactory


class BaseStation(Agent):
    def __init__(self,
                 cell_tower_id,
                 cell_tower_position: Series,
                 computing_hardware: ComputingHardware,
                 wireless_hardware: NetworkingHardware,
                 wired_hardware: NetworkingHardware,
                 activation_settings: ActivationSettings,
                 application_settings: list[ApplicationSettings],
                 cell_tower_models_data: dict):
        """
        Initialize the base station.

        Parameters
        ----------
        cell_tower_id : int
            The id of the cell tower.
        cell_tower_position : Series
            The position of the cell tower.
        computing_hardware : ComputingHardware
            The computing hardware of the cell tower.
        wireless_hardware : NetworkingHardware
            The wireless hardware of the cell tower.
        wired_hardware : NetworkingHardware
            The wired hardware of the cell tower.
        activation_settings : ActivationSettings
            The activation settings of the cell tower.
        application_settings : list[ApplicationSettings]
            The application settings of the cell tower.
        cell_tower_models_data : dict
            The model data of the cell tower.
        """
        super().__init__(cell_tower_id, None)

        self._location: list[float] = []
        self.sim_model = None

        self._wired_hardware: NetworkingHardware = wired_hardware
        self._computing_hardware: ComputingHardware = computing_hardware
        self._wireless_hardware: NetworkingHardware = wireless_hardware
        self._activation_settings: ActivationSettings = activation_settings
        self._application_settings: list[ApplicationSettings] = application_settings

        # Incoming vehicle data from the vehicles, set by the edge orchestrator
        self._uplink_vehicle_data: dict[int, VehiclePayload] = {}

        # Uplink payload generated at the base station after receiving the vehicle data
        self._uplink_payload: BaseStationPayload | None = None

        # Downlink response received from the controllers
        self._downlink_response: BaseStationResponse | None = None

        # Downlink responses generated at the base station after receiving the controller response
        self._downlink_vehicle_data: dict[int, VehicleResponse] = {}

        # Add the position to the base station models data
        cell_tower_models_data['mobility_model']['position'] = [cell_tower_position['x'], cell_tower_position['y']]
        self._create_models(cell_tower_models_data)

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

    def _create_models(self, cell_tower_models_data: dict) -> None:
        """
        Create the models for the base station.
        """
        model_factory = ModelFactory()
        self._mobility_model = model_factory.create_mobility_model(cell_tower_models_data['mobility_model'])
        self._base_station_data_processor = model_factory.create_base_station_data_processor(
            cell_tower_models_data['data_processor_model'])
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
