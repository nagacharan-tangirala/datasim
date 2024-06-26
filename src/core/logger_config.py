import logging.config
from datetime import datetime


class LoggerConfig:
    def __init__(self, log_file: str, log_level: str, log_overwrite: bool = False):
        """
        Initialize the logger configuration.

        Parameters
        ----------
        log_file : str
            The log file.
        """
        self._log_file = log_file
        self._log_level = log_level
        self._log_overwrite = log_overwrite

    def setup_logger_config(self) -> None:
        """
        Configure the logger.
        """
        # Check if the log file already exists
        if self._log_file and not self._log_overwrite:
            self._log_file = self._log_file.replace(
                ".log", "_%s.log" % datetime.now().strftime("%Y%m%d_%H%M%S")
            )

        with open(self._log_file, "w") as f:
            f.write("")

        simple_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {
                    "format": "%(asctime)s - %(name)20s - %(levelname)6s - %(message)s"
                },
            },
            "handlers": {
                "stderr": {
                    "class": "logging.StreamHandler",
                    "level": "ERROR",
                    "formatter": "simple",
                    "stream": "ext://sys.stderr",
                },
                "local_file_handler": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": self._log_level,
                    "formatter": "simple",
                    "filename": self._log_file,
                },
            },
            "root": {"level": self._log_level, "handlers": ["local_file_handler"]},
        }

        logging.config.dictConfig(simple_config)
