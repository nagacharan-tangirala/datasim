from src.coverage.BCoverageModel import CoverageModel
from src.coverage.KDTree import KDTree
from src.device.BEntity import EntityBase
from src.nodes.BNode import NodeBase


class UnitDiskCoverageModel(CoverageModel):
    def __init__(self, params: dict):
        """
        Initialize the unit disk coverage model.
        """
        super().__init__()
        self.radius = params.get('radius', 100.0)

    def update_coverage(self, entities: list[EntityBase], nodes: list[NodeBase], ts: int):
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
        # Get entity positions and create a KDTree
        entity_positions = {}
        for entity in entities:
            entity_positions[entity.get_id()] = entity.get_location()

        entity_kd_tree = KDTree(entity_positions)

        # Get the neighbours of entities
        for entity in entities:
            entity.set_neighbours(entity_kd_tree.get_neighbours(entity.get_location(), self.radius))
