#!/usr/bin/env python3
"""
Test script to verify that the ai-sandbox package is installed and working correctly.
"""

from ai_sandbox import execute_ai_code, safe_path_access, SecurityError

def test_execute_ai_code():
    """Test the execute_ai_code function"""
    code = """
def add(a, b):
    return a + b

result = add(a, b)
"""
    result = execute_ai_code(code, {"a": 5, "b": 7})
    print(f"Result of execute_ai_code: {result}")
    assert result == 12

def test_safe_path_access():
    """Test the safe_path_access function"""
    try:
        # This should work (accessing a file within the project directory)
        path = safe_path_access("README.md")
        print(f"Safe path access successful: {path}")
    except SecurityError as e:
        print(f"Unexpected error: {e}")
        
    try:
        # This should fail (attempting to access a file outside the project directory)
        path = safe_path_access("/etc/passwd")
        print(f"Unexpected success: {path}")
    except SecurityError as e:
        print(f"Expected security error: {e}")

if __name__ == "__main__":
    print("Testing ai-sandbox package...")
    test_execute_ai_code()
    test_safe_path_access()
    print("All tests passed!")
