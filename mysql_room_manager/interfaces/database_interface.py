"""Database interface definitions."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from contextlib import contextmanager


class DatabaseConnectionInterface(ABC):
    
    @abstractmethod
    def connect(self) -> Any:
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        pass
    
    @abstractmethod
    @contextmanager
    def get_connection(self):
        pass


class DatabaseSchemaInterface(ABC):
    
    @abstractmethod
    def create_database(self) -> None:
        pass
    
    @abstractmethod
    def create_tables(self) -> None:
        pass
    
    @abstractmethod
    def drop_tables(self) -> None:
        pass
    
    @abstractmethod
    def create_indexes(self) -> None:
        pass
    
    @abstractmethod
    def table_exists(self, table_name: str) -> bool:
        pass


class TransactionManagerInterface(ABC):
    
    @abstractmethod
    @contextmanager
    def transaction(self):
        pass
    
    @abstractmethod
    def begin(self) -> None:
        pass
    
    @abstractmethod
    def commit(self) -> None:
        pass
    
    @abstractmethod
    def rollback(self) -> None:
        pass
