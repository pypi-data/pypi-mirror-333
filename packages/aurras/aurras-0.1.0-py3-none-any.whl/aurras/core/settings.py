"""
Settings Module

This module provides functionality for loading and creating default settings.
"""

import yaml
from pathlib import Path

from config.path import settings

# Default settings as a dictionary
default_settings = {
    "max-volume": "130",
    "show-video": "no",
    "show-lyrics": "yes",
    "authenticated": "yes",
    "keyboard-shortcuts": {
        "end-song": "q",
        "pause": "p",
        "translate-lyrics": "t",
    },
    "backup": {
        "auto-backup": "on",
        "manual-backup": {
            "status": "off",
            "timed": {
                "status": "off",
                "daily": "off",
                "weekly": "off",
                "monthly": "off",
            },
        },
    },
}


class LoadDefaultSettings:
    """Class for loading default settings from the settings file."""

    def __init__(self) -> None:
        """Initialize with loaded settings."""
        self.settings = self.load_default_settings()

    def load_default_settings(self):
        """Load settings from the settings file."""
        if not settings.exists():
            # Create default settings if file doesn't exist
            self.create_default_settings()

        with open(settings, "r") as default_settings_file:
            settings_data = yaml.safe_load(default_settings_file)

        return settings_data

    def create_default_settings(self):
        """Create the default settings file."""
        settings.parent.mkdir(parents=True, exist_ok=True)

        with open(settings, "w") as config_file:
            yaml.dump(default_settings, config_file, default_flow_style=False, indent=4)

    def reset_default_settings(self):
        """Reset settings to default values."""
        self.create_default_settings()
