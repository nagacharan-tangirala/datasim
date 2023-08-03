from src.output.BOutput import OutputBase
from src.output.DOutputCSV import OutputCSV


class OutputFactory:
    def __init__(self):
        """
        Initialize the output factory.
        """
        pass

    @staticmethod
    def get_output_helper(params: dict) -> OutputBase:
        """
        Get the output object.

        Parameters
        ----------
        params : dict
            Dictionary containing the parameters for the output object.

        Returns
        ----------
        OutputBase
            The output object.
        """
        output_type = params.get("output_type")
        if output_type == "csv":
            return OutputCSV(params)
        # elif output_type == "sql":
        # return OutputSQL(params)
        else:
            return None
