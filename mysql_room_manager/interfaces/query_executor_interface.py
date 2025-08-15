"""Query executor interface definitions."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple


class QueryExecutorInterface(ABC):
    
    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def execute_batch_query(self, query: str, params_list: List[tuple]) -> int:
        pass
    
    @abstractmethod
    def execute_scalar_query(self, query: str, params: Optional[tuple] = None) -> Any:
        pass
