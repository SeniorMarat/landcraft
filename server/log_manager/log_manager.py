import logging
from logging.handlers import RotatingFileHandler

class LogManager:
    """
    A class for managing centralized logging configurations.
    """

    @staticmethod
    def get_logger(name="app_logger", log_file="app.log", level=logging.INFO):
        """
        Creates and configures a logger instance.
        
        Args:
            name (str): Name of the logger.
            log_file (str): File to log messages to.
            level (int): Logging level (e.g., logging.INFO, logging.DEBUG).
        
        Returns:
            logging.Logger: Configured logger instance.
        """
        # Create a logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Prevent adding duplicate handlers
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(console_formatter)

            # File handler with rotation
            file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)

            # Add handlers to the logger
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)

        return logger

