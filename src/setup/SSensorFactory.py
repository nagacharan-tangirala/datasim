from src.sensor.BSensor import SensorType
from src.sensor.DSimpleSensor import SimpleSensor


def create_sensor(sensor_type: SensorType, params: dict):
    if sensor_type == SensorType.SIMPLE:
        return SimpleSensor(params)
    # elif sensor_type == SensorType.INTERMITTENT:
        # return CameraSensor(params)
    else:
        raise ValueError("Sensor type not supported.")
