"""Data loader interface definitions."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class DataLoaderInterface(ABC):
    
    @abstractmethod
    def load_students(self, file_path: str) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def load_rooms(self, file_path: str) -> List[Dict[str, Any]]:
        pass
