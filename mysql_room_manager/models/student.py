"""Student data model."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from ..utils.validation import validate_positive_integer, validate_non_empty_string
from ..utils.date_utils import parse_iso_datetime, calculate_age


@dataclass
class Student:
    id: int
    name: str
    birthday: datetime
    sex: str
    room: Optional[int] = None
    
    def __post_init__(self):
        validate_positive_integer(self.id, "Student ID")
        validate_non_empty_string(self.name, "Student name")
        
        if not isinstance(self.birthday, datetime):
            raise ValueError("Birthday must be a datetime object")
        
        if self.sex not in ('M', 'F'):
            raise ValueError("Sex must be 'M' or 'F'")
        
        if self.room is not None:
            validate_positive_integer(self.room, "Room ID")
    
    @property
    def age(self) -> int:
        return calculate_age(self.birthday)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'birthday': self.birthday.isoformat(),
            'sex': self.sex,
            'room': self.room,
            'age': self.age
        }
    
    def to_db_tuple(self) -> tuple:
        return (self.id, self.name, self.birthday, self.sex, self.room)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        birthday = data.get('birthday')
        if isinstance(birthday, str):
            birthday = parse_iso_datetime(birthday)
        
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            birthday=birthday,
            sex=data.get('sex', ''),
            room=data.get('room')
        )

