from src.device.payload import BaseStationPayload


class ControllerCollector:
    def __init__(self):
        """
        Initialize the data collector.
        """
        pass

    def collect_data(self, incoming_data: dict[int, BaseStationPayload]):
        """
        Collect the data from the controller.
        """
        # Collect the statistics of the incoming data
        pass
