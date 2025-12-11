"""
Profiles Service for Unipile API
Provides functions to read user profiles.
"""

from typing import Dict, Any, Optional
from .client import UnipileClient


class ProfilesService:
    """
    Service for LinkedIn profile operations via Unipile API.

    Provides methods to read own profile and other users' profiles.

    Example:
        >>> from unipile_client import UnipileClient, ProfilesService
        >>> client = UnipileClient.from_env()
        >>> profiles = ProfilesService(client)
        >>> my_profile = profiles.get_own_profile(account_id="account_123")
    """

    def __init__(self, client: UnipileClient):
        """
        Initialize Profiles service.

        Args:
            client: UnipileClient instance
        """
        self.client = client

    def get_own_profile(
        self,
        account_id: str,
        provider: str = "LINKEDIN"
    ) -> Dict[str, Any]:
        """
        Get own profile (account owner profile).

        Retrieves the profile information of the authenticated account owner.

        API Reference:
            https://developer.unipile.com/reference/userscontroller_getaccountownerprofile

        Args:
            account_id: The Unipile account ID
            provider: The provider (default: "LINKEDIN")

        Returns:
            Response dictionary with profile data

        Response format:
            {
                "success": True,
                "data": {
                    "id": "profile_id",
                    "name": "User Name",
                    "headline": "Professional Title",
                    "location": "City, Country",
                    "profile_url": "https://linkedin.com/in/...",
                    "profile_picture": "https://...",
                    "connections": 500,
                    "followers": 1000,
                    ...
                },
                "message": "Request successful"
            }

        Example:
            >>> result = profiles.get_own_profile(account_id="acc_123")
            >>> if result['success']:
            ...     profile = result['data']
            ...     print(f"Name: {profile.get('name')}")
            ...     print(f"Headline: {profile.get('headline')}")
        """
        endpoint = f"/api/v1/users/{account_id}/profile"
        params = {"provider": provider}

        result = self.client.get(endpoint, params=params)

        # Add context to error message
        if not result.get("success"):
            result["context"] = "Failed to get own profile"

        return result

    def get_user_profile(
        self,
        account_id: str,
        identifier: str,
        provider: str = "LINKEDIN"
    ) -> Dict[str, Any]:
        """
        Get profile of another user by identifier.

        Retrieves the profile information of any LinkedIn user by their
        profile URL or identifier.

        API Reference:
            https://developer.unipile.com/reference/userscontroller_getprofilebyidentifier

        Args:
            account_id: The Unipile account ID
            identifier: User identifier (can be profile URL or LinkedIn ID)
                       Examples:
                       - "https://linkedin.com/in/username"
                       - "username"
                       - LinkedIn member ID
            provider: The provider (default: "LINKEDIN")

        Returns:
            Response dictionary with profile data

        Response format:
            {
                "success": True,
                "data": {
                    "id": "profile_id",
                    "name": "User Name",
                    "headline": "Professional Title",
                    "location": "City, Country",
                    "profile_url": "https://linkedin.com/in/...",
                    "profile_picture": "https://...",
                    "about": "About section text",
                    "experience": [...],
                    "education": [...],
                    "connections": 500,
                    ...
                },
                "message": "Request successful"
            }

        Example:
            >>> # By profile URL
            >>> result = profiles.get_user_profile(
            ...     account_id="acc_123",
            ...     identifier="https://linkedin.com/in/johndoe"
            ... )
            >>>
            >>> # By username
            >>> result = profiles.get_user_profile(
            ...     account_id="acc_123",
            ...     identifier="johndoe"
            ... )
            >>>
            >>> if result['success']:
            ...     profile = result['data']
            ...     print(f"Name: {profile.get('name')}")
            ...     print(f"Headline: {profile.get('headline')}")
            ...     print(f"Connections: {profile.get('connections')}")
        """
        endpoint = f"/api/v1/users/{account_id}/profile"
        params = {
            "provider": provider,
            "identifier": identifier
        }

        result = self.client.get(endpoint, params=params)

        # Add context to error message
        if not result.get("success"):
            result["context"] = f"Failed to get profile for identifier: {identifier}"

        return result

    def get_user_profile_by_url(
        self,
        account_id: str,
        profile_url: str,
        provider: str = "LINKEDIN"
    ) -> Dict[str, Any]:
        """
        Get profile by LinkedIn profile URL (convenience method).

        This is a convenience wrapper around get_user_profile() specifically
        for profile URLs.

        Args:
            account_id: The Unipile account ID
            profile_url: Full LinkedIn profile URL
            provider: The provider (default: "LINKEDIN")

        Returns:
            Response dictionary with profile data

        Example:
            >>> result = profiles.get_user_profile_by_url(
            ...     account_id="acc_123",
            ...     profile_url="https://www.linkedin.com/in/johndoe/"
            ... )
        """
        return self.get_user_profile(
            account_id=account_id,
            identifier=profile_url,
            provider=provider
        )

    def get_user_profile_by_username(
        self,
        account_id: str,
        username: str,
        provider: str = "LINKEDIN"
    ) -> Dict[str, Any]:
        """
        Get profile by LinkedIn username (convenience method).

        This is a convenience wrapper around get_user_profile() specifically
        for usernames.

        Args:
            account_id: The Unipile account ID
            username: LinkedIn username (without URL)
            provider: The provider (default: "LINKEDIN")

        Returns:
            Response dictionary with profile data

        Example:
            >>> result = profiles.get_user_profile_by_username(
            ...     account_id="acc_123",
            ...     username="johndoe"
            ... )
        """
        return self.get_user_profile(
            account_id=account_id,
            identifier=username,
            provider=provider
        )

    def extract_profile_data(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extract profile data from API response.

        Helper method to extract clean profile data from API response.

        Args:
            result: Response dictionary from get_own_profile or get_user_profile

        Returns:
            Profile data dictionary or None if failed

        Example:
            >>> result = profiles.get_own_profile(account_id="acc_123")
            >>> profile = profiles.extract_profile_data(result)
            >>> if profile:
            ...     print(f"Name: {profile['name']}")
        """
        if result.get("success") and result.get("data"):
            return result["data"]
        return None

    def compare_profiles(
        self,
        account_id: str,
        identifier1: str,
        identifier2: str,
        provider: str = "LINKEDIN"
    ) -> Dict[str, Any]:
        """
        Compare two user profiles.

        Fetches two profiles and provides them for comparison.

        Args:
            account_id: The Unipile account ID
            identifier1: First user identifier
            identifier2: Second user identifier
            provider: The provider (default: "LINKEDIN")

        Returns:
            Dictionary with both profiles

        Example:
            >>> result = profiles.compare_profiles(
            ...     account_id="acc_123",
            ...     identifier1="johndoe",
            ...     identifier2="janedoe"
            ... )
            >>> if result['success']:
            ...     profile1 = result['profile1']
            ...     profile2 = result['profile2']
        """
        profile1_result = self.get_user_profile(account_id, identifier1, provider)
        profile2_result = self.get_user_profile(account_id, identifier2, provider)

        if profile1_result.get("success") and profile2_result.get("success"):
            return {
                "success": True,
                "profile1": profile1_result["data"],
                "profile2": profile2_result["data"],
                "message": "Both profiles retrieved successfully"
            }
        else:
            errors = []
            if not profile1_result.get("success"):
                errors.append(f"Profile 1 error: {profile1_result.get('error')}")
            if not profile2_result.get("success"):
                errors.append(f"Profile 2 error: {profile2_result.get('error')}")

            return {
                "success": False,
                "error": "; ".join(errors),
                "profile1": profile1_result.get("data"),
                "profile2": profile2_result.get("data"),
                "message": "Failed to retrieve one or both profiles"
            }
