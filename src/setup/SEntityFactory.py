class EntityFactory:
    def __init__(self):
        self._entity_types = {'test': TestEntity}

    def create_entity(self, entity_type, params):
        if entity_type in self._entity_types:
            return self._entity_types[entity_type](params)
        else:
            raise ValueError("Entity type not supported.")
