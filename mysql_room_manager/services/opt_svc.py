import logging
from typing import List, Dict, Any
from ..database.optimizer import Optimizer
from ..queries.analytics_queries import *

class OptSvc:
    
    def __init__(self, optimizer: Optimizer):
        self.optimizer = optimizer 
        self.logger = logging.getLogger(__name__)
    
    def analyze_query_perf(self) -> Dict[str, Any]:
        try:
            self.logger.info("Analyzing query performance")
            
            queries_to_analyze = [
                ("Room Student Count", ROOMS_WITH_STUDENT_COUNT_QUERY),
                ("Top Rooms by Average Age", TOP_ROOMS_BY_AVG_AGE_QUERY.replace("%s", "5")),
                ("Top Rooms by Age Difference", TOP_ROOMS_BY_AGE_DIFFERENCE_QUERY.replace("%s", "5")),
                ("Mixed Gender Rooms", MIXED_GENDER_ROOMS_QUERY)
            ]
            
            analysis_results = {}
            
            for query_name, query in queries_to_analyze:
                self.logger.debug(f"Analyzing query: {query_name}")
                analysis = self.optimizer.analyze_query_perf(query)
                analysis_results[query_name] = analysis
            
            return {
                'query_analyses': analysis_results,
                'table_statistics': self.optimizer.get_table_stats(),
                'index_statistics': self.optimizer.get_index_usage_stats()
            }
            
        except Exception as e:
            self.logger.error(f"Query performance analysis failed: {e}")
            return {'error': str(e)}
    
    def get_opt_recommendations(self) -> List[str]:
        try:
            recommendations = [
                "Composite index on (room_id, sex, age_years) for mixed gender analysis",
                "Index on age_years column for age-based queries", 
                "Index on room_id for student-room relationship queries",
                "Generated column for age calculation to avoid runtime computation",
                "Consider partitioning students table by room_id for large datasets",
                "Monitor query execution plans regularly",
                "Use EXPLAIN ANALYZE to identify bottlenecks",
                "Consider materialized views for frequently accessed analytics"
            ]
            
            self.logger.info("Generated optimization recommendations")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations: {e}")
            return [f"Error generating recommendations: {e}"]

