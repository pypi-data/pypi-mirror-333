import logging
import sys
import imghdr


def setup_logging(log_level: str = "INFO"):
    """Configures logging for the application."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stderr,  # Log to stderr to keep stdout clean for output
    )


def handle_error(message: str, error: Exception = None):
    """Handles errors, logs them, and exits."""
    logging.error(f"Handling error: {message}")  # Log the message
    if error:
        logging.exception(error)  # Log the exception if provided
    sys.exit(1)


def validate_image_file(file_path: str) -> bool:
    """
    Validates if the given file path is a valid image file.
    Uses imghdr to determine the image type without fully loading the image.
    """
    if imghdr.what(file_path) is None:
        return False
    return True
