from collections import namedtuple

from pandas import DataFrame

from src.data.MUEDataHandlerModel import UEDataHandlerModel
from src.device.BUE import UEBase
from src.ue_models.MUEMobilityModel import UEMobilityModel


class VehicleUE(UEBase):
    def __init__(self, ue_id: int, ue_models: dict):
        """
        Initialize the vehicle ue.
        """
        super().__init__(ue_id)

        # Create the models.
        self.neighbour_data: dict[int, float] = {}

        self._create_models(ue_models)

    def _create_models(self, model_data: dict) -> None:
        """
        Create the models for this ue.
        """
        self.mobility_model = UEMobilityModel(model_data['mobility'])
        self.data_handler_model = UEDataHandlerModel(self.unique_id, model_data['data_unit'])

    def _activate_models(self) -> None:
        """
        Initiate the models related to this ue.
        """
        self.mobility_model.activate()
        self.data_handler_model.activate()

    def _deactivate_models(self) -> None:
        """
        Deactivate the models related to this ue.
        """
        self.mobility_model.deactivate()
        self.data_handler_model.deactivate()

    def get_generated_data(self) -> namedtuple:
        """
        Get the generated data.
        """
        return self.data_handler_model.get_generated_data()

    def get_cached_data(self) -> namedtuple:
        """
        Get the cached data.
        """
        return self.data_handler_model.get_cached_data()

    def update_mobility_data(self, mobility_data: DataFrame) -> None:
        """
        Update the mobility data.
        """
        self.mobility_model.update_data(mobility_data)
        self.start_time, self.end_time = self.mobility_model.get_start_and_end_time()

    def step(self) -> None:
        """
        Step function for the ue.
        """
        # Check if the ue is active
        if not self.active:
            return

        # Step through the models
        self.mobility_model.step(self.sim_model.current_time)
        self.data_handler_model.step(self.sim_model.current_time)

        # Update the current position
        self.position = self.mobility_model.get_location()
