class NodeFactory:
    def __init__(self):
        self._node_types = {'test': TestNode}

    def create_node(self, node_type, params):
        if node_type in self._node_types:
            return self._node_types[node_type](params)
        else:
            raise ValueError("Node type not supported.")