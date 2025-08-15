"""Custom exceptions for MySQL Student Room Manager."""

from .custom_exceptions import (
    StudentRoomDBError,
    DatabaseConnectionError,
    DatabaseSchemaError,
    DataImportError,
    QueryExecutionError,
    ValidationError,
    ConfigurationError,
    UnsupportedFormatError
)

__all__ = [
    'StudentRoomDBError',
    'DatabaseConnectionError', 
    'DatabaseSchemaError',
    'DataImportError',
    'QueryExecutionError',
    'ValidationError',
    'ConfigurationError',
    'UnsupportedFormatError'
]
