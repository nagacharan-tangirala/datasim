from mesa import Model
from mesa.time import BaseScheduler
from pandas import DataFrame

from src.channel_models.BTowerLookup import TowerLookupBase
from src.channel_models.DNearestTowerLookup import NearestTowerLookup
from src.core.CustomExceptions import ModelTypeNotImplementedError


class TowerLookupModel(Model):
    def __init__(self, cell_towers: dict, tower_links_df: DataFrame, model_data: dict):
        """
        Initialize the tower look up model.
        """
        super().__init__()

        self._tower_lookup: TowerLookupBase = self._create_tower_lookup(cell_towers, tower_links_df, model_data)
        self.schedule: BaseScheduler = BaseScheduler(self)
        self._current_time: int = -1

    @property
    def current_time(self) -> int:
        """ Get the current time."""
        return self._current_time

    @staticmethod
    def _create_tower_lookup(cell_towers: dict, tower_links_df: DataFrame, model_data: dict) -> TowerLookupBase:
        """
        Create the tower lookup.
        """
        match model_data['name']:
            case 'nearest':
                return NearestTowerLookup(cell_towers, tower_links_df)
            case _:
                raise ModelTypeNotImplementedError('tower_lookup', model_data['name'])

    def step(self, *args, **kwargs) -> None:
        """
        Step through the tower look up model.
        """
        # Get the current time
        self._tower_lookup.current_time = int(args[0])
        self.schedule.step()

    def select_tower_for_ue(self, ue_id: int) -> int:
        """
        Select towers for the ue.
        """
        return self._tower_lookup.select_tower_for_ue(ue_id)
