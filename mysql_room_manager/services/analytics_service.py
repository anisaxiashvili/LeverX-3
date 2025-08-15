"""Service for analytics operations."""
import logging
from typing import List, Dict, Any

from ..interfaces.repository_interface import AnalyticsRepositoryInterface
from ..database.query_optimizer import QueryOptimizer
from ..exceptions.custom_exceptions import QueryExecutionError


class AnalyticsService:
    
    def __init__(self, analytics_repository: AnalyticsRepositoryInterface,
                 query_optimizer: QueryOptimizer = None):
        self.analytics_repository = analytics_repository
        self.query_optimizer = query_optimizer
        self.logger = logging.getLogger(__name__)
    
    def get_room_student_counts(self) -> List[Dict[str, Any]]:
        try:
            self.logger.info("Retrieving room student counts")
            results = self.analytics_repository.get_rooms_with_student_count()
            
            self.logger.info(f"Retrieved {len(results)} room student counts")
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to get room student counts: {e}")
            raise QueryExecutionError(f"Analytics query failed: {e}")
    
    def get_youngest_rooms(self, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            self.logger.info(f"Retrieving top {limit} youngest rooms")
            results = self.analytics_repository.get_top_rooms_by_avg_age(limit)
            
            self.logger.info(f"Retrieved {len(results)} youngest rooms")
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to get youngest rooms: {e}")
            raise QueryExecutionError(f"Analytics query failed: {e}")
    
    def get_rooms_with_largest_age_gaps(self, limit: int = 5) -> List[Dict[str, Any]]:
        try:
            self.logger.info(f"Retrieving top {limit} rooms with largest age gaps")
            results = self.analytics_repository.get_top_rooms_by_age_difference(limit)
            
            self.logger.info(f"Retrieved {len(results)} rooms with age gaps")
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to get rooms with age gaps: {e}")
            raise QueryExecutionError(f"Analytics query failed: {e}")
    
    def get_mixed_gender_rooms(self) -> List[Dict[str, Any]]:
        try:
            self.logger.info("Retrieving mixed gender rooms")
            results = self.analytics_repository.get_mixed_gender_rooms()
            
            self.logger.info(f"Retrieved {len(results)} mixed gender rooms")
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to get mixed gender rooms: {e}")
            raise QueryExecutionError(f"Analytics query failed: {e}")
    
    def generate_analytics_report(self) -> Dict[str, Any]:
        try:
            self.logger.info("Generating comprehensive analytics report")
            
            report = {
                'room_student_counts': self.get_room_student_counts(),
                'youngest_rooms': self.get_youngest_rooms(),
                'rooms_with_age_gaps': self.get_rooms_with_largest_age_gaps(),
                'mixed_gender_rooms': self.get_mixed_gender_rooms()
            }
            
            report['summary'] = {
                'total_rooms_analyzed': len(report['room_student_counts']),
                'rooms_with_students': len([r for r in report['room_student_counts'] if r['student_count'] > 0]),
                'mixed_gender_room_count': len(report['mixed_gender_rooms'])
            }
            
            self.logger.info("Analytics report generated successfully")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate analytics report: {e}")
            raise QueryExecutionError(f"Report generation failed: {e}")
