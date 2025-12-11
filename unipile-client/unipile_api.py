"""
Unipile API - Main entry point for Unipile operations.

This module provides a simple interface to access all Unipile
functionality through a single API class.

Example:
    >>> from unipile_api import UnipileAPI
    >>>
    >>> # Initialize
    >>> api = UnipileAPI.from_env()
    >>>
    >>> # Get own profile
    >>> result = api.profiles.get_own_profile(account_id="acc_123")
    >>>
    >>> # Get another user's profile
    >>> result = api.profiles.get_user_profile(
    ...     account_id="acc_123",
    ...     identifier="johndoe"
    ... )
"""

from typing import Optional
from unipile_client import UnipileClient, ProfilesService
from unipile_client.config import UnipileConfig


class UnipileAPI:
    """
    Main API class for Unipile operations.

    Provides easy access to all Unipile operations through
    a single interface.

    Example:
        >>> # From environment variables
        >>> api = UnipileAPI.from_env()
        >>>
        >>> # Or with explicit config
        >>> api = UnipileAPI(dsn="your-dsn")
    """

    def __init__(
        self,
        dsn: Optional[str] = None,
        api_url: Optional[str] = None,
        config: Optional[UnipileConfig] = None
    ):
        """
        Initialize Unipile API.

        Args:
            dsn: Unipile DSN
            api_url: Unipile API base URL
            config: UnipileConfig object (overrides dsn and api_url)
        """
        # Initialize client
        self._client = UnipileClient(dsn=dsn, api_url=api_url, config=config)

        # Initialize services
        self._profiles = ProfilesService(self._client)

    @classmethod
    def from_env(cls) -> "UnipileAPI":
        """
        Create API instance from environment variables.

        Environment variables:
            UNIPILE_DSN: Unipile DSN

        Returns:
            UnipileAPI instance

        Example:
            >>> api = UnipileAPI.from_env()
        """
        config = UnipileConfig.from_env()
        return cls(config=config)

    @classmethod
    def from_dict(cls, config_dict: dict) -> "UnipileAPI":
        """
        Create API instance from configuration dictionary.

        Args:
            config_dict: Dictionary with 'dsn' and optionally 'api_url'

        Returns:
            UnipileAPI instance

        Example:
            >>> api = UnipileAPI.from_dict({
            ...     'dsn': 'your-dsn',
            ...     'api_url': 'https://api4.unipile.com:13443'
            ... })
        """
        config = UnipileConfig.from_dict(config_dict)
        return cls(config=config)

    @property
    def client(self) -> UnipileClient:
        """Get the underlying Unipile client."""
        return self._client

    @property
    def profiles(self) -> ProfilesService:
        """
        Access profiles service.

        Returns:
            ProfilesService instance

        Example:
            >>> result = api.profiles.get_own_profile(account_id="acc_123")
            >>> result = api.profiles.get_user_profile(
            ...     account_id="acc_123",
            ...     identifier="johndoe"
            ... )
        """
        return self._profiles

    def test_connection(self) -> bool:
        """
        Test the connection to Unipile API.

        Returns:
            True if connection successful, False otherwise

        Example:
            >>> if api.test_connection():
            ...     print("Connected to Unipile!")
        """
        return self._client.test_connection()


# Convenience function for quick access
def create_api(dsn: Optional[str] = None) -> UnipileAPI:
    """
    Create a Unipile API instance.

    Args:
        dsn: Unipile DSN (optional, reads from env if not provided)

    Returns:
        UnipileAPI instance

    Example:
        >>> from unipile_api import create_api
        >>> api = create_api()  # From environment
        >>> # Or with explicit DSN
        >>> api = create_api(dsn='your-dsn')
    """
    if dsn:
        return UnipileAPI(dsn=dsn)
    else:
        return UnipileAPI.from_env()
