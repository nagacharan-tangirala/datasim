from src.device.DCentralTrafficController import CentralController


class ControllerFactory:
    def __init__(self):
        pass

    def create_controller(self, controller_id, position):
        """
        Create a controller from the given parameters.

        Parameters
        ----------
        controller_id : int
            The ID of the controller.
        position : list[float]
            The position of the controller.
        """
        return CentralController(controller_id, position)
