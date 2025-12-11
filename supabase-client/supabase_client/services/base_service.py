"""
Base Service for Supabase operations.
Provides common functionality for all services.
"""

from typing import Optional, Dict, Any, List
from ..client import SupabaseClient


class BaseService:
    """
    Base service class for Supabase operations.

    This class provides common functionality and should be inherited
    by specific service classes.

    Example:
        >>> class UsersService(BaseService):
        ...     def __init__(self, client: SupabaseClient):
        ...         super().__init__(client, "users")
    """

    def __init__(self, client: SupabaseClient, table_name: str):
        """
        Initialize base service.

        Args:
            client: SupabaseClient instance
            table_name: Name of the table this service operates on
        """
        self.client = client
        self.table_name = table_name
        self._table = client.table(table_name)

    def _handle_response(self, response: Any) -> Dict[str, Any]:
        """
        Handle and format API response.

        Args:
            response: Response from Supabase

        Returns:
            Formatted response dictionary
        """
        return {
            "success": True,
            "data": response.data if hasattr(response, 'data') else response,
            "count": response.count if hasattr(response, 'count') else None,
        }

    def _handle_error(self, error: Exception) -> Dict[str, Any]:
        """
        Handle and format errors.

        Args:
            error: Exception that occurred

        Returns:
            Formatted error dictionary
        """
        return {
            "success": False,
            "error": str(error),
            "data": None,
        }

    def get_table(self):
        """
        Get the table reference.

        Returns:
            Table reference for building custom queries
        """
        return self._table
