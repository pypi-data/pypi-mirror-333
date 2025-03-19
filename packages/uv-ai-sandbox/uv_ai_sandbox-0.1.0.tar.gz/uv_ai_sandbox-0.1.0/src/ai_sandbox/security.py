import os
from pathlib import Path
from pathvalidate import validate_filepath, Platform


class SecurityError(Exception):
    """Exception raised for security violations."""

    pass


def safe_path_access(path_str):
    """
    Validate that a path is within the current directory and safe to access.

    Args:
        path_str: String representation of the path to validate

    Returns:
        Path: A validated Path object

    Raises:
        SecurityError: If the path is outside allowed boundaries or invalid
    """
    # Get the absolute path of the current directory
    current_dir = Path.cwd().resolve()
    # Convert to Path object and resolve to absolute path
    path = Path(path_str).resolve()

    # Check if the path is within the current directory
    if not str(path).startswith(str(current_dir)):
        raise SecurityError(f"Access denied: {path} is outside the allowed directory")

    try:
        # Get the appropriate platform for validation
        platform = Platform.POSIX if os.name == "posix" else Platform.WINDOWS

        # Validate the path string for potential security issues
        validate_filepath(str(path), platform=platform)
        return path  # Return the validated Path object
    except Exception as e:
        raise SecurityError(f"Invalid path: {e}")
