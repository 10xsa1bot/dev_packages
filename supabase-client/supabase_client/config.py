"""
Configuration module for Supabase Client
Handles environment variables and configuration settings.
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class SupabaseConfig:
    """Supabase configuration dataclass."""

    url: str
    key: str
    timeout: int = 30
    auto_refresh_token: bool = True
    persist_session: bool = True

    @classmethod
    def from_env(cls) -> "SupabaseConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            SUPABASE_URL: Supabase project URL
            SUPABASE_KEY: Supabase anon/service key
            SUPABASE_TIMEOUT: Request timeout (default: 30)

        Returns:
            SupabaseConfig instance

        Raises:
            ValueError: If required environment variables are missing
        """
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url:
            raise ValueError(
                "SUPABASE_URL environment variable is required. "
                "Set it to your Supabase project URL."
            )

        if not key:
            raise ValueError(
                "SUPABASE_KEY environment variable is required. "
                "Set it to your Supabase anon or service role key."
            )

        timeout = int(os.getenv("SUPABASE_TIMEOUT", "30"))

        return cls(
            url=url,
            key=key,
            timeout=timeout
        )

    @classmethod
    def from_dict(cls, config_dict: dict) -> "SupabaseConfig":
        """
        Create configuration from dictionary.

        Args:
            config_dict: Dictionary with configuration values

        Returns:
            SupabaseConfig instance
        """
        return cls(**config_dict)
