from datetime import datetime
from typing import Union


def parse_iso_datetime(date_string: str) -> datetime:
    try:
        formats = [
            "%Y-%m-%dT%H:%M:%S.%f",  
            "%Y-%m-%dT%H:%M:%S",     
            "%Y-%m-%d"               
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse datetime string: {date_string}")
        
    except Exception as e:
        raise ValueError(f"Invalid datetime format: {date_string}. Error: {e}")


def calculate_age(birth_date: datetime, reference_date: datetime = None) -> int:
    if reference_date is None:
        reference_date = datetime.now()
    
    age = reference_date.year - birth_date.year
    
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return max(0, age)


def datetime_to_mysql_string(dt: datetime) -> str:
    """Convert datetime to MySQL-compatible string."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

