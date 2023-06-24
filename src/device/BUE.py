from abc import abstractmethod

from mesa import Agent


class BaseUE(Agent):
    def __init__(self, ue_id: int):
        """
        Initialize the ue.
        """
        super().__init__(ue_id, None)

        self.sim_model = None

        self.current_position: list[float] = []

        self.start_time: int = 0
        self.end_time: int = 0

        self.active: bool = False
        self.data_sent: bool = False

    @abstractmethod
    def step(self, *args, **kwargs) -> None:
        """
        Step function for the ue.
        """
        pass

    @abstractmethod
    def _activate_models(self) -> None:
        """
        Initiate the models related to this ue.
        """
        pass

    @abstractmethod
    def _deactivate_models(self) -> None:
        """
        Deactivate the models related to this ue.
        """
        pass

    def get_id(self) -> int:
        """
        Get the ue id.

        Returns
        -------
        int
            The ue id.
        """
        return self.unique_id

    def get_position(self) -> list[float]:
        """
        Get the current position of the ue.

        Returns
        -------
        list[float]
            The current position of the ue.
        """
        return self.current_position

    def is_active(self) -> bool:
        """
        Check if the ue is active.

        Returns
        -------
        bool
            True if the ue is active, False otherwise.
        """
        return self.active

    def toggle_status(self) -> None:
        """
        Toggle the active status of the ue.
        """
        # Toggle the status
        self.active = not self.active

        if self.active:
            # Initiate the models
            self._activate_models()
        else:
            # Deactivate the models
            self._deactivate_models()

    def get_start_and_end_time(self) -> tuple[int, int]:
        """
        Get the start and end time of the ue.

        Returns
        -------
        tuple[int, int]
            The start and end time of the ue.
        """
        return self.start_time, self.end_time
