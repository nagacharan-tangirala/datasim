from src.sensor.BSensor import SensorBase, SensorType
from src.sensor.DSimpleSensor import BasicSensor


def create_sensor(sensor_type: SensorType, params: dict):
    if sensor_type == SensorType.BASIC:
        return BasicSensor(params)
    # elif sensor_type == SensorType.INTERMITTENT:
        # return CameraSensor(params)
    else:
        raise ValueError("Sensor type not supported.")
