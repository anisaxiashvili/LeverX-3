from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class RoomStudentCount:
    room_id: int
    room_name: str
    student_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'room_id': self.room_id,
            'room_name': self.room_name,
            'student_count': self.student_count
        }


@dataclass
class RoomAvgAge:
    room_id: int
    room_name: str
    average_age: float
    student_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'room_id': self.room_id,
            'room_name': self.room_name,
            'average_age': round(self.average_age, 2),
            'student_count': self.student_count
        }


@dataclass
class RoomAgeDiff:
    room_id: int
    room_name: str
    age_difference: int
    min_age: int
    max_age: int
    student_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'room_id': self.room_id,
            'room_name': self.room_name,
            'age_difference': self.age_difference,
            'min_age': self.min_age,
            'max_age': self.max_age,
            'student_count': self.student_count
        }


@dataclass
class MixedGenderRoom:
    room_id: int
    room_name: str
    male_count: int
    female_count: int
    total_students: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'room_id': self.room_id,
            'room_name': self.room_name,
            'male_count': self.male_count,
            'female_count': self.female_count,
            'total_students': self.total_students
        }

