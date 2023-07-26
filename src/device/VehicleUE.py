import logging

from mesa import Agent
from pandas import DataFrame

from src.application.ApplicationSettings import ApplicationSettings
from src.application.Payload import VehiclePayload, VehicleResponse
from src.core.Constants import *
from src.core.CustomExceptions import WrongActivationTimeError, WrongDeactivationTimeError
from src.device.ActivationSettings import ActivationSettings
from src.device.ComputingHardware import ComputingHardware
from src.device.NetworkHardware import NetworkHardware
from src.models.ModelFactory import ModelFactory

logger = logging.getLogger(__name__)


class VehicleUE(Agent):
    def __init__(self,
                 vehicle_id: int,
                 computing_hardware: ComputingHardware,
                 wireless_hardware: NetworkHardware,
                 activation_settings: ActivationSettings,
                 application_settings: list[ApplicationSettings],
                 vehicle_models: dict) -> None:
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
        application_settings : list[ApplicationSettings]
            The application settings of the vehicle.
        vehicle_models : dict
            The model data of the vehicle.
        """
        super().__init__(vehicle_id, None)

        self._location: list[float] = []
        self.sim_model = None

        self._uplink_payload: VehiclePayload | None = None
        self._downlink_response: VehicleResponse | None = None

        self._computing_hardware: ComputingHardware = computing_hardware
        self._networking_hardware: NetworkHardware = wireless_hardware
        self._activation_settings: ActivationSettings = activation_settings
        self._application_settings: list[ApplicationSettings] = application_settings

        self._create_models(vehicle_models)

    @property
    def start_time(self) -> int:
        """ Get the start time. """
        return self._activation_settings.start_time

    @property
    def end_time(self) -> int:
        """ Get the end time. """
        return self._activation_settings.end_time

    @property
    def uplink_payload(self) -> VehiclePayload:
        """ Get the uplink payload. """
        return self._uplink_payload

    @property
    def downlink_response(self) -> VehicleResponse:
        """ Get the downlink response. """
        return self._downlink_response

    @downlink_response.setter
    def downlink_response(self, response: VehicleResponse) -> None:
        """ Set the downlink response. """
        self._downlink_response = response

    @property
    def location(self) -> list[float, float]:
        """ Get the location of the vehicle. """
        return self._location

    def _create_models(self, model_data: dict) -> None:
        """
        Create the models for this vehicle.
        """
        logger.debug(f"Creating models for vehicle {self.unique_id}")
        model_factory = ModelFactory()
        self._mobility_model = model_factory.create_mobility_model(model_data[C_MOBILITY_MODEL])
        self._vehicle_data_processor = model_factory.create_vehicle_data_processor(model_data[C_DATA_PROCESSOR])
        self._vehicle_app_runner = model_factory.create_vehicle_app_runner(self.unique_id,
                                                                           self._application_settings,
                                                                           computing_hardware=self._computing_hardware)

    def update_mobility_data(self, mobility_data: DataFrame | list[float]) -> None:
        """
        Update the mobility data depending on the mobility model.

        Parameters
        ----------
        mobility_data : DataFrame | list[float]
            The mobility data to update.
        """
        match self._mobility_model.type:
            case 'static':
                logger.debug(f"Updating position for vehicle {self.unique_id}")
                self._mobility_model.update_position(mobility_data)
            case 'trace':
                logger.debug(f"Updating trace for vehicle {self.unique_id} with length {len(mobility_data)}")
                self._mobility_model.update_positions(mobility_data)

    def activate_vehicle(self, time_step: int) -> None:
        """
        Activate the vehicle if the time step is correct.
        """
        if time_step != self._activation_settings.start_time:
            raise WrongActivationTimeError(time_step, self._activation_settings.start_time)
        self._activation_settings.active = True

    def deactivate_vehicle(self, time_step: int) -> None:
        """
        Deactivate the vehicle if the time step is correct.
        """
        if time_step != self._activation_settings.end_time:
            raise WrongDeactivationTimeError(time_step, self._activation_settings.end_time)
        self._activation_settings.active = False

    def use_network_for_uplink(self) -> None:
        """
        Use the network hardware to transfer data in the uplink direction.
        """
        self._networking_hardware.consume_capacity(self._uplink_payload.uplink_data)

    def use_network_for_downlink(self) -> None:
        """
        Use the network hardware to transfer data in the downlink direction.
        """
        self._networking_hardware.consume_capacity(self._downlink_response.downlink_data)

    def uplink_stage(self) -> None:
        """
        Downlink stage for the vehicle.
        """
        logger.debug(f"Uplink stage for vehicle {self.unique_id} at time {self.sim_model.current_time}")
        # Propagate the mobility model and get the current location
        self._mobility_model.current_time = self.sim_model.current_time
        self._mobility_model.step()
        self._location = self._mobility_model.current_location
        logger.debug(f"Position updated: {self._location}")

        # Generate data from the applications
        self._uplink_payload = self._vehicle_app_runner.generate_vehicle_payload(self.sim_model.current_time)

        # Simplify the data using the data processor
        self._uplink_payload = self._vehicle_data_processor.simplify_vehicle_data(self._uplink_payload)

        logger.debug(f"Payload generated: {self._uplink_payload}")

    def downlink_stage(self) -> None:
        """
        Downlink stage for the vehicle.
        """
        logger.debug(f"Downlink stage for vehicle {self.unique_id} at time {self.sim_model.current_time}")
        # Process the data from the applications
        self._vehicle_app_runner.process_result(self._downlink_response)
        logger.debug(f"Response processed: {self._downlink_response}")
