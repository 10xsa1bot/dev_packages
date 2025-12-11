"""
Main Supabase Client
Handles connection and provides access to services.
"""

from typing import Optional
from supabase import create_client, Client
from .config import SupabaseConfig


class SupabaseClient:
    """
    Main Supabase client for database operations.

    This client manages the connection to Supabase and provides
    access to various services for database operations.

    Example:
        >>> from supabase_client import SupabaseClient
        >>> client = SupabaseClient.from_env()
        >>> # Or with explicit config
        >>> client = SupabaseClient(
        ...     url="https://xxx.supabase.co",
        ...     key="your-anon-key"
        ... )
    """

    def __init__(
        self,
        url: Optional[str] = None,
        key: Optional[str] = None,
        config: Optional[SupabaseConfig] = None
    ):
        """
        Initialize Supabase client.

        Args:
            url: Supabase project URL
            key: Supabase anon/service key
            config: SupabaseConfig object (overrides url and key)
        """
        if config:
            self.config = config
        elif url and key:
            self.config = SupabaseConfig(url=url, key=key)
        else:
            raise ValueError(
                "Either provide (url and key) or config parameter"
            )

        # Create Supabase client
        self._client: Client = create_client(
            self.config.url,
            self.config.key
        )

    @classmethod
    def from_env(cls) -> "SupabaseClient":
        """
        Create client from environment variables.

        Environment variables:
            SUPABASE_URL: Supabase project URL
            SUPABASE_KEY: Supabase anon/service key

        Returns:
            SupabaseClient instance

        Example:
            >>> client = SupabaseClient.from_env()
        """
        config = SupabaseConfig.from_env()
        return cls(config=config)

    @classmethod
    def from_dict(cls, config_dict: dict) -> "SupabaseClient":
        """
        Create client from configuration dictionary.

        Args:
            config_dict: Dictionary with 'url' and 'key'

        Returns:
            SupabaseClient instance

        Example:
            >>> client = SupabaseClient.from_dict({
            ...     'url': 'https://xxx.supabase.co',
            ...     'key': 'your-key'
            ... })
        """
        config = SupabaseConfig.from_dict(config_dict)
        return cls(config=config)

    @property
    def client(self) -> Client:
        """
        Get the underlying Supabase client.

        Returns:
            Supabase Client instance
        """
        return self._client

    def table(self, table_name: str):
        """
        Get a table reference for queries.

        Args:
            table_name: Name of the table

        Returns:
            Table reference for building queries

        Example:
            >>> users = client.table('users')
            >>> result = users.select('*').execute()
        """
        return self._client.table(table_name)

    def test_connection(self) -> bool:
        """
        Test the connection to Supabase.

        Returns:
            True if connection successful, False otherwise

        Example:
            >>> if client.test_connection():
            ...     print("Connected!")
        """
        try:
            # Try to access a table (will fail gracefully if no tables exist)
            self._client.table("_test_").select("*").limit(0).execute()
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
