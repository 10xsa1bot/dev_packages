"""
Helper utilities for Supabase operations.
"""

from typing import Dict, Any, List, Optional


def format_response(
    data: Any,
    success: bool = True,
    message: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Format a standardized API response.

    Args:
        data: Response data
        success: Success flag
        message: Optional message
        **kwargs: Additional fields to include

    Returns:
        Formatted response dictionary

    Example:
        >>> response = format_response(
        ...     data={'id': 1, 'name': 'John'},
        ...     success=True,
        ...     message='User created successfully'
        ... )
    """
    response = {
        "success": success,
        "data": data,
    }

    if message:
        response["message"] = message

    response.update(kwargs)

    return response


def handle_pagination(
    page: int = 1,
    page_size: int = 10,
    max_page_size: int = 100
) -> Dict[str, int]:
    """
    Calculate pagination parameters.

    Args:
        page: Page number (1-indexed)
        page_size: Number of items per page
        max_page_size: Maximum allowed page size

    Returns:
        Dictionary with limit and offset

    Example:
        >>> params = handle_pagination(page=2, page_size=10)
        >>> # Returns: {'limit': 10, 'offset': 10}
    """
    # Validate and cap page_size
    page_size = min(page_size, max_page_size)
    page_size = max(1, page_size)

    # Validate page
    page = max(1, page)

    # Calculate offset
    offset = (page - 1) * page_size

    return {
        "limit": page_size,
        "offset": offset
    }


def build_filter_query(
    base_query,
    filters: Optional[Dict[str, Any]] = None,
    search: Optional[Dict[str, str]] = None,
    order_by: Optional[str] = None,
    ascending: bool = True
):
    """
    Build a query with filters, search, and ordering.

    Args:
        base_query: Base query object
        filters: Dictionary of exact match filters
        search: Dictionary with 'column' and 'term' for text search
        order_by: Column to order by
        ascending: Sort order

    Returns:
        Modified query object

    Example:
        >>> query = table.select('*')
        >>> query = build_filter_query(
        ...     query,
        ...     filters={'status': 'active'},
        ...     order_by='created_at'
        ... )
    """
    query = base_query

    # Apply exact match filters
    if filters:
        for column, value in filters.items():
            query = query.eq(column, value)

    # Apply text search
    if search and 'column' in search and 'term' in search:
        query = query.ilike(search['column'], f"%{search['term']}%")

    # Apply ordering
    if order_by:
        query = query.order(order_by, desc=not ascending)

    return query


def extract_ids(data: List[Dict[str, Any]], id_field: str = "id") -> List[Any]:
    """
    Extract IDs from a list of records.

    Args:
        data: List of record dictionaries
        id_field: Name of the ID field

    Returns:
        List of IDs

    Example:
        >>> records = [{'id': 1, 'name': 'A'}, {'id': 2, 'name': 'B'}]
        >>> ids = extract_ids(records)
        >>> # Returns: [1, 2]
    """
    return [record.get(id_field) for record in data if id_field in record]


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks.

    Args:
        items: List to split
        chunk_size: Size of each chunk

    Returns:
        List of chunks

    Example:
        >>> items = [1, 2, 3, 4, 5]
        >>> chunks = chunk_list(items, 2)
        >>> # Returns: [[1, 2], [3, 4], [5]]
    """
    return [
        items[i:i + chunk_size]
        for i in range(0, len(items), chunk_size)
    ]
