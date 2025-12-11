"""
Supabase API - Main entry point for database operations.

This module provides a simple interface to access all Supabase
functionality through a single API class.

Example:
    >>> from supabase_api import SupabaseAPI
    >>>
    >>> # Initialize
    >>> api = SupabaseAPI.from_env()
    >>>
    >>> # Use generic CRUD for any table
    >>> users = api.table('users')
    >>> result = users.get_all(limit=10)
    >>>
    >>> # Or use specific services
    >>> result = api.users.get_by_email('user@example.com')
"""

from typing import Optional, Dict, Any
from supabase_client import SupabaseClient, CRUDService
from supabase_client.models import UsersService, ExampleService
from supabase_client.config import SupabaseConfig


class SupabaseAPI:
    """
    Main API class for Supabase operations.

    Provides easy access to all database operations through
    a single interface.

    Example:
        >>> # From environment variables
        >>> api = SupabaseAPI.from_env()
        >>>
        >>> # Or with explicit config
        >>> api = SupabaseAPI(
        ...     url="https://xxx.supabase.co",
        ...     key="your-key"
        ... )
    """

    def __init__(
        self,
        url: Optional[str] = None,
        key: Optional[str] = None,
        config: Optional[SupabaseConfig] = None
    ):
        """
        Initialize Supabase API.

        Args:
            url: Supabase project URL
            key: Supabase anon/service key
            config: SupabaseConfig object (overrides url and key)
        """
        # Initialize client
        self._client = SupabaseClient(url=url, key=key, config=config)

        # Initialize pre-defined services
        self._users = UsersService(self._client)

        # Cache for dynamically created table services
        self._table_services: Dict[str, CRUDService] = {}

    @classmethod
    def from_env(cls) -> "SupabaseAPI":
        """
        Create API instance from environment variables.

        Environment variables:
            SUPABASE_URL: Supabase project URL
            SUPABASE_KEY: Supabase anon/service key

        Returns:
            SupabaseAPI instance

        Example:
            >>> api = SupabaseAPI.from_env()
        """
        config = SupabaseConfig.from_env()
        return cls(config=config)

    @classmethod
    def from_dict(cls, config_dict: dict) -> "SupabaseAPI":
        """
        Create API instance from configuration dictionary.

        Args:
            config_dict: Dictionary with 'url' and 'key'

        Returns:
            SupabaseAPI instance

        Example:
            >>> api = SupabaseAPI.from_dict({
            ...     'url': 'https://xxx.supabase.co',
            ...     'key': 'your-key'
            ... })
        """
        config = SupabaseConfig.from_dict(config_dict)
        return cls(config=config)

    @property
    def client(self) -> SupabaseClient:
        """Get the underlying Supabase client."""
        return self._client

    @property
    def users(self) -> UsersService:
        """
        Access users service.

        Returns:
            UsersService instance

        Example:
            >>> result = api.users.get_by_email('user@example.com')
        """
        return self._users

    def table(self, table_name: str) -> CRUDService:
        """
        Get a CRUD service for any table.

        This creates a generic CRUD service for the specified table,
        giving you access to all standard database operations.

        Args:
            table_name: Name of the table

        Returns:
            CRUDService instance for the table

        Example:
            >>> posts = api.table('posts')
            >>> result = posts.get_all(limit=10)
            >>> result = posts.create({'title': 'New Post'})
            >>> result = posts.find({'status': 'published'})
        """
        # Check cache first
        if table_name not in self._table_services:
            self._table_services[table_name] = CRUDService(
                self._client,
                table_name
            )

        return self._table_services[table_name]

    def custom_service(self, service_class, *args, **kwargs):
        """
        Create a custom service instance.

        Use this for your custom service classes that extend
        BaseService or CRUDService.

        Args:
            service_class: Your custom service class
            *args: Arguments to pass to service constructor
            **kwargs: Keyword arguments to pass to service constructor

        Returns:
            Instance of your custom service

        Example:
            >>> from my_services import CustomService
            >>> service = api.custom_service(CustomService, 'table_name')
            >>> result = service.custom_method()
        """
        return service_class(self._client, *args, **kwargs)

    def test_connection(self) -> bool:
        """
        Test the connection to Supabase.

        Returns:
            True if connection successful, False otherwise

        Example:
            >>> if api.test_connection():
            ...     print("Connected to Supabase!")
        """
        return self._client.test_connection()

    # Convenience methods for common operations

    def quick_select(
        self,
        table_name: str,
        filters: Optional[Dict[str, Any]] = None,
        columns: str = "*",
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Quick select from any table.

        Args:
            table_name: Name of the table
            filters: Optional filters
            columns: Columns to select
            limit: Maximum number of records

        Returns:
            Response dictionary with records

        Example:
            >>> result = api.quick_select(
            ...     'posts',
            ...     filters={'status': 'published'},
            ...     limit=10
            ... )
        """
        service = self.table(table_name)
        if filters:
            return service.find(filters, columns=columns, limit=limit)
        else:
            return service.get_all(columns=columns, limit=limit)

    def quick_insert(
        self,
        table_name: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Quick insert into any table.

        Args:
            table_name: Name of the table
            data: Data to insert

        Returns:
            Response dictionary with created record

        Example:
            >>> result = api.quick_insert('posts', {
            ...     'title': 'New Post',
            ...     'content': 'Post content'
            ... })
        """
        return self.table(table_name).create(data)

    def quick_update(
        self,
        table_name: str,
        id_value: Any,
        data: Dict[str, Any],
        id_column: str = "id"
    ) -> Dict[str, Any]:
        """
        Quick update in any table.

        Args:
            table_name: Name of the table
            id_value: Value of the ID
            data: Data to update
            id_column: Name of the ID column

        Returns:
            Response dictionary with updated record

        Example:
            >>> result = api.quick_update('posts', 123, {
            ...     'title': 'Updated Title'
            ... })
        """
        return self.table(table_name).update(id_value, data, id_column)

    def quick_delete(
        self,
        table_name: str,
        id_value: Any,
        id_column: str = "id"
    ) -> Dict[str, Any]:
        """
        Quick delete from any table.

        Args:
            table_name: Name of the table
            id_value: Value of the ID
            id_column: Name of the ID column

        Returns:
            Response dictionary

        Example:
            >>> result = api.quick_delete('posts', 123)
        """
        return self.table(table_name).delete(id_value, id_column)


# Convenience function for quick access
def create_api(
    url: Optional[str] = None,
    key: Optional[str] = None
) -> SupabaseAPI:
    """
    Create a Supabase API instance.

    Args:
        url: Supabase URL (optional, reads from env if not provided)
        key: Supabase key (optional, reads from env if not provided)

    Returns:
        SupabaseAPI instance

    Example:
        >>> from supabase_api import create_api
        >>> api = create_api()  # From environment
        >>> # Or with explicit credentials
        >>> api = create_api(url='...', key='...')
    """
    if url and key:
        return SupabaseAPI(url=url, key=key)
    else:
        return SupabaseAPI.from_env()
