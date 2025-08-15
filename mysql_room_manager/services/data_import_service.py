"""Service for importing data from files to database."""
import logging
from typing import Dict, Any

from ..interfaces.repository_interface import StudentRepositoryInterface, RoomRepositoryInterface
from ..data.loaders.data_loader_factory import DataLoaderFactory
from ..database.schema_manager import SchemaManager
from ..exceptions.custom_exceptions import DataImportError


class DataImportService:
    
    def __init__(self, 
                 schema_manager: SchemaManager,
                 student_repository: StudentRepositoryInterface,
                 room_repository: RoomRepositoryInterface):
        self.schema_manager = schema_manager
        self.student_repository = student_repository
        self.room_repository = room_repository
        self.logger = logging.getLogger(__name__)
    
    def import_data(self, students_file: str, rooms_file: str, 
                   file_format: str = "json") -> Dict[str, Any]:
        try:
            self.logger.info("Starting data import process")
            
            self._initialize_schema()
            
            loader = DataLoaderFactory.create_loader(file_format)
            
            self.logger.info("Loading data from files")
            students_data = loader.load_students(students_file)
            rooms_data = loader.load_rooms(rooms_file)
            
            self.logger.info("Importing rooms data")
            rooms_inserted = self.room_repository.insert_rooms(rooms_data)
            
            self.logger.info("Importing students data")  
            students_inserted = self.student_repository.insert_students(students_data)
            
            self.schema_manager.create_indexes()
            
            results = {
                'success': True,
                'rooms_imported': rooms_inserted,
                'students_imported': students_inserted,
                'total_records': rooms_inserted + students_inserted
            }
            
            self.logger.info(f"Data import completed successfully: {results}")
            return results
            
        except Exception as e:
            error_msg = f"Data import failed: {e}"
            self.logger.error(error_msg)
            raise DataImportError(error_msg)
    
    def _initialize_schema(self) -> None:
        """Initialize database schema."""
        try:
            self.logger.info("Initializing database schema")
            
            self.schema_manager.create_database()
            
            self.schema_manager.create_tables()
            
            self.logger.info("Database schema initialized")
            
        except Exception as e:
            raise DataImportError(f"Failed to initialize schema: {e}")

