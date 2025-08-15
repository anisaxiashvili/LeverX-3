"""Database schema management."""
import logging
from typing import List
from ..database.connection_manager import DatabaseConfig
from ..interfaces.database_interface import DatabaseSchemaInterface
from ..database.connection_manager import ConnectionManager
from ..queries.schema_queries import *
from ..exceptions.custom_exceptions import DatabaseSchemaError


class SchemaManager(DatabaseSchemaInterface):
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.logger = logging.getLogger(__name__)
        self.database_name = connection_manager.config.database
    
    def create_database(self) -> None:
        try:
            self.logger.info(f"Creating database: {self.database_name}")
            
            config = self.connection_manager.config
            temp_config = DatabaseConfig(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                database="",
                charset=config.charset
            )
            temp_manager = ConnectionManager(temp_config)
            
            with temp_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = CREATE_DATABASE_QUERY.format(database_name=self.database_name)
                cursor.execute(query)
                conn.commit()
                cursor.close()
            
            self.logger.info(f"Database {self.database_name} created successfully")
            
        except Exception as e:
            error_msg = f"Failed to create database {self.database_name}: {e}"
            self.logger.error(error_msg)
            raise DatabaseSchemaError(error_msg)
    
    def create_tables(self) -> None:
        """Create all required tables with proper relationships."""
        try:
            self.logger.info("Creating database tables")
            
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                tables = [
                    ("rooms", CREATE_ROOMS_TABLE_QUERY),
                    ("students", CREATE_STUDENTS_TABLE_QUERY)
                ]
                
                for table_name, query in tables:
                    self.logger.debug(f"Creating table: {table_name}")
                    cursor.execute(query)
                    self.logger.info(f"Table {table_name} created successfully")
                
                conn.commit()
                cursor.close()
            
            self.logger.info("All tables created successfully")
            
        except Exception as e:
            error_msg = f"Failed to create tables: {e}"
            self.logger.error(error_msg)
            raise DatabaseSchemaError(error_msg)
    
    def drop_tables(self) -> None:
        try:
            self.logger.info("Dropping database tables")
            
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor()
                drop_queries = [
                    DROP_STUDENTS_TABLE_QUERY,
                    DROP_ROOMS_TABLE_QUERY
                ]
                
                for query in drop_queries:
                    cursor.execute(query)
                
                conn.commit()
                cursor.close()
            
            self.logger.info("All tables dropped successfully")
            
        except Exception as e:
            error_msg = f"Failed to drop tables: {e}"
            self.logger.error(error_msg)
            raise DatabaseSchemaError(error_msg)
    
    def create_indexes(self) -> None:
        try:
            self.logger.info("Creating optimization indexes")
            
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                for i, index_query in enumerate(OPTIMIZATION_INDEXES):
                    try:
                        cursor.execute(index_query)
                        self.logger.debug(f"Created optimization index {i+1}")
                    except Exception as e:
                        # Log warning but continue - index might already exist
                        self.logger.warning(f"Index creation warning: {e}")
                
                conn.commit()
                cursor.close()
            
            self.logger.info("Optimization indexes created successfully")
            
        except Exception as e:
            error_msg = f"Failed to create indexes: {e}"
            self.logger.error(error_msg)
            raise DatabaseSchemaError(error_msg)
    
    def table_exists(self, table_name: str) -> bool:
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(TABLE_EXISTS_QUERY, (self.database_name, table_name))
                result = cursor.fetchone()
                cursor.close()
                return result[0] > 0
                
        except Exception as e:
            self.logger.error(f"Failed to check table existence: {e}")
            return False
    
    def get_table_info(self) -> List[dict]:
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(TABLE_SIZE_ANALYSIS_QUERY, (self.database_name,))
                results = cursor.fetchall()
                cursor.close()
                return results
                
        except Exception as e:
            self.logger.error(f"Failed to get table info: {e}")
            return []

