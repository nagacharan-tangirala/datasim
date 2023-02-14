from src.sensor.BSensor import SensorMode
from src.sensor.DRegularSensor import RegularSensor


class SensorFactory:
    def __init__(self):
        pass

    def create_sensor(params: dict):
        sensor_mode = params.get('sensor_mode', None)
        if sensor_mode == SensorMode.REGULAR:
            return RegularSensor(params)
        # elif sensor_mode == SensorMode.INTERMITTENT:
        # return CameraSensor(params)
        elif sensor_mode == SensorMode.CUSTOM:
            if params.get('custom_ti')
        else:
            raise ValueError("Sensor mode not supported.")
