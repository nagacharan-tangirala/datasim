import logging.config
from datetime import datetime
from pathlib import Path


class LoggerConfig:
    def __init__(self, log_file: Path, log_level: str, log_overwrite: bool = False):
        """
        Initialize the logger configuration.

        Parameters
        ----------
        log_file : Path
            The log file.
        log_level : str
            The log level.
        log_overwrite : bool
            Whether to overwrite the log file.
        """
        self._log_file: Path = log_file
        self._log_level: str = log_level
        self._log_overwrite: bool = log_overwrite

    def setup_logger_config(self) -> None:
        """
        Configure the logger.
        """
        # Check if the log file already exists
        if self._log_file and not self._log_overwrite:
            log_file_name = self._log_file.name
            log_file_name = log_file_name.replace(
                ".log", "_%s.log" % datetime.now().strftime("%Y%m%d_%H%M%S")
            )
            self._log_file = self._log_file.parent / log_file_name

        with self._log_file.open(mode="w") as f:
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
