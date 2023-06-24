from random import choices

from pandas import DataFrame, Series

from src.core.CustomExceptions import NotSupportedCellTowerError
from src.device.DBasicCellTower import BasicCellTower
from src.device.DCentralController import CentralController
from src.device.DIntermediateCellTower import IntermediateCellTower
from src.device.DVehicleUE import VehicleUE


class DeviceFactory:
    def __init__(self):
        """
        Initialize the device factory object.
        """
        # Create the dictionaries to store the devices in the simulation
        self.cell_towers = {}
        self.ues = {}
        self.controllers = {}

    def get_cell_towers(self) -> dict:
        """
        Get the cell towers in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the cell_tower.
        """
        return self.cell_towers

    def get_controllers(self) -> dict:
        """
        Get the controllers in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the controllers.
        """
        return self.controllers

    def get_ues(self) -> dict:
        """
        Get the ues in the simulation.

        Returns
        ----------
        dict
            Dictionary containing the ues.
        """
        return self.ues

    def create_cell_towers(self, cell_tower_data: DataFrame, cell_tower_models_data: dict, cell_tower_links_data: DataFrame) -> None:
        """
        Create the cell towers in the simulation.
        """
        # Get the list of cell towers in the simulation.
        cell_tower_list = cell_tower_data['cell_tower_id'].unique()

        for cell_tower_id in cell_tower_list:
            # Get the cell tower data.
            cell_tower_data: Series = cell_tower_data[cell_tower_data['cell_tower_id'] == cell_tower_id].iloc[0]

            # Create the cell tower.
            self.cell_towers[cell_tower_id] = self._create_cell_tower(cell_tower_id, cell_tower_data, cell_tower_models_data, cell_tower_links_data)

    @staticmethod
    def _create_cell_tower(cell_tower_id: int, cell_tower_data: Series, cell_tower_models_data: dict, cell_tower_links_data: DataFrame):
        """
        Create a cell tower from the given parameters.
        """
        cell_tower_type = cell_tower_data['type']
        if cell_tower_type == 'bs':
            return BasicCellTower(cell_tower_id, cell_tower_data, cell_tower_models_data, cell_tower_links_data)
        elif cell_tower_type == 'intermediate':
            return IntermediateCellTower(cell_tower_id, cell_tower_data, cell_tower_models_data, cell_tower_links_data)
        else:
            raise NotSupportedCellTowerError(cell_tower_type)

    def create_controllers(self, controller_data: DataFrame, controller_models_data: dict, controller_links_data: DataFrame) -> None:
        """
        Create the controllers in the simulation.
        """
        # Get the list of controllers in the simulation.
        controller_list = controller_data['controller_id'].unique()

        # Create the controllers.
        for controller_id in controller_list:
            # Get the controller position.
            controller_position: list[float, float] = controller_data[controller_data['controller_id'] == controller_id][['x', 'y']].values.tolist()

            # Create the controller.
            self.controllers[controller_id] = self._create_controller(controller_id, controller_position, controller_models_data, controller_links_data)

    @staticmethod
    def _create_controller(controller_id, position, controller_models_data, controller_links_data) -> CentralController:
        """
        Create a controller from the given parameters.

        Parameters
        ----------
        controller_id : int
            The ID of the controller.
        position : list[float]
            The position of the controller.
        """
        return CentralController(controller_id, position, controller_models_data, controller_links_data)

    def create_ues(self, ue_trace_data: DataFrame, ue_models: dict, ue_links_df: DataFrame) -> None:
        """
        Create the ues in the simulation.
        """
        # Get the list of ues in the simulation.
        ue_list = ue_trace_data['vehicle_id'].unique()

        # Get the weights of the ue types.
        ue_weights = [float(ue_data['weight']) for ue_data in ue_models.values()]
        ue_types = list(ue_models.keys())

        # Create the ues.
        for ue_id in ue_list:
            # Randomly select the type of the ue and get the respective model set.
            ue_type_choice = choices(ue_types, weights=ue_weights, k=1)[0]
            selected_ue_model_set = ue_models[ue_type_choice].copy()

            # Create the ue.
            self.ues[ue_id] = self._create_ue(ue_id, selected_ue_model_set, ue_links_df)

    @staticmethod
    def _create_ue(ue_id: int, ue_models: dict, ue_links_df: DataFrame) -> VehicleUE:
        """
        Create an ue from the given parameters.

        Parameters
        ----------
        ue_id : int
            The ID of the ue.
        """
        return VehicleUE(ue_id, ue_models, ue_links_df)
