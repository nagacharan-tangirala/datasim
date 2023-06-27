from mesa import Agent


class WiredChannelBase(Agent):
    def __init__(self):
        """
        Initialize the wired channel.
        """
        super().__init__(0, None)

        self._data_from_towers: dict = {}
        self._data_from_controller: dict = {}
