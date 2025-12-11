"""
CRUD Service for Supabase operations.
Provides Create, Read, Update, Delete operations.
"""

from typing import Optional, Dict, Any, List, Union
from .base_service import BaseService
from ..client import SupabaseClient


class CRUDService(BaseService):
    """
    CRUD service for database operations.

    Provides standard Create, Read, Update, Delete operations
    for any Supabase table.

    Example:
        >>> from supabase_client import SupabaseClient, CRUDService
        >>> client = SupabaseClient.from_env()
        >>> users_service = CRUDService(client, "users")
        >>> result = users_service.get_all()
    """

    def __init__(self, client: SupabaseClient, table_name: str):
        """
        Initialize CRUD service.

        Args:
            client: SupabaseClient instance
            table_name: Name of the table
        """
        super().__init__(client, table_name)

    # CREATE operations

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a single record.

        Args:
            data: Dictionary with record data

        Returns:
            Response dictionary with created record

        Example:
            >>> result = service.create({
            ...     'name': 'John Doe',
            ...     'email': 'john@example.com'
            ... })
        """
        try:
            response = self._table.insert(data).execute()
            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    def create_many(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple records.

        Args:
            data: List of dictionaries with record data

        Returns:
            Response dictionary with created records

        Example:
            >>> result = service.create_many([
            ...     {'name': 'John', 'email': 'john@example.com'},
            ...     {'name': 'Jane', 'email': 'jane@example.com'}
            ... ])
        """
        try:
            response = self._table.insert(data).execute()
            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    # READ operations

    def get_all(
        self,
        columns: str = "*",
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        ascending: bool = True
    ) -> Dict[str, Any]:
        """
        Get all records from table.

        Args:
            columns: Columns to select (default: "*")
            limit: Maximum number of records to return
            offset: Number of records to skip
            order_by: Column to order by
            ascending: Sort order (True for ASC, False for DESC)

        Returns:
            Response dictionary with records

        Example:
            >>> result = service.get_all(limit=10, order_by='created_at')
        """
        try:
            query = self._table.select(columns)

            if order_by:
                query = query.order(order_by, desc=not ascending)

            if limit:
                query = query.limit(limit)

            if offset:
                query = query.offset(offset)

            response = query.execute()
            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    def get_by_id(
        self,
        id_value: Any,
        id_column: str = "id",
        columns: str = "*"
    ) -> Dict[str, Any]:
        """
        Get a single record by ID.

        Args:
            id_value: Value of the ID
            id_column: Name of the ID column (default: "id")
            columns: Columns to select (default: "*")

        Returns:
            Response dictionary with record

        Example:
            >>> result = service.get_by_id(123)
            >>> result = service.get_by_id("uuid-here", id_column="user_id")
        """
        try:
            response = self._table.select(columns).eq(id_column, id_value).execute()
            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    def find(
        self,
        filters: Dict[str, Any],
        columns: str = "*",
        limit: Optional[int] = None,
        order_by: Optional[str] = None,
        ascending: bool = True
    ) -> Dict[str, Any]:
        """
        Find records matching filters.

        Args:
            filters: Dictionary of column: value pairs to filter by
            columns: Columns to select (default: "*")
            limit: Maximum number of records to return
            order_by: Column to order by
            ascending: Sort order (True for ASC, False for DESC)

        Returns:
            Response dictionary with matching records

        Example:
            >>> result = service.find({
            ...     'status': 'active',
            ...     'role': 'admin'
            ... }, limit=10)
        """
        try:
            query = self._table.select(columns)

            # Apply filters
            for column, value in filters.items():
                query = query.eq(column, value)

            if order_by:
                query = query.order(order_by, desc=not ascending)

            if limit:
                query = query.limit(limit)

            response = query.execute()
            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    def find_one(
        self,
        filters: Dict[str, Any],
        columns: str = "*"
    ) -> Dict[str, Any]:
        """
        Find a single record matching filters.

        Args:
            filters: Dictionary of column: value pairs to filter by
            columns: Columns to select (default: "*")

        Returns:
            Response dictionary with matching record

        Example:
            >>> result = service.find_one({'email': 'john@example.com'})
        """
        result = self.find(filters, columns=columns, limit=1)

        if result["success"] and result["data"]:
            result["data"] = result["data"][0] if result["data"] else None

        return result

    def search(
        self,
        column: str,
        search_term: str,
        columns: str = "*",
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Search records using text search.

        Args:
            column: Column to search in
            search_term: Text to search for
            columns: Columns to select (default: "*")
            limit: Maximum number of records to return

        Returns:
            Response dictionary with matching records

        Example:
            >>> result = service.search('name', 'John', limit=10)
        """
        try:
            query = self._table.select(columns).ilike(column, f"%{search_term}%")

            if limit:
                query = query.limit(limit)

            response = query.execute()
            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    # UPDATE operations

    def update(
        self,
        id_value: Any,
        data: Dict[str, Any],
        id_column: str = "id"
    ) -> Dict[str, Any]:
        """
        Update a record by ID.

        Args:
            id_value: Value of the ID
            data: Dictionary with fields to update
            id_column: Name of the ID column (default: "id")

        Returns:
            Response dictionary with updated record

        Example:
            >>> result = service.update(123, {'name': 'Jane Doe'})
        """
        try:
            response = self._table.update(data).eq(id_column, id_value).execute()
            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    def update_many(
        self,
        filters: Dict[str, Any],
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update multiple records matching filters.

        Args:
            filters: Dictionary of column: value pairs to filter by
            data: Dictionary with fields to update

        Returns:
            Response dictionary with updated records

        Example:
            >>> result = service.update_many(
            ...     {'status': 'pending'},
            ...     {'status': 'active'}
            ... )
        """
        try:
            query = self._table.update(data)

            for column, value in filters.items():
                query = query.eq(column, value)

            response = query.execute()
            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    # DELETE operations

    def delete(
        self,
        id_value: Any,
        id_column: str = "id"
    ) -> Dict[str, Any]:
        """
        Delete a record by ID.

        Args:
            id_value: Value of the ID
            id_column: Name of the ID column (default: "id")

        Returns:
            Response dictionary

        Example:
            >>> result = service.delete(123)
        """
        try:
            response = self._table.delete().eq(id_column, id_value).execute()
            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    def delete_many(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete multiple records matching filters.

        Args:
            filters: Dictionary of column: value pairs to filter by

        Returns:
            Response dictionary

        Example:
            >>> result = service.delete_many({'status': 'inactive'})
        """
        try:
            query = self._table.delete()

            for column, value in filters.items():
                query = query.eq(column, value)

            response = query.execute()
            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    # COUNT operations

    def count(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Count records in table.

        Args:
            filters: Optional dictionary of column: value pairs to filter by

        Returns:
            Response dictionary with count

        Example:
            >>> result = service.count()
            >>> result = service.count({'status': 'active'})
        """
        try:
            query = self._table.select("*", count="exact")

            if filters:
                for column, value in filters.items():
                    query = query.eq(column, value)

            response = query.execute()
            return {
                "success": True,
                "count": response.count,
                "data": None
            }
        except Exception as e:
            return self._handle_error(e)

    # EXISTS operations

    def exists(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if a record exists matching filters.

        Args:
            filters: Dictionary of column: value pairs to filter by

        Returns:
            Response dictionary with exists boolean

        Example:
            >>> result = service.exists({'email': 'john@example.com'})
            >>> if result['exists']:
            ...     print("User exists")
        """
        try:
            query = self._table.select("*", count="exact").limit(1)

            for column, value in filters.items():
                query = query.eq(column, value)

            response = query.execute()
            return {
                "success": True,
                "exists": response.count > 0,
                "data": None
            }
        except Exception as e:
            return self._handle_error(e)
