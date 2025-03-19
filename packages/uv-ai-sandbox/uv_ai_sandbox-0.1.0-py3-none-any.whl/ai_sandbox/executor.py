import builtins
from typing import Any, Dict, Optional

from RestrictedPython import compile_restricted  # type: ignore
from RestrictedPython.Guards import (  # type: ignore
    full_write_guard,
    guarded_iter_unpack_sequence,
    guarded_unpack_sequence,
    safe_builtins,
    safe_globals,
    safer_getattr,
)


# Custom implementation of limited_range
def limited_range(start, stop=None, step=None):
    """A range with a limited number of elements for safety."""
    if stop is None:
        stop = start
        start = 0
    if step is None:
        step = 1

    # Limit to max 10000 elements to prevent resource exhaustion
    if (stop - start) // step > 10000:
        raise ValueError("Range too large, maximum size is 10000 elements")

    return range(start, stop, step)


# Define a safe_import function that only allows whitelisted modules
def safe_import(name, *args, **kwargs):
    """Only allow importing from a specific whitelist of safe modules."""
    safe_modules = [
        "math",
        "random",
        "json",
        "re",
        "datetime",
        "collections",
        "itertools",
        "functools",
    ]

    if name not in safe_modules:
        raise ImportError(
            f"Import of module '{name}' is restricted for security reasons"
        )

    return __import__(name, *args, **kwargs)


def execute_ai_code(code_string: str, inputs: Optional[Dict[str, Any]] = None) -> Any:
    """
    Execute AI-generated code in a restricted environment.

    Args:
        code_string: String containing Python code to execute
        inputs: Dictionary of input values available to the code

    Returns:
        Any: The result of the execution

    Raises:
        Exception: If code fails to compile or execute
    """
    # Prepare safe execution environment
    restricted_globals = dict(safe_globals)
    restricted_builtins = dict(safe_builtins)

    # Add safe versions of necessary builtins
    whitelist = [
        "list",
        "dict",
        "tuple",
        "set",
        "sum",
        "range",
        "len",
        "int",
        "float",
        "str",
        "bool",
        "True",
        "False",
        "None",
        # Remove __import__ from whitelist to restrict imports
    ]

    for name in whitelist:
        if hasattr(builtins, name):
            restricted_builtins[name] = getattr(builtins, name)

    # Replace __import__ with our safe version
    restricted_builtins["__import__"] = safe_import

    restricted_globals["__builtins__"] = restricted_builtins

    # Add all necessary guards for RestrictedPython
    restricted_globals["_getiter_"] = iter
    restricted_globals["_iter_unpack_sequence_"] = guarded_iter_unpack_sequence
    restricted_globals["_unpack_sequence_"] = guarded_unpack_sequence
    restricted_globals["_getitem_"] = lambda obj, key: obj[key]
    restricted_globals["_write_"] = full_write_guard
    restricted_globals["_getattr_"] = safer_getattr
    restricted_globals["_apply_"] = lambda func, *args, **kwargs: func(*args, **kwargs)
    restricted_globals["_range_"] = limited_range
    # Add inplace operation guard
    restricted_globals["_inplacevar_"] = lambda op, x, y: operator_guard(op, x, y)

    # Add input data to the environment
    if inputs:
        for key, value in inputs.items():
            restricted_globals[key] = value

    # Compile the code with restrictions
    byte_code = compile_restricted(code_string, "<ai_generated>", "exec")

    # Initialize result as an empty dict instead of None
    restricted_globals["result"] = {}

    # Execute the code
    exec(byte_code, restricted_globals)

    # Return result if defined, otherwise return None
    return restricted_globals.get("result")


# Helper function for inplace operations
def operator_guard(op, x, y):
    """Guard for inplace operations."""
    if op == "+=":
        return x + y
    elif op == "-=":
        return x - y
    elif op == "*=":
        return x * y
    elif op == "/=":
        return x / y
    elif op == "//=":
        return x // y
    elif op == "%=":
        return x % y
    elif op == "**=":
        return x**y
    elif op == "<<=":
        return x << y
    elif op == ">>=":
        return x >> y
    elif op == "&=":
        return x & y
    elif op == "^=":
        return x ^ y
    elif op == "|=":
        return x | y
    else:
        raise NotImplementedError(f"Unsupported inplace operation: {op}")
