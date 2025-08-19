import logging
from typing import Dict, Any
from ..interfaces.repo_interface import StudentRepoInterface, RoomRepoInterface
from ..data.loaders.loader_factory import LoaderFactory
from ..database.schema_mgr import SchemaMgr
from ..exceptions.exceptions import ImportError


class ImportSvc:  
    
    def __init__(self, 
                 schema_mgr: SchemaMgr,
                 student_repo: StudentRepoInterface,
                 room_repo: RoomRepoInterface):
        self.schema_mgr = schema_mgr  
        self.student_repo = student_repo  
        self.room_repo = room_repo  
        self.logger = logging.getLogger(__name__)
    
    def import_data(self, students_file: str, rooms_file: str, 
                   file_format: str = "json") -> Dict[str, Any]:
        try:
            self.logger.info("Starting data import process")
            
            self._init_schema() 
            loader = LoaderFactory.create_loader(file_format)
            
            self.logger.info("Loading data from files")
            students_data = loader.load_students(students_file)
            rooms_data = loader.load_rooms(rooms_file)
            
            self.logger.info("Importing rooms data")
            rooms_inserted = self.room_repo.insert_rooms(rooms_data)
            
            self.logger.info("Importing students data")  
            students_inserted = self.student_repo.insert_students(students_data)
            
            self.schema_mgr.create_indexes()
            
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
            raise ImportError(error_msg)
    
    def _init_schema(self) -> None:
        try:
            self.logger.info("Initializing db schema")
            
            self.schema_mgr.create_db()
            
            self.schema_mgr.create_tables()
            
            self.logger.info("Db schema initialized")
            
        except Exception as e:
            raise ImportError(f"Failed to initialize schema: {e}")

