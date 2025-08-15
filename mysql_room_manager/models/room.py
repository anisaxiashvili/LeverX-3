"""Room data model."""
from dataclasses import dataclass
from typing import Dict, Any
from ..utils.validation import validate_positive_integer, validate_non_empty_string


@dataclass
class Room:
    id: int
    name: str
    
    def __post_init__(self):
        validate_positive_integer(self.id, "Room ID")
        validate_non_empty_string(self.name, "Room name")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name
        }
    
    def to_db_tuple(self) -> tuple:
        return (self.id, self.name)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Room':
        return cls(
            id=data.get('id'),
            name=data.get('name', '')
        )
