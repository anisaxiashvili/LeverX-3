"""Data models for MySQL Student Room Manager."""

from .student import Student
from .room import Room
from .query_result import (
    RoomStudentCount,
    RoomAverageAge, 
    RoomAgeDifference,
    MixedGenderRoom
)

__all__ = [
    'Student',
    'Room',
    'RoomStudentCount',
    'RoomAverageAge',
    'RoomAgeDifference', 
    'MixedGenderRoom'
]
