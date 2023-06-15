from src.channel.BCellTowerChannel import BaseCellTowerChannel


class InfiniteBandwidthCellTowerChannel(BaseCellTowerChannel):
    def __init__(self):
        """
        Initialize the infinite bandwidth node channel.
        """
        super().__init__()
