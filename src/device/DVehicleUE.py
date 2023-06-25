from pandas import DataFrame

from src.device.BUE import BaseUE
from src.models.MUEDataUnitModel import UEDataUnitModel
from src.models.MUEMobilityModel import UEMobilityModel


class VehicleUE(BaseUE):
    def __init__(self, ue_id: int, ue_models: dict):
        """
        Initialize the vehicle ue.
        """
        super().__init__(ue_id)

        # Create the models.
        self.model_data = ue_models
        self.neighbour_data: dict[int, float] = {}

        self._create_models()

    def _create_models(self) -> None:
        """
        Create the models for this ue.
        """
        self.mobility_model = UEMobilityModel(self.model_data['mobility'])
        self.data_unit_model = UEDataUnitModel(self.unique_id, self.model_data['data_unit'])

    def _activate_models(self) -> None:
        """
        Initiate the models related to this ue.
        """
        self.mobility_model.activate()
        self.data_unit_model.activate()

    def _deactivate_models(self) -> None:
        """
        Deactivate the models related to this ue.
        """
        self.mobility_model.deactivate()
        self.data_unit_model.deactivate()

    def get_generated_data(self) -> int:
        """
        Get the generated data.
        """
        return self.data_unit_model.get_generated_data()

    def get_cached_data(self) -> int:
        """
        Get the cached data.
        """
        return self.data_unit_model.get_cached_data()

    def get_start_and_end_time(self) -> tuple[int, int]:
        """
        Get the start and end time of the ue.
        """
        return self.start_time, self.end_time

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
        self.data_unit_model.step(self.sim_model.current_time)

        # Update the current position
        self.current_position = self.mobility_model.get_location()
