from src.sensor.BSensor import SensorMode
from src.sensor.DRegularSensor import RegularSensor


class SensorFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_sensor(params: dict):
        """
        Create a sensor from the given parameters.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the sensor.
        """
        sensor_mode = params.get('sensor_mode', None)
        if sensor_mode == SensorMode.REGULAR:
            return RegularSensor(params)
        # elif sensor_mode == SensorMode.INTERMITTENT:
        # return CameraSensor(params)
        # elif sensor_mode == SensorMode.CUSTOM:
            # if 'custom_times' not in params:
            #     raise ValueError("Custom times are mandatory for a sensor set to custom mode.")
            # return CustomSensor(params)
        else:
            raise ValueError("Sensor mode not supported.")
