"""Database connection management."""
import mysql.connector
from mysql.connector import pooling
import logging
from contextlib import contextmanager
from typing import Optional, Any

from ..interfaces.database_interface import DatabaseConnectionInterface
from ..config.database_config import DatabaseConfig
from ..exceptions.custom_exceptions import DatabaseConnectionError


class ConnectionManager(DatabaseConnectionInterface):
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._pool: Optional[pooling.MySQLConnectionPool] = None
        self._connection: Optional[mysql.connector.MySQLConnection] = None
    
    def connect(self) -> Any:
        try:
            if self._pool is None:
                self.logger.info(f"Creating connection pool to {self.config.host}:{self.config.port}")
                
                pool_config = self.config.to_connection_dict()
                pool_config.update({
                    'pool_name': self.config.pool_name,
                    'pool_size': self.config.pool_size,
                    'pool_reset_session': self.config.pool_reset_session
                })
                
                self._pool = pooling.MySQLConnectionPool(**pool_config)
                self.logger.info("Connection pool created successfully")
            
            return self._pool.get_connection()
            
        except mysql.connector.Error as e:
            error_msg = f"Failed to connect to MySQL database: {e}"
            self.logger.error(error_msg)
            raise DatabaseConnectionError(
                error_msg, 
                self.config.host, 
                self.config.database
            )
    
    def disconnect(self) -> None:
        try:
            if self._connection and self._connection.is_connected():
                self._connection.close()
                self._connection = None
            
            self._pool = None
            self.logger.info("Database connection closed")
            
        except Exception as e:
            self.logger.error(f"Error closing database connection: {e}")
    
    def is_connected(self) -> bool:
        return self._pool is not None
    
    @contextmanager
    def get_connection(self):
        connection = None
        try:
            connection = self.connect()
            self.logger.debug("Database connection acquired from pool")
            yield connection
            
        except Exception as e:
            self.logger.error(f"Database connection error: {e}")
            if connection and connection.is_connected():
                connection.rollback()
            raise
            
        finally:
            if connection and connection.is_connected():
                connection.close()
                self.logger.debug("Database connection returned to pool")
    
    def test_connection(self) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                return result[0] == 1
                
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
