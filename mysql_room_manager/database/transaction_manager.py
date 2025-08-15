"""Transaction management for database operations."""
import logging
from contextlib import contextmanager
from typing import Optional

from ..interfaces.database_interface import TransactionManagerInterface
from ..database.connection_manager import ConnectionManager
from ..exceptions.custom_exceptions import QueryExecutionError


class TransactionManager(TransactionManagerInterface):
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.logger = logging.getLogger(__name__)
        self._current_connection = None
    
    @contextmanager
    def transaction(self):
        connection = None
        try:
            connection = self.connection_manager.connect()
            self._current_connection = connection
            
            connection.start_transaction()
            self.logger.debug("Transaction started")
            yield connection
            
            connection.commit()
            self.logger.debug("Transaction committed")
            
        except Exception as e:
            if connection and connection.is_connected():
                connection.rollback()
                self.logger.warning(f"Transaction rolled back due to error: {e}")
            raise QueryExecutionError(f"Transaction failed: {e}")
            
        finally:
            if connection and connection.is_connected():
                connection.close()
            self._current_connection = None
    
    def begin(self) -> None:
        if self._current_connection:
            self._current_connection.start_transaction()
            self.logger.debug("Manual transaction started")
    
    def commit(self) -> None:
        if self._current_connection:
            self._current_connection.commit()
            self.logger.debug("Manual transaction committed")
    
    def rollback(self) -> None:
        if self._current_connection:
            self._current_connection.rollback()
            self.logger.debug("Manual transaction rolled back")
