import logging


def setup_logger(name: str) -> logging.Logger:
    """
    Sets up and returns a logger with a specified name.

    :param name: Name for the logger instance.
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():  # Avoid duplicate handlers if logger is used multiple times
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)  # Default to INFO level
    return logger