from abc import ABCMeta, abstractmethod


class CoverageModel(metaclass=ABCMeta):
    def __init__(self):
        """
        Initialize the coverage model to update the nodes and entities that are in each other's coverage.
        """
        pass

    @abstractmethod
    def update_coverage(self, entities: list, nodes: list, ts: int):
        """
        Update the coverage of the nodes and entities.

        Parameters
        ----------
        nodes : list
            List of nodes.
        entities : list
            List of entities.
        ts : int
            The current time step.
        """
        pass
