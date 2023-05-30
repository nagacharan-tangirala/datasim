from src.device.DCentralTrafficController import CentralController


class ControllerFactory:
    def __init__(self):
        pass

    def create_controller(self, params: dict, nodes: dict):
        """
        Create a controller from the given parameters.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the controller.
        """
        controller_type = params.get('type', None)
        if controller_type == 'central':
            return CentralController(params, nodes)
        else:
            raise ValueError("Controller type not supported.")
