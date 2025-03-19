"""Configuration module for codemcp.

This module provides access to user configuration stored in ~/.codemcprc in TOML format.
"""

from pathlib import Path
from typing import Any

import tomli

__all__ = [
    "get_config_path",
    "load_config",
    "get_logger_verbosity",
]

# Default configuration values
DEFAULT_CONFIG = {
    "logger": {
        "verbosity": "INFO",  # Default logging level
    },
}


def get_config_path() -> Path:
    """Return the path to the user's config file."""
    return Path.home() / ".codemcprc"


def load_config() -> dict[str, Any]:
    """Load configuration from ~/.codemcprc file.

    Returns:
        Dict containing the merged configuration (defaults + user config).

    """
    config = DEFAULT_CONFIG.copy()
    config_path = get_config_path()

    if config_path.exists():
        try:
            with open(config_path, "rb") as f:
                user_config = tomli.load(f)

            # Merge user config with defaults
            _merge_configs(config, user_config)
        except Exception as e:
            print(f"Error loading config from {config_path}: {e}")

    return config


def _merge_configs(base: dict[str, Any], override: dict[str, Any]) -> None:
    """Recursively merge override dict into base dict.

    Args:
        base: The base configuration dictionary to merge into.
        override: The override configuration dictionary to merge from.

    """
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _merge_configs(base[key], value)
        else:
            base[key] = value


def get_logger_verbosity() -> str:
    """Get the configured logger verbosity level.

    Returns:
        String representing the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    """
    config = load_config()
    return config["logger"]["verbosity"]
