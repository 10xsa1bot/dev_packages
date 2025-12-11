"""
Main Unipile Client
Handles connection and provides access to services.
"""

from typing import Optional, Dict, Any
import requests
from .config import UnipileConfig


class UnipileClient:
    """
    Main Unipile client for API operations.

    This client manages the connection to Unipile and provides
    access to various services for API operations.

    Example:
        >>> from unipile_client import UnipileClient
        >>> client = UnipileClient.from_env()
        >>> # Or with explicit config
        >>> client = UnipileClient(dsn="your-dsn")
    """

    def __init__(
        self,
        dsn: Optional[str] = None,
        api_url: Optional[str] = None,
        config: Optional[UnipileConfig] = None
    ):
        """
        Initialize Unipile client.

        Args:
            dsn: Unipile DSN
            api_url: Unipile API base URL
            config: UnipileConfig object (overrides dsn and api_url)
        """
        if config:
            self.config = config
        elif dsn:
            self.config = UnipileConfig(
                dsn=dsn,
                api_url=api_url or "https://api4.unipile.com:13443"
            )
        else:
            raise ValueError("Either provide dsn or config parameter")

        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "X-API-KEY": self.config.dsn
        })

    @classmethod
    def from_env(cls) -> "UnipileClient":
        """
        Create client from environment variables.

        Environment variables:
            UNIPILE_DSN: Unipile DSN

        Returns:
            UnipileClient instance

        Example:
            >>> client = UnipileClient.from_env()
        """
        config = UnipileConfig.from_env()
        return cls(config=config)

    @classmethod
    def from_dict(cls, config_dict: dict) -> "UnipileClient":
        """
        Create client from configuration dictionary.

        Args:
            config_dict: Dictionary with 'dsn' and optionally 'api_url'

        Returns:
            UnipileClient instance

        Example:
            >>> client = UnipileClient.from_dict({
            ...     'dsn': 'your-dsn',
            ...     'api_url': 'https://api4.unipile.com:13443'
            ... })
        """
        config = UnipileConfig.from_dict(config_dict)
        return cls(config=config)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Unipile API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON body data

        Returns:
            Response dictionary

        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.config.api_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.config.timeout
            )

            response.raise_for_status()

            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.text else None,
                "message": "Request successful"
            }

        except requests.exceptions.HTTPError as e:
            error_detail = None
            try:
                error_detail = e.response.json() if e.response else None
            except:
                pass

            return {
                "success": False,
                "status_code": e.response.status_code if e.response else None,
                "error": str(e),
                "error_detail": error_detail,
                "message": f"HTTP error occurred: {e}"
            }

        except requests.exceptions.ConnectionError as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to connect to Unipile API"
            }

        except requests.exceptions.Timeout as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Request timeout"
            }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"An error occurred: {e}"
            }

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make GET request to Unipile API.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            Response dictionary
        """
        return self._make_request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make POST request to Unipile API.

        Args:
            endpoint: API endpoint path
            data: JSON body data
            params: Query parameters

        Returns:
            Response dictionary
        """
        return self._make_request("POST", endpoint, params=params, json_data=data)

    def test_connection(self) -> bool:
        """
        Test the connection to Unipile API.

        Returns:
            True if connection successful, False otherwise

        Example:
            >>> if client.test_connection():
            ...     print("Connected!")
        """
        try:
            # Try to get own profile as connection test
            result = self.get("/api/v1/users/me")
            return result.get("success", False)
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
