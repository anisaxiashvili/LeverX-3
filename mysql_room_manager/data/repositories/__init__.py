"""Data repositories for MySQL Student Room Manager."""

from .student_repository import StudentRepository
from .room_repository import RoomRepository
from .analytics_repository import AnalyticsRepository

__all__ = ['StudentRepository', 'RoomRepository', 'AnalyticsRepository']
