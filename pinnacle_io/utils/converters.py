"""
Utility functions for the pinnacle_io package.
"""
from datetime import datetime
from typing import Optional, Union, Any
import re

def convert_integer(value: Union[str, float, int, None]) -> Optional[int]:
    """
    Convert a value to an integer, handling various string representations.
    
    Args:
        value: Value to convert (string, float, int, or None)
        
    Returns:
        Integer value or None if conversion fails or value is None/empty
    """
    if value is None:
        return None
        
    if isinstance(value, str):
        # Handle common string representations
        value = value.strip()
        if value.lower() in ('', 'null', 'none'):
            return None
        # Remove commas from numbers like "1,234"
        value = value.replace(',', '')
    
    try:
        return int(float(value))  # Handle "25.0" -> 25
    except (ValueError, TypeError):
        return None


def convert_float(value: Union[str, float, int, None]) -> Optional[float]:
    """
    Convert a value to a float, handling various string representations.
    
    Args:
        value: Value to convert (string, float, int, or None)
        
    Returns:
        Float value or None if conversion fails or value is None/empty
    """
    if value is None:
        return None
        
    if isinstance(value, str):
        value = value.strip()
        if value.lower() in ('', 'null', 'none'):
            return None
        # Remove commas from numbers like "1,234.56"
        value = value.replace(',', '')
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def convert_string(value: Any, field_name: str) -> Optional[str]:
    """
    Convert a value to a string with appropriate formatting based on field name patterns.
    
    Args:
        value: Value to convert to string
        field_name: Name of the field (used for formatting rules)
        
    Returns:
        Formatted string value or None if value is None/empty
    """
    if value is None:
        return None
        
    if isinstance(value, str) and value.strip().lower() in ('null', 'none'):
        return None
        
    str_value = str(value)
    
    if 'email' in field_name.lower():
        str_value = str_value.lower().strip()
    elif 'phone' in field_name.lower():
        # Remove all non-digit characters from phone numbers
        str_value = re.sub(r'[^\d]', '', str_value)
    # elif 'name' in field_name.lower() or 'title' in field_name.lower():
    #     # Title case for names and titles
    #     str_value = str_value.strip().title()
    # elif field_name.lower().endswith('_code') or field_name.lower().startswith('code_'):
    #     # Uppercase for codes
    #     str_value = str_value.upper().strip()
    
    return str_value


def convert_boolean(value: Union[str, bool, int, None]) -> Optional[bool]:
    """
    Convert a value to a boolean, handling various string representations.
    
    Args:
        value: Value to convert (string, boolean, int, or None)
        
    Returns:
        Boolean value or None if conversion fails or value is None/empty
    """
    if value is None:
        return None
        
    if isinstance(value, str):
        value = value.strip().lower()
        if value in ('true', '1', 'yes', 'on', 'active', 'enabled'):
            return True
        elif value in ('false', '0', 'no', 'off', 'inactive', 'disabled', ''):
            return False
        else:
            raise ValueError(f"Cannot convert '{value}' to boolean")
    return bool(value)


def convert_datetime(value: Union[str, int, float, datetime, None]) -> Optional[datetime]:
    """
    Convert a value to a datetime object, handling various string formats and timestamps.
    
    Args:
        value: Value to convert (string, int, float, datetime, or None)
        
    Returns:
        Datetime object or None if conversion fails or value is None/empty
    """
    if value is None:
        return None
        
    if isinstance(value, datetime):
        return value
        
    if isinstance(value, str):
        value = value.strip()
        if value.lower() in ("", "null", "none"):
            return None

        # Try common datetime formats
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d.%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%m/%d/%Y %H:%M:%S",
            "%d/%m/%Y",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ValueError(f"Cannot parse datetime '{value}'")

    if isinstance(value, (int, float)):
        # Assume Unix timestamp
        return datetime.fromtimestamp(value)
    return value