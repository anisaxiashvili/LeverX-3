from abc import ABC, abstractmethod
from typing import List, Dict, Any


class LoaderInterface(ABC):
    
    @abstractmethod
    def load_students(self, file_path: str) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def load_rooms(self, file_path: str) -> List[Dict[str, Any]]:
        pass