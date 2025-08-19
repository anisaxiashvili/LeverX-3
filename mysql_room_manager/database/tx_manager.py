import logging
from contextlib import contextmanager
from ..interfaces.db_interface import TxInterface
from ..database.conn_manager import ConnManager
from ..exceptions.exceptions import QueryError


class TxManager(TxInterface):  
    
    def __init__(self, conn_manager: ConnManager):
        self.conn_manager = conn_manager  
        self.logger = logging.getLogger(__name__)
        self._current_conn = None  
    
    @contextmanager
    def transaction(self):
        connection = None
        try:
            connection = self.conn_manager.connect()
            self._current_conn = connection
            
            connection.start_transaction()
            self.logger.debug("Transaction started")
            
            yield connection
            
            connection.commit()
            self.logger.debug("Transaction committed")
            
        except Exception as e:
            if connection and connection.is_connected():
                connection.rollback()
                self.logger.warning(f"Transaction rolled back due to error: {e}")
            raise QueryError(f"Transaction failed: {e}")
            
        finally:
            if connection and connection.is_connected():
                connection.close()
            self._current_conn = None
    
    def begin(self) -> None:
        if self._current_conn:
            self._current_conn.start_transaction()
            self.logger.debug("Manual transaction started")
    
    def commit(self) -> None:
        if self._current_conn:
            self._current_conn.commit()
            self.logger.debug("Manual transaction committed")
    
    def rollback(self) -> None:
        if self._current_conn:
            self._current_conn.rollback()
            self.logger.debug("Manual transaction rolled back")

