from abc import ABCMeta, abstractmethod


class NeighbourModelBase(metaclass=ABCMeta):
    """Base class for all neighbour models."""

    def __init__(self, params: dict):
        """
        Initialize the neighbour model with given parameters.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the neighbour model.
        """
        self.neighbour_model_id = params.get('id', None)
        self.entity_id = params.get('entity_id', None)

        self.start_time = params.get('start_time', None)
        self.end_time = params.get('end_time', None)

        self.last_update_time = 0
        self.data = None
        self.is_active = False

    @abstractmethod
    def _update_neighbour_status(self, sim_time: int):
        """
        Update the neighbour status.

        Parameters
        ----------
        sim_time : int
            Simulation time.
        """
        pass

    @abstractmethod
    def get_neighbours(self, sim_time: int):
        """
        Get the neighbours.

        Parameters
        ----------
        sim_time : int
            Simulation time.
        """
        pass

    def update(self, sim_time: int):
        """
        Update the neighbour model.

        Parameters
        ----------
        sim_time : int
            Simulation time.
        """
        self._update_neighbour_status(sim_time)

