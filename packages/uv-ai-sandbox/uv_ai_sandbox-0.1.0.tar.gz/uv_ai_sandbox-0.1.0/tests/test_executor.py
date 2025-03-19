from ai_sandbox.executor import execute_ai_code  # type: ignore


def test_execute_ai_code_basic():
    """Test basic code execution with a simple calculation."""
    code = """
result = 2 + 2
"""
    output = execute_ai_code(code)
    assert output == 2 + 2


def test_execute_ai_code_with_inputs():
    """Test code execution with provided inputs."""
    code = """
result = a + b
"""
    output = execute_ai_code(code, {"a": 5, "b": 7})
    assert output == 12


def test_execute_ai_code_with_function():
    """Test executing code that defines and uses a function."""
    code = """
def multiply(x, y):
    return x * y
    
result = multiply(6, 7)
"""
    output = execute_ai_code(code)
    assert output == 42


def test_restricted_imports():
    """Test that dangerous imports are restricted."""
    code = """
try:
    import os
    result = "Import allowed"
except ImportError:
    result = "Import restricted"
"""
    output = execute_ai_code(code)
    assert output == "Import restricted"


def test_restricted_file_access():
    """Test that file operations are restricted."""
    code = """
try:
    with open('/etc/passwd', 'r') as f:
        result = "File access allowed"
except:
    result = "File access restricted"
"""
    output = execute_ai_code(code)
    assert output == "File access restricted"


def test_result_dictionary():
    """Test that we can return a dictionary."""
    code = """
result = {"key1": "value1", "key2": 42}
"""
    output = execute_ai_code(code)
    assert output == {"key1": "value1", "key2": 42}
