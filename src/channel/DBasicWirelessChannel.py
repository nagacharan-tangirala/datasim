from pandas import DataFrame

from src.channel.BWirelessChannel import WirelessChannelBase
from src.channel_models.BChannelConstraints import ChannelConstraintsBase
from src.channel_models.BDataReduction import DataReductionBase
from src.channel_models.DSimpleChannelConstraints import SimpleChannelConstraints
from src.channel_models.DSimpleDataReduction import SimpleDataReduction
from src.channel_models.MTowerLookupModel import TowerLookupModel
from src.core.CustomExceptions import ModelTypeNotImplementedError


class BasicWirelessChannel(WirelessChannelBase):
    def __init__(self, cell_towers: dict, ue_links_df: DataFrame, tower_links_df: DataFrame, model_data: dict):
        """
        Initialize the basic wireless channel.
        """
        super().__init__(cell_towers, ue_links_df, tower_links_df)

        self._tower_lookup_model: TowerLookupModel | None = None
        self._channel_constraints_model: ChannelConstraintsBase | None = None
        self._data_reduction_model: DataReductionBase | None = None

        self._create_models(model_data)

    def _create_models(self, model_data: dict):
        """
        Create the models
        """
        self._tower_lookup_model = TowerLookupModel(self._cell_towers, self._tower_links, model_data['tower_lookup'])
        self._channel_constraints_model = self._create_channel_constraints_model(model_data['constraints'])
        self._data_reduction_model = self._create_data_reduction_model(model_data['data_reduction'])

    @staticmethod
    def _create_channel_constraints_model(constraints: dict) -> ChannelConstraintsBase:
        """
        Create the channel constraints model.
        """
        match constraints['name']:
            case "simple":
                return SimpleChannelConstraints(constraints)
            case _:
                raise ModelTypeNotImplementedError('channel constraints', constraints['name'])

    @staticmethod
    def _create_data_reduction_model(data_reduction: dict) -> DataReductionBase:
        """
        Create the data reduction model.
        """
        match data_reduction['name']:
            case "simple":
                return SimpleDataReduction(data_reduction)
            case _:
                raise ModelTypeNotImplementedError('data reduction', data_reduction['name'])

    def step(self) -> None:
        """
        Step through the ue channel.
        """
        # Step through the models.
        self._tower_lookup_model.step(self.current_time)

        # Collect data from each ue
        self._collect_data_from_ues()

        # Apply data models to the data
        self._apply_data_models()

        # Send data to the respective cell towers
        self._send_data_to_cell_towers()

        # Receive data from cell towers
        self._receive_data_from_cell_towers()

        # Send data to the respective ues
        self._send_data_to_ues()

    def _collect_data_from_ues(self):
        """
        Send data from the ues to the towers.
        """
        self.data_from_ues.clear()
        for ue_id, ue in self._ues.items():
            self.data_from_ues[ue_id] = ue.get_generated_data()

    def _apply_data_models(self):
        """
        Apply the data models to the data.
        """
        self.processed_ue_data = self._data_reduction_model.simplify_ue_data(self.data_from_ues)

    def _send_data_to_cell_towers(self):
        """
        Find the towers for the ues.
        """
