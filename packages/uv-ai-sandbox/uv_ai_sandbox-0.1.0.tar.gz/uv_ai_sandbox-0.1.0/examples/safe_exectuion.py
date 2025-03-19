from ai_sandbox.security import safe_path_access, SecurityError  # type: ignore
from ai_sandbox.executor import execute_ai_code  # type: ignore

# Example of safely accessing files
try:
    # This will work if the file exists and is in the current directory
    file_path = safe_path_access("examples/data.txt")
    print(f"Safe path: {file_path}")

    # This would fail because it tries to access parent directory
    # file_path = safe_path_access("../outside_folder/unsafe.txt")
except SecurityError as e:
    print(f"Security error: {e}")

# Example of safely executing AI code
ai_code = """
def analyze(x):
    return x * 2

result = analyze(input_value)
"""

result = execute_ai_code(ai_code, {"input_value": 21})
print(f"AI execution result: {result}")
