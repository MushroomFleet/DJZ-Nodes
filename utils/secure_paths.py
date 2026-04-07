"""Centralized path validation utility for DJZ-Nodes.

Provides safe path resolution and validation helpers that all file-handling
nodes can import to defend against path traversal (CWE-22) attacks.

Usage:
    from utils.secure_paths import validate_safe_path, sanitize_glob_pattern

    safe = validate_safe_path(user_input, base_directory="/comfyui/output")
    clean_pattern = sanitize_glob_pattern(raw_pattern)
"""

import os
import re

__all__ = ["validate_safe_path", "sanitize_glob_pattern"]


def validate_safe_path(requested_path: str, base_directory: str) -> str:
    """Resolve *requested_path* and ensure it lives under *base_directory*.

    Raises ``ValueError`` if the resolved path escapes the base directory.
    """
    abs_base = os.path.abspath(base_directory)
    abs_requested = os.path.abspath(os.path.join(abs_base, requested_path))

    try:
        common = os.path.commonpath([abs_base, abs_requested])
    except ValueError:
        raise ValueError(
            f"Path escape detected: '{requested_path}' is not under '{base_directory}'"
        )

    if common != abs_base:
        raise ValueError(
            f"Path escape detected: '{requested_path}' resolves outside '{base_directory}'"
        )

    return abs_requested


def sanitize_glob_pattern(pattern: str) -> str:
    """Strip traversal sequences from a user-supplied glob pattern.

    Returns a cleaned pattern safe for use with ``glob.glob()``.
    Falls back to ``'*'`` if the pattern becomes empty after sanitisation.
    """
    sanitized = pattern.replace("..", "")
    sanitized = sanitized.lstrip("/").lstrip("\\")
    sanitized = re.sub(r'[/\\]{2,}', os.sep, sanitized)
    return sanitized.strip() or "*"
