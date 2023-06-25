from mesa import Model
from mesa.time import BaseScheduler

from src.core.CustomExceptions import DuplicateDeviceFoundError
from src.device.BController import BaseController


class ControllerModel(Model):
    def __init__(self, controllers: dict[int, BaseController]):
        """
        Initialize the controller model.
        """
        super().__init__()

        self.controllers = controllers

        self.schedule: BaseScheduler = BaseScheduler(self)
        self._add_controllers_to_scheduler()

    def _create_cell_tower_controller_links(self):
        """
        Create the links between the cell towers and controllers.
        """
        pass

    def _add_controllers_to_scheduler(self) -> None:
        """
        Add the controllers to the scheduler.
        """
        for controller in self.controllers.values():
            self.schedule.add(controller)

    def step(self) -> None:
        """
        Step function for the model. This function is called every time step.
        """
        # Step the scheduler
        self.schedule.step()

    def _initiate_models(self):
        """
        Initiate the controllers and add them to the scheduler.
        """
        for controller_id, controller in self.controllers.items():
            self.schedule.add(controller)

    def update_controllers(self, new_controllers):
        """
        Update the controllers.
        """
        for controller_id, controller in new_controllers:
            if controller_id in self.controllers:
                raise DuplicateDeviceFoundError(controller_id, 'controller')
            self.controllers[controller_id] = controller
