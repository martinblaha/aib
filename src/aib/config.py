"""Configuration management for aib."""

import sys
import tomllib
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / ".config" / "aib"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULTS: dict[str, Any] = {
    "backend": "claude",
    "language": "en",
    "max_results": 5,
    "timeout": 30,
}


def load() -> dict[str, Any]:
    """Load config from file, returning defaults for missing keys."""
    config = dict(DEFAULTS)
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "rb") as f:
            user_config = tomllib.load(f)
        config.update(user_config)
    return config


def save(config: dict[str, Any]) -> None:
    """Save config to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    # Manual TOML serialization for simple flat configs
    lines = []
    for key, value in config.items():
        if isinstance(value, str):
            lines.append(f'{key} = "{value}"')
        elif isinstance(value, bool):
            lines.append(f"{key} = {'true' if value else 'false'}")
        else:
            lines.append(f"{key} = {value}")
    CONFIG_FILE.write_text("\n".join(lines) + "\n")
