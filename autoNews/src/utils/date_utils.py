from datetime import datetime
from dateutil import parser as date_parser
from typing import Optional
import time


def parse_date(date_string: str, default: Optional[datetime] = None) -> datetime:
    """
    Parse a date string into a datetime object

    Args:
        date_string: Date string in various formats
        default: Default datetime to return if parsing fails

    Returns:
        Parsed datetime object
    """
    if not date_string:
        return default or datetime.now()

    try:
        # Try using dateutil parser (handles most formats)
        return date_parser.parse(date_string)
    except (ValueError, TypeError):
        # Fallback to current time
        return default or datetime.now()


def format_date(dt: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    Format a datetime object as a string

    Args:
        dt: Datetime object
        format_str: Format string (default: YYYY-MM-DD)

    Returns:
        Formatted date string
    """
    return dt.strftime(format_str)


def get_today_filename() -> str:
    """Get a filename-friendly string for today's date"""
    return datetime.now().strftime("%Y-%m-%d")


def parse_struct_time(struct_time) -> datetime:
    """
    Convert a time.struct_time to datetime

    Args:
        struct_time: time.struct_time object (from feedparser)

    Returns:
        Datetime object
    """
    if struct_time:
        return datetime.fromtimestamp(time.mktime(struct_time))
    return datetime.now()
