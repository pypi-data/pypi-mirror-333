# AI Sandbox Template

A GitHub template for creating sandboxed environments to safely run AI models and execute AI-generated code with strict security boundaries.

## 🛡️ Security Features

- Restricted file system access (limited to project directory)
- Controlled code execution using RestrictedPython
- Path validation and sanitization
- Process isolation capabilities

## 🚀 Getting Started

### Use this template

1. Click the "Use this template" button on GitHub
2. Clone your new repository
3. Set up the environment with uv:

```bash
# Install uv if you don't have it already
# pip install uv

# Create virtual environment with Python 3.13
uv venv --python 3.13 .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/MacOS:
source .venv/bin/activate

# Install dependencies using uv
uv pip install -e ".[dev]"

# For Linux-specific security features (requires libcap-dev)
# uv pip install -e ".[linux-security]"
```

## 📁 Repository Structure

```txt
/
├── src/
│   └── ai_sandbox/           # Main package code
│       ├── __init__.py
│       ├── security.py       # Security utilities
│       └── executor.py       # Safe code execution utilities
├── examples/                 # Example usage
│   └── safe_execution.py     # Example of running AI code safely
├── tests/                    # Test cases
│   ├── test_executor.py
│   └── test_security.py
├── pyproject.toml            # Package configuration
├── README.md
└── LICENSE
```

## 🧰 Usage Example

```python
from ai_sandbox.security import safe_path_access, SecurityError
from ai_sandbox.executor import execute_ai_code

# Safely access files only within project directory
try:
    file_path = safe_path_access("data/training.json")
    with open(file_path, 'r') as f:
        data = f.read()
except SecurityError as e:
    print(f"Security violation: {e}")

# Safely execute AI-generated code with restrictions
ai_code = """
def analyze_data(input_data):
    return {"summary": "Data analysis complete", "count": len(input_data)}

result = analyze_data(input_data)
"""

result = execute_ai_code(ai_code, {"input_data": [1, 2, 3]})
print(result)  # Output: {"summary": "Data analysis complete", "count": 3}
```

## 🔒 Best Practices

1. **Never** grant AI access to sensitive directories outside the project
2. Use multiple layers of security - no single mechanism is foolproof
3. Implement logging of all AI actions for audit purposes
4. Regularly update dependencies to patch security vulnerabilities
5. Run security scanning tools like Bandit regularly

## ⚠️ Limitations

- This sandbox provides basic isolation but is not equivalent to container/VM isolation
- Different security mechanisms are available on different operating systems
- Python's dynamic nature makes 100% secure sandboxing difficult

## 🔐 Security Implementation

### Path Security

The AI Sandbox uses multiple layers to ensure file system security:

1. **Path Boundary Enforcement**: Ensures all file operations are restricted to the current directory and its subdirectories
2. **Path Validation**: Validates paths against platform-specific security rules using `pathvalidate`
3. **Absolute Path Resolution**: Converts all paths to absolute and resolved form before validation

### Code Execution Security

The sandbox uses RestrictedPython to enforce several security measures:

1. **Limited Builtins**: Only safe Python builtins are accessible
2. **Import Restrictions**: Prevents importing dangerous modules
3. **Execution Isolation**: Code executes in a restricted environment with limited access to the global namespace

### Example Security Flow

When AI-generated code attempts to access a file:

1. The path is validated using `safe_path_access()`
2. If the path points outside the allowed directory, access is denied
3. If the path contains potentially dangerous patterns, access is denied
4. Only after passing all security checks is file access granted

## 🔍 Testing

Run the security tests to verify sandbox functionality:

```bash
# Run all tests
uv run pytest tests/

# Run with coverage
uv run pytest --cov=ai_sandbox tests/

# Run specific test file
uv run pytest tests/test_executor.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔧 Development

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run linting
uv run ruff check .

# Run code formatting
uv run black .

# Run security checks
uv run bandit -r src/
```
