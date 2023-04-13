from scipy.spatial import kdtree


class KDTree:
    def __init__(self, entity_positions: dict):
        """
        Initialize the coverage index with the given positions.

        Parameters
        ----------
        entity_positions : dict
            Dictionary containing the entity ID as key and the position as value.
        """
        self.tree = kdtree.KDTree(list(entity_positions.values()))

        # Create a map from entity ID to position
        self.position_to_entity_id = {}
        for entity_id, position in entity_positions.items():
            self.position_to_entity_id[tuple(position)] = entity_id

    def get_neighbours(self, position, radius):
        """
        Get the neighbours of the given position within the given radius.

        Parameters
        ----------
        position : list
            The position.
        radius : float
            The radius.

        Returns
        ----------
        list
            List of neighbours.
        """
        # Get the neighbours
        neighbours = self.tree.query_ball_point(position, radius)

        # Get the entity IDs
        entity_ids = []
        for neighbour in neighbours:
            entity_ids.append(self.position_to_entity_id[tuple(self.tree.data[neighbour])])

        return entity_ids
