"""Repository interface definitions."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class StudentRepositoryInterface(ABC):
    
    @abstractmethod
    def insert_students(self, students: List[Dict[str, Any]]) -> int:
        pass
    
    @abstractmethod
    def get_student_by_id(self, student_id: int) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_students_by_room(self, room_id: int) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def count_students(self) -> int:
        pass


class RoomRepositoryInterface(ABC):
    
    @abstractmethod
    def insert_rooms(self, rooms: List[Dict[str, Any]]) -> int:
        pass
    
    @abstractmethod
    def get_room_by_id(self, room_id: int) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def count_rooms(self) -> int:
        pass


class AnalyticsRepositoryInterface(ABC):
    
    @abstractmethod
    def get_rooms_with_student_count(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_top_rooms_by_avg_age(self, limit: int = 5) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_top_rooms_by_age_difference(self, limit: int = 5) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_mixed_gender_rooms(self) -> List[Dict[str, Any]]:
        pass

