from src.application.Payload import VehiclePayload


class VehicleDataProcessor:
    def __init__(self, model_data: dict):
        """
        Initialize the vehicle data processor.
        """
        self._compression_factor: float = float(model_data['data_compression_factor'])

    def simplify_vehicle_data(self, vehicle_data: VehiclePayload) -> VehiclePayload:
        """
        Simplify the vehicle data by applying the data processing techniques.

        Parameters
        ----------
        vehicle_data : dict[int, VehiclePayload]
            The vehicle data to simplify.

        Returns
        -------
        dict[int, VehiclePayload]
            The simplified vehicle data.
        """
        vehicle_data.uplink_data = vehicle_data.uplink_data * self._compression_factor
        # TODO: Add more data processing techniques here.

        return vehicle_data
