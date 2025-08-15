"""JSON data loader implementation."""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

from ...interfaces.data_loader_interface import DataLoaderInterface
from ...exceptions.custom_exceptions import DataImportError, ValidationError
from ...utils.validation import validate_file_path, validate_students_data, validate_rooms_data


class JSONDataLoader(DataLoaderInterface):
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_students(self, file_path: str) -> List[Dict[str, Any]]:
        validate_file_path(file_path)
        
        try:
            self.logger.info(f"Loading students from: {file_path}")
            
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise DataImportError(f"Students file not found: {file_path}", file_path)
            
            with open(file_path_obj, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            validate_students_data(data)
            self.logger.info(f"Successfully loaded {len(data)} students")
            return data
            
        except json.JSONDecodeError as e:
            raise DataImportError(f"Invalid JSON format in students file: {e}", file_path)
        except ValidationError:
            raise
        except Exception as e:
            raise DataImportError(f"Failed to load students data: {e}", file_path)
    
    def load_rooms(self, file_path: str) -> List[Dict[str, Any]]:
        validate_file_path(file_path)
        
        try:
            self.logger.info(f"Loading rooms from: {file_path}")
            
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise DataImportError(f"Rooms file not found: {file_path}", file_path)
            
            with open(file_path_obj, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            validate_rooms_data(data)
            self.logger.info(f"Successfully loaded {len(data)} rooms")
            return data
            
        except json.JSONDecodeError as e:
            raise DataImportError(f"Invalid JSON format in rooms file: {e}", file_path)
        except ValidationError:
            raise
        except Exception as e:
            raise DataImportError(f"Failed to load rooms data: {e}", file_path)

