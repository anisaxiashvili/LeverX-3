"""Interface definitions for MySQL Student Room Manager."""

from .database_interface import (
    DatabaseConnectionInterface,
    DatabaseSchemaInterface, 
    TransactionManagerInterface
)
from .repository_interface import (
    StudentRepositoryInterface,
    RoomRepositoryInterface,
    AnalyticsRepositoryInterface
)
from .data_loader_interface import DataLoaderInterface
from .query_executor_interface import QueryExecutorInterface

__all__ = [
    'DatabaseConnectionInterface',
    'DatabaseSchemaInterface',
    'TransactionManagerInterface',
    'StudentRepositoryInterface', 
    'RoomRepositoryInterface',
    'AnalyticsRepositoryInterface',
    'DataLoaderInterface',
    'QueryExecutorInterface'
]


