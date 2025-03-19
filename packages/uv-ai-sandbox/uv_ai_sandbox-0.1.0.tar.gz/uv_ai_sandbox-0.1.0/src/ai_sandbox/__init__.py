"""
UV AI Sandbox - Safely run AI models and execute AI-generated code with strict security boundaries.

This package provides tools for creating sandboxed environments to safely run AI models
and execute AI-generated code with strict security boundaries.
"""

__version__ = "0.1.0"

from ai_sandbox.executor import execute_ai_code
from ai_sandbox.security import safe_path_access, SecurityError

__all__ = ["execute_ai_code", "safe_path_access", "SecurityError"]