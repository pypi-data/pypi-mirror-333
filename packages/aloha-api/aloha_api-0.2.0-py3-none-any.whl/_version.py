"""Version information."""

import os

import tomli


def get_version():
    """Get the package version from pyproject.toml."""
    path = os.path.join(os.path.dirname(__file__), "pyproject.toml")
    with open(path, mode="rb") as fp:
        pyproject = tomli.load(fp)
    version = pyproject["project"]["version"]

    # Try to read build number if it exists
    build_path = os.path.join(os.path.dirname(__file__), ".buildnum")
    if os.path.exists(build_path):
        with open(build_path) as f:
            build_num = f.read().strip()
            if build_num:
                version = f"{version}+build.{build_num}"

    return version


__version__ = get_version()
