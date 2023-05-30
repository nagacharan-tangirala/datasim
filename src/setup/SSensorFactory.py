from src.device.BSensor import SensorMode
from src.device.DRegularSensor import RegularSensor


class SensorFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_sensor(params: dict, sensor_model, time_step: int):
        """
        Create a sensor from the given parameters.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the sensor.
        sensor_model : Model
            The sensor model.
        time_step : int
            The time step of the simulation.
        """
        sensor_mode = params.get('mode', None)
        if sensor_mode == SensorMode.REGULAR:
            return RegularSensor(params, sensor_model, time_step)
        else:
            raise ValueError("Sensor mode not supported.")
