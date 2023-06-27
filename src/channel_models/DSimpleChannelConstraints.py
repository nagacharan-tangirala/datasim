from src.channel_models.BChannelConstraints import ChannelConstraintsBase


class SimpleChannelConstraints(ChannelConstraintsBase):
    def __init__(self, model_data: dict):
        """
        Initialize the simple channel constraints.
        """
        super().__init__()

        self._bandwidth: float = float(model_data['bandwidth'])
