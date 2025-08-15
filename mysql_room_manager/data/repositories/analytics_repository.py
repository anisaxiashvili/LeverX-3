"""Analytics repository for complex database queries."""
import logging
from typing import List, Dict, Any

from ...interfaces.repository_interface import AnalyticsRepositoryInterface
from ...database.connection_manager import ConnectionManager
from ...queries.analytics_queries import *
from ...models.query_result import (
    RoomStudentCount, RoomAverageAge, RoomAgeDifference, MixedGenderRoom
)
from ...exceptions.custom_exceptions import QueryExecutionError


class AnalyticsRepository(AnalyticsRepositoryInterface):
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.logger = logging.getLogger(__name__)
    
    def get_rooms_with_student_count(self) -> List[Dict[str, Any]]:
        try:
            self.logger.info("Executing query: rooms with student count")
            
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(ROOMS_WITH_STUDENT_COUNT_QUERY)
                results = cursor.fetchall()
                cursor.close()

            room_counts = [
                RoomStudentCount(
                    room_id=row['room_id'],
                    room_name=row['room_name'],
                    student_count=row['student_count']
                ).to_dict()
                for row in results
            ]
            
            self.logger.info(f"Found {len(room_counts)} rooms with student counts")
            return room_counts
            
        except Exception as e:
            error_msg = f"Failed to get rooms with student count: {e}"
            self.logger.error(error_msg)
            raise QueryExecutionError(error_msg)
    
    def get_top_rooms_by_avg_age(self, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            self.logger.info(f"Executing query: top {limit} rooms by average age")
            
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(TOP_ROOMS_BY_AVG_AGE_QUERY, (limit,))
                results = cursor.fetchall()
                cursor.close()
            
            room_ages = [
                RoomAverageAge(
                    room_id=row['room_id'],
                    room_name=row['room_name'],
                    average_age=float(row['average_age']),
                    student_count=row['student_count']
                ).to_dict()
                for row in results
            ]
            
            self.logger.info(f"Found {len(room_ages)} rooms with average ages")
            return room_ages
            
        except Exception as e:
            error_msg = f"Failed to get rooms by average age: {e}"
            self.logger.error(error_msg)
            raise QueryExecutionError(error_msg)
    
    def get_top_rooms_by_age_difference(self, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            self.logger.info(f"Executing query: top {limit} rooms by age difference")
            
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(TOP_ROOMS_BY_AGE_DIFFERENCE_QUERY, (limit,))
                results = cursor.fetchall()
                cursor.close()
            
            room_age_diffs = [
                RoomAgeDifference(
                    room_id=row['room_id'],
                    room_name=row['room_name'],
                    age_difference=row['age_difference'],
                    min_age=row['min_age'],
                    max_age=row['max_age'],
                    student_count=row['student_count']
                ).to_dict()
                for row in results
            ]
            
            self.logger.info(f"Found {len(room_age_diffs)} rooms with age differences")
            return room_age_diffs
            
        except Exception as e:
            error_msg = f"Failed to get rooms by age difference: {e}"
            self.logger.error(error_msg)
            raise QueryExecutionError(error_msg)
    
    def get_mixed_gender_rooms(self) -> List[Dict[str, Any]]:
        try:
            self.logger.info("Executing query: mixed gender rooms")
            
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(MIXED_GENDER_ROOMS_QUERY)
                results = cursor.fetchall()
                cursor.close()
            
            mixed_rooms = [
                MixedGenderRoom(
                    room_id=row['room_id'],
                    room_name=row['room_name'],
                    male_count=row['male_count'],
                    female_count=row['female_count'],
                    total_students=row['total_students']
                ).to_dict()
                for row in results
            ]
            
            self.logger.info(f"Found {len(mixed_rooms)} mixed gender rooms")
            return mixed_rooms
            
        except Exception as e:
            error_msg = f"Failed to get mixed gender rooms: {e}"
            self.logger.error(error_msg)
            raise QueryExecutionError(error_msg)

