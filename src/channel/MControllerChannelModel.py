from mesa import Model

from src.device.BCellTower import BaseCellTower


class ControllerChannelModel(Model):
    def __init__(self, nodes: dict[int, BaseCellTower]):
        """
        Initialize the controller channel model.
        """
        super().__init__()

        self.nodes = nodes

    def add_channel(self, channel):
        """
        Add the channel to the model.
        """
        self.schedule.add(channel)
