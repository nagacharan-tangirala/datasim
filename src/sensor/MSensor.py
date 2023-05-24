from mesa import Model
from mesa.time import BaseScheduler

from src.sensor.ASensor import SensorBase
from src.sensor.SSensorFactory import SensorFactory


class SensorModel(Model):
    def __init__(self, sensor_params: dict, time_step: int):
        """
        Initialize the sensor model.
        """
        super().__init__()

        self.sensor_params = sensor_params

        # Create a dictionary to store the sensors
        self.sensors: dict[int, SensorBase] = {}

        # Create a sensor factory to create the sensors when the model is activated
        self.sensor_factory = SensorFactory()

        self.time_step = time_step

    def step(self):
        """
        Step function for the model.
        """
        self.schedule.step()

    def get_collected_data_size(self) -> float:
        """
        Get the total data collected by the sensors.
        """
        # Iterate over all the sensors and get the data collected by them
        total_data = 0.0
        for sensor in self.sensors.values():
            total_data += sensor.get_collected_data_size()

        return total_data

    def activate(self):
        """
        Get the start time of the model.
        """
        # Create the sensors
        for sensor_id, sensor_params in self.sensor_params.items():
            self.sensors[sensor_id] = self.sensor_factory.create_sensor(sensor_params, self, self.time_step)

        # Override the scheduler
        self.schedule = BaseScheduler(self)

        # Activate the sensors
        for sensor in self.sensors.values():
            sensor.activate()

    def deactivate(self):
        """
        Deactivate the model.
        """
        # Iterate over all the sensors and remove them from the scheduler to deactivate them
        for sensor in self.sensors.values():
            sensor.deactivate()
