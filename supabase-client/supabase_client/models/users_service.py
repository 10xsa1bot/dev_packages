"""
Users Service - Example of table-specific service.
Extends CRUDService with custom methods for users table.
"""

from typing import Dict, Any, Optional
from ..services.crud_service import CRUDService
from ..client import SupabaseClient


class UsersService(CRUDService):
    """
    Service for users table operations.

    Extends CRUDService with user-specific methods.

    Example:
        >>> from supabase_client import SupabaseClient
        >>> from supabase_client.models import UsersService
        >>> client = SupabaseClient.from_env()
        >>> users = UsersService(client)
        >>> result = users.get_by_email('user@example.com')
    """

    def __init__(self, client: SupabaseClient, table_name: str = "users"):
        """
        Initialize Users service.

        Args:
            client: SupabaseClient instance
            table_name: Name of users table (default: "users")
        """
        super().__init__(client, table_name)

    # Custom methods for users

    def get_by_email(self, email: str) -> Dict[str, Any]:
        """
        Get user by email address.

        Args:
            email: User's email address

        Returns:
            Response dictionary with user data

        Example:
            >>> result = users.get_by_email('user@example.com')
        """
        return self.find_one({"email": email})

    def get_by_username(self, username: str) -> Dict[str, Any]:
        """
        Get user by username.

        Args:
            username: Username

        Returns:
            Response dictionary with user data

        Example:
            >>> result = users.get_by_username('johndoe')
        """
        return self.find_one({"username": username})

    def get_active_users(
        self,
        limit: Optional[int] = None,
        order_by: str = "created_at"
    ) -> Dict[str, Any]:
        """
        Get all active users.

        Args:
            limit: Maximum number of users to return
            order_by: Column to order by (default: "created_at")

        Returns:
            Response dictionary with active users

        Example:
            >>> result = users.get_active_users(limit=10)
        """
        return self.find(
            {"status": "active"},
            limit=limit,
            order_by=order_by,
            ascending=False
        )

    def create_user(
        self,
        email: str,
        username: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new user.

        Args:
            email: User's email address
            username: Username
            **kwargs: Additional user fields

        Returns:
            Response dictionary with created user

        Example:
            >>> result = users.create_user(
            ...     email='user@example.com',
            ...     username='johndoe',
            ...     first_name='John',
            ...     last_name='Doe'
            ... )
        """
        data = {
            "email": email,
            "username": username,
            **kwargs
        }
        return self.create(data)

    def update_user_status(
        self,
        user_id: Any,
        status: str
    ) -> Dict[str, Any]:
        """
        Update user status.

        Args:
            user_id: User ID
            status: New status (e.g., 'active', 'inactive', 'suspended')

        Returns:
            Response dictionary with updated user

        Example:
            >>> result = users.update_user_status(123, 'active')
        """
        return self.update(user_id, {"status": status})

    def deactivate_user(self, user_id: Any) -> Dict[str, Any]:
        """
        Deactivate a user.

        Args:
            user_id: User ID

        Returns:
            Response dictionary with updated user

        Example:
            >>> result = users.deactivate_user(123)
        """
        return self.update_user_status(user_id, "inactive")

    def search_users(
        self,
        search_term: str,
        limit: Optional[int] = 10
    ) -> Dict[str, Any]:
        """
        Search users by name or email.

        Args:
            search_term: Search term
            limit: Maximum number of results (default: 10)

        Returns:
            Response dictionary with matching users

        Example:
            >>> result = users.search_users('john', limit=5)
        """
        # Search in multiple fields - you can customize this
        return self.search("email", search_term, limit=limit)

    def email_exists(self, email: str) -> Dict[str, Any]:
        """
        Check if email already exists.

        Args:
            email: Email address to check

        Returns:
            Response dictionary with exists boolean

        Example:
            >>> result = users.email_exists('user@example.com')
            >>> if result['exists']:
            ...     print("Email already registered")
        """
        return self.exists({"email": email})

    def username_exists(self, username: str) -> Dict[str, Any]:
        """
        Check if username already exists.

        Args:
            username: Username to check

        Returns:
            Response dictionary with exists boolean

        Example:
            >>> result = users.username_exists('johndoe')
            >>> if result['exists']:
            ...     print("Username already taken")
        """
        return self.exists({"username": username})
