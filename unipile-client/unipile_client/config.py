"""
Configuration module for Unipile Client
Handles API credentials and configuration settings.
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class UnipileConfig:
    """Unipile API configuration dataclass."""

    dsn: str
    api_url: str = "https://api4.unipile.com:13443"
    timeout: int = 30

    @classmethod
    def from_env(cls) -> "UnipileConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            UNIPILE_DSN: Unipile DSN (Data Source Name)
            UNIPILE_API_URL: API base URL (default: https://api4.unipile.com:13443)
            UNIPILE_TIMEOUT: Request timeout (default: 30)

        Returns:
            UnipileConfig instance

        Raises:
            ValueError: If required environment variables are missing
        """
        dsn = os.getenv("UNIPILE_DSN")

        if not dsn:
            raise ValueError(
                "UNIPILE_DSN environment variable is required. "
                "Set it to your Unipile DSN."
            )

        api_url = os.getenv("UNIPILE_API_URL", "https://api4.unipile.com:13443")
        timeout = int(os.getenv("UNIPILE_TIMEOUT", "30"))

        return cls(
            dsn=dsn,
            api_url=api_url,
            timeout=timeout
        )

    @classmethod
    def from_dict(cls, config_dict: dict) -> "UnipileConfig":
        """
        Create configuration from dictionary.

        Args:
            config_dict: Dictionary with configuration values

        Returns:
            UnipileConfig instance
        """
        return cls(**config_dict)
