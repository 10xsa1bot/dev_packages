"""
Supabase Client Module
Provides a modular interface for Supabase database operations.
"""

from .client import SupabaseClient
from .services.base_service import BaseService
from .services.crud_service import CRUDService
from .supabase_api import SupabaseAPI

__version__ = "1.0.0"
__all__ = [
    "SupabaseClient",
    "BaseService",
    "CRUDService",
    "SupabaseAPI",
]
