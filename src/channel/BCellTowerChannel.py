from mesa import Agent


class BaseCellTowerChannel(Agent):
    def __init__(self, channel_id: int):
        super().__init__(channel_id, None)
