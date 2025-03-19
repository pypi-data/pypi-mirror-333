import pytest
from pathlib import Path
from ai_sandbox.security import safe_path_access, SecurityError  # type: ignore


def test_safe_path_access_valid():
    """Test that accessing a valid path works."""
    # Create a temporary test file
    test_file = Path("test_file.txt")
    test_file.touch()

    try:
        path = safe_path_access("test_file.txt")
        assert path == test_file.resolve()
    finally:
        # Clean up
        test_file.unlink()


def test_safe_path_access_subdir():
    """Test that accessing a file in a subdirectory works."""
    # Create a temporary subdirectory and file
    subdir = Path("test_subdir")
    subdir.mkdir(exist_ok=True)
    test_file = subdir / "test_file.txt"
    test_file.touch()

    try:
        path = safe_path_access("test_subdir/test_file.txt")
        assert path == test_file.resolve()
    finally:
        # Clean up
        test_file.unlink()
        subdir.rmdir()


def test_safe_path_access_parent_dir():
    """Test that accessing a file in a parent directory is blocked."""
    with pytest.raises(SecurityError):
        safe_path_access("../outside_file.txt")


def test_safe_path_access_absolute_path():
    """Test that accessing an absolute path outside current dir is blocked."""
    with pytest.raises(SecurityError):
        safe_path_access("/etc/passwd")
