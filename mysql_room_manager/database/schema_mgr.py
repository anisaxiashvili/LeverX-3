import logging
from typing import List
from ..interfaces.db_interface import SchemaInterface
from ..database.conn_manager import ConnManager
from ..queries.schema_queries import *
from ..config.db_config import DbConfig
from ..exceptions.exceptions import SchemaError


class SchemaMgr(SchemaInterface):  
    
    def __init__(self, conn_manager: ConnManager):
        self.conn_manager = conn_manager  
        self.logger = logging.getLogger(__name__)
        self.db_name = conn_manager.config.database  
    
    def create_db(self) -> None:
        try:
            self.logger.info(f"Creating database: {self.db_name}")

            config = self.conn_manager.config
            temp_config = DbConfig(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                database="",
                charset=config.charset
            )
            temp_manager = ConnManager(temp_config)
            
            with temp_manager.get_conn() as conn:
                cursor = conn.cursor()
                query = CREATE_DATABASE_QUERY.format(database_name=self.db_name)
                cursor.execute(query)
                conn.commit()
                cursor.close()
            
            self.logger.info(f"Database {self.db_name} created successfully")
            
        except Exception as e:
            error_msg = f"Failed to create database {self.db_name}: {e}"
            self.logger.error(error_msg)
            raise SchemaError(error_msg)
    
    def create_tables(self) -> None:
        try:
            self.logger.info("Creating database tables")
            
            with self.conn_manager.get_conn() as conn:
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
            raise SchemaError(error_msg)
    
    def drop_tables(self) -> None:
        try:
            self.logger.info("Dropping database tables")
            
            with self.conn_manager.get_conn() as conn:
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
            raise SchemaError(error_msg)
    
    def create_indexes(self) -> None:
        try:
            self.logger.info("Creating optimization indexes")
            
            with self.conn_manager.get_conn() as conn:
                cursor = conn.cursor()
                
                for i, index_query in enumerate(OPTIMIZATION_INDEXES):
                    try:
                        cursor.execute(index_query)
                        self.logger.debug(f"Created optimization index {i+1}")
                    except Exception as e:
                        self.logger.warning(f"Index creation warning: {e}")
                
                conn.commit()
                cursor.close()
            
            self.logger.info("Optimization indexes created successfully")
            
        except Exception as e:
            error_msg = f"Failed to create indexes: {e}"
            self.logger.error(error_msg)
            raise SchemaError(error_msg)
    
    def table_exists(self, table_name: str) -> bool:
        try:
            with self.conn_manager.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(TABLE_EXISTS_QUERY, (self.db_name, table_name))
                result = cursor.fetchone()
                cursor.close()
                return result[0] > 0
                
        except Exception as e:
            self.logger.error(f"Failed to check table existence: {e}")
            return False
    
    def get_table_info(self) -> List[dict]:
        try:
            with self.conn_manager.get_conn() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(TABLE_SIZE_ANALYSIS_QUERY, (self.db_name,))
                results = cursor.fetchall()
                cursor.close()
                return results
                
        except Exception as e:
            self.logger.error(f"Failed to get table info: {e}")
            return []

