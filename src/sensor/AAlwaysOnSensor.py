from mesa import Model

from src.sensor.ASensor import SensorBase


class AlwaysOnSensor(SensorBase):
    def activate(self):
        pass

    def __init__(self, params: dict, sensor_model: Model, time_step: int):
        """
        Initialize the sensor.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the sensor.
        sensor_model : Model
            The sensor model.
        """
        super().__init__(params, sensor_model, time_step)
        self.is_active = True

    def step(self):
        # Check if the model is active
        if not self.active:
            return

        # Get the size of the data collected by the sensors
        collected_data = 0
        for sensor in self.sensors.values():
            collected_data += sensor.collect_data(self.model.current_time)

        # Update the data collected by the sensors
        self.total_data = collected_data

    def _update_sensor_status(self, sim_time: int):
        """
        Activate the sensor. This method is called by the entity when the start time of the sensor is reached.
        For the AlwaysActiveSensor, this method does not change the status of the sensor.
        """
        self.is_active = True
