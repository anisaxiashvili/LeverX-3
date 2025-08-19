import logging
import json
from typing import List, Dict, Any, Optional
from ..database.conn_manager import ConnManager
from ..queries.opt_queries import * 


class Optimizer: 
    
    def __init__(self, conn_manager: ConnManager):
        self.conn_manager = conn_manager
        self.logger = logging.getLogger(__name__)
    
    def analyze_query_perf(self, query: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        try:
            with self.conn_manager.get_conn() as conn:
                cursor = conn.cursor()
                
                explain_query = EXPLAIN_QUERY_TEMPLATE.format(query=query)
                cursor.execute(explain_query)
                explain_result = cursor.fetchone()
                
                if explain_result and explain_result[0]:
                    exec_plan = json.loads(explain_result[0])  
                else:
                    exec_plan = {}
                
                cursor.close()
                
                return {
                    'query': query,
                    'execution_plan': exec_plan,
                    'optimization_suggestions': self._gen_opt_suggestions(exec_plan)  
                }
                
        except Exception as e:
            self.logger.error(f"Query analysis failed: {e}")
            return {
                'query': query,
                'error': str(e),
                'execution_plan': {},
                'optimization_suggestions': []
            }
    
    def get_table_stats(self) -> List[Dict[str, Any]]: 
        try:
            with self.conn_manager.get_conn() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(TABLE_SIZE_ANALYSIS_QUERY, (self.conn_manager.config.database,))
                table_stats = cursor.fetchall()
                cursor.close()
                return table_stats
                
        except Exception as e:
            self.logger.error(f"Failed to get table statistics: {e}")
            return []
    
    def get_index_usage_stats(self) -> List[Dict[str, Any]]:
        try:
            with self.conn_manager.get_conn() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(INDEX_USAGE_ANALYSIS_QUERY, (self.conn_manager.config.database,))
                index_stats = cursor.fetchall()
                cursor.close()
                return index_stats
                
        except Exception as e:
            self.logger.error(f"Failed to get index statistics: {e}")
            return []
    
    def _gen_opt_suggestions(self, exec_plan: Dict[str, Any]) -> List[str]: 
        suggestions = []
        
        try:
            if 'query_block' in exec_plan:
                query_block = exec_plan['query_block']
                
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

