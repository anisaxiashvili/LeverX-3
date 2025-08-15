"""Query optimization analysis"""
import logging
import json
from typing import List, Dict, Any, Optional

from ..database.connection_manager import ConnectionManager
from ..queries.optimization_queries import *


class QueryOptimizer:

    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.logger = logging.getLogger(__name__)
    
    def analyze_query_performance(self, query: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                explain_query = EXPLAIN_QUERY_TEMPLATE.format(query=query)
                cursor.execute(explain_query)
                explain_result = cursor.fetchone()
                
                if explain_result and explain_result[0]:
                    execution_plan = json.loads(explain_result[0])
                else:
                    execution_plan = {}
                
                cursor.close()
                
                return {
                    'query': query,
                    'execution_plan': execution_plan,
                    'optimization_suggestions': self._generate_optimization_suggestions(execution_plan)
                }
                
        except Exception as e:
            self.logger.error(f"Query analysis failed: {e}")
            return {
                'query': query,
                'error': str(e),
                'execution_plan': {},
                'optimization_suggestions': []
            }
    
    def get_table_statistics(self) -> List[Dict[str, Any]]:
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(TABLE_SIZE_ANALYSIS_QUERY, (self.connection_manager.config.database,))
                table_stats = cursor.fetchall()
                cursor.close()
                return table_stats
                
        except Exception as e:
            self.logger.error(f"Failed to get table statistics: {e}")
            return []
    
    def get_index_usage_statistics(self) -> List[Dict[str, Any]]:
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(INDEX_USAGE_ANALYSIS_QUERY, (self.connection_manager.config.database,))
                index_stats = cursor.fetchall()
                cursor.close()
                return index_stats
                
        except Exception as e:
            self.logger.error(f"Failed to get index statistics: {e}")
            return []
    
    def _generate_optimization_suggestions(self, execution_plan: Dict[str, Any]) -> List[str]:
        suggestions = []
        
        try:
            if 'query_block' in execution_plan:
                query_block = execution_plan['query_block']
                
                if 'table' in query_block:
                    access_type = query_block.get('table', {}).get('access_type', '')
                    if access_type == 'ALL':
                        suggestions.append("Consider adding indexes - full table scan detected")
                
                if 'nested_loop' in query_block:
                    suggestions.append("Consider optimizing join conditions and adding composite indexes")
                
                if query_block.get('using_filesort'):
                    suggestions.append("Consider adding index for ORDER BY clause to avoid filesort")
                
                if query_block.get('using_temporary_table'):
                    suggestions.append("Query uses temporary table - consider query restructuring")
            
            if not suggestions:
                suggestions.append("Query execution plan looks optimized")
                
        except Exception as e:
            self.logger.error(f"Error generating suggestions: {e}")
            suggestions.append("Unable to analyze execution plan")
        
        return suggestions
