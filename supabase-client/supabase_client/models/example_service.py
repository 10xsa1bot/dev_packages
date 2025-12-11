"""
Example Service - Template for creating custom table services.
Copy and modify this file for your specific tables.
"""

from typing import Dict, Any, Optional, List
from ..services.crud_service import CRUDService
from ..client import SupabaseClient


class ExampleService(CRUDService):
    """
    Example service for a custom table.

    This is a template showing how to create custom services
    for your specific tables. Copy this file and modify it
    for your needs.

    Example:
        >>> from supabase_client import SupabaseClient
        >>> from supabase_client.models import ExampleService
        >>> client = SupabaseClient.from_env()
        >>> service = ExampleService(client, "your_table_name")
    """

    def __init__(
        self,
        client: SupabaseClient,
        table_name: str = "your_table_name"
    ):
        """
        Initialize Example service.

        Args:
            client: SupabaseClient instance
            table_name: Name of your table
        """
        super().__init__(client, table_name)

    # Add your custom methods here

    def custom_method_example(
        self,
        param1: str,
        param2: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Example of a custom method.

        Args:
            param1: Description of param1
            param2: Description of param2

        Returns:
            Response dictionary with results

        Example:
            >>> result = service.custom_method_example('value', 123)
        """
        # Use inherited CRUD methods
        return self.find({"column_name": param1}, limit=param2)

    def get_by_custom_field(self, field_value: Any) -> Dict[str, Any]:
        """
        Get record by a custom field.

        Args:
            field_value: Value to search for

        Returns:
            Response dictionary with record

        Example:
            >>> result = service.get_by_custom_field('some_value')
        """
        return self.find_one({"custom_field": field_value})

    def get_active_records(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Get active records (assuming you have an 'active' or 'status' field).

        Args:
            limit: Maximum number of records

        Returns:
            Response dictionary with active records

        Example:
            >>> result = service.get_active_records(limit=10)
        """
        return self.find({"status": "active"}, limit=limit)

    def bulk_update_status(
        self,
        record_ids: List[Any],
        new_status: str
    ) -> Dict[str, Any]:
        """
        Bulk update status for multiple records.

        Args:
            record_ids: List of record IDs
            new_status: New status value

        Returns:
            Response dictionary with updated records

        Example:
            >>> result = service.bulk_update_status([1, 2, 3], 'completed')
        """
        try:
            response = (
                self._table
                .update({"status": new_status})
                .in_("id", record_ids)
                .execute()
            )
            return self._handle_response(response)
        except Exception as e:
            return self._handle_error(e)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about records in the table.

        Returns:
            Response dictionary with statistics

        Example:
            >>> result = service.get_statistics()
        """
        try:
            total = self.count()
            active = self.count({"status": "active"})

            return {
                "success": True,
                "data": {
                    "total": total.get("count", 0),
                    "active": active.get("count", 0),
                }
            }
        except Exception as e:
            return self._handle_error(e)
