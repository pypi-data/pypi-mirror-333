"""
Absfuyu: Core
-------------
Pre-defined typing

Version: 5.1.0
Date updated: 10/03/2025 (dd/mm/yyyy)
"""

# Module Package
# ---------------------------------------------------------------------------
__all__ = ["_T", "_P", "_R", "_CALLABLE", "_CT", "_N", "_Number", "override"]


# Library
# ---------------------------------------------------------------------------
from collections.abc import Callable
from typing import ParamSpec, TypeVar

try:
    from typing import override  # type: ignore
except ImportError:
    from absfuyu.core.decorator import dummy_decorator as override


# Type
# ---------------------------------------------------------------------------
_T = TypeVar("_T")  # Type

# Callable
_P = ParamSpec("_P")  # Parameter type
_R = TypeVar("_R")  # Return type - Can be anything
_CALLABLE = Callable[_P, _R]

# Class type - Can be any subtype of `type`
_CT = TypeVar("_CT", bound=type)

# Number type
_N = TypeVar("_N", int, float)
_Number = int | float
