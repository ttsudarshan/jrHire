def first_letter(value):
    return value.replace(""," ").split()[0].upper() if value else ""

def thisisthat_remote(value):
    if value == True:
        return "Remote"
    else:
        return "Not Remote"
    
def thisisthat_worldwide(value):
    if value == True:
        return "Worldwide"
    else:
        return "Not Worldwide"
    
from datetime import datetime, timezone
from typing import Optional, Union
from zoneinfo import ZoneInfo  # Modern timezone handling

def time_since(created_at: Optional[Union[datetime, str]] = None) -> str:
    """
    Calculate human-readable time difference between now and a given datetime.
    
    Args:
        created_at: Datetime object or ISO format string. If None, returns "No date provided"
        
    Returns:
        String representing time elapsed in a human-readable format
    """
    if created_at is None:
        return "No date provided"
    
    # Convert string to datetime if needed
    if isinstance(created_at, str):
        try:
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        except ValueError:
            return "Invalid date format"
    
    # Ensure datetime is timezone-aware
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    
    now = datetime.now(timezone.utc)
    diff = now - created_at
    
    # Handle future dates
    if diff.total_seconds() < 0:
        return "in the future"
    
    # Define time intervals in seconds
    intervals = [
        (60 * 60 * 24 * 365, "year"),
        (60 * 60 * 24 * 30, "month"),
        (60 * 60 * 24 * 7, "week"),
        (60 * 60 * 24, "day"),
        (60 * 60, "hour"),
        (60, "minute")
    ]
    
    seconds = int(diff.total_seconds())
    
    # Find the appropriate time interval
    for seconds_in_interval, interval_name in intervals:
        if seconds >= seconds_in_interval:
            count = seconds // seconds_in_interval
            return f"{count} {interval_name}{'s' if count > 1 else ''} ago"
    
    # Handle cases less than a minute
    if seconds <= 0:
        return "just now"
    return "less than a minute ago"

def check_compensation(value):
    return value if value else "there is no compensation"