"""
Minimal setup.py shim for backward compatibility.

All project metadata is now in pyproject.toml (PEP 621 standard).
Modern Python packaging tools read pyproject.toml directly.

This file exists only for compatibility with legacy tools that
don't yet support PEP 621.

For package metadata, see: pyproject.toml
"""

from setuptools import setup

# Empty setup() reads all metadata from pyproject.toml
setup()
