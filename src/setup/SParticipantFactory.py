from src.setup.SEntityFactory import EntityFactory
from src.setup.SSensorFactory import SensorFactory
from src.setup.SNodeFactory import NodeFactory


class ParticipantFactory:
    def __init__(self):
        self._node_factory = NodeFactory()
        self._sensor_factory = SensorFactory()
        self._entity_factory = EntityFactory()

    def create_sensor(self, params):
        return self._sensor_factory.create_sensor(params)

    def create_node(self, node_type, params):
        return self._node_factory.create_node(node_type, params)

    def create_main(self, main_type, params):
        return self._main_factory.create_main(main_type, params)
