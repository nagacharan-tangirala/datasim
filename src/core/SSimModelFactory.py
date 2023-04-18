from src.device.DUnitDiskCoverageModel import UnitDiskCoverageModel


class SimModelFactory:
    def __init__(self):
        """
        Initialize the simulation model factory.
        """
        pass

    @staticmethod
    def create_coverage_model(params: dict):
        """
        Create the coverage model.

        Parameters
        ----------
        params : dict
            Dictionary containing all the parameters for the coverage model.

        Returns
        ----------
        CoverageModel
            The coverage model.
        """
        # Get the coverage model type
        coverage_model_type = params.get('type', 'unit_disk')

        # Create the coverage model
        if coverage_model_type == 'unit_disk':
            return UnitDiskCoverageModel(params)
        else:
            raise ValueError('Invalid coverage model type')
