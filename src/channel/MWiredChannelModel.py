from mesa import Model


class WiredChannelModel(Model):
    def __init__(self):
        """
        Initialize the wired channel model.
        """
        super().__init__()

        self._wired_channel: WiredChannelBase = WiredChannelBase()
        self.schedule: BaseScheduler = BaseScheduler(self)
        self.current_time = 0

        self._create_wired_channel()
