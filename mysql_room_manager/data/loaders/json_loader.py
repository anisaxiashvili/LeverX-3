import json
import logging
from pathlib import Path
from typing import List, Dict, Any

from ...interfaces.loader_interface import LoaderInterface
from ...exceptions.exceptions import ImportError, ValidationError
from ...utils.validation import validate_file_path, validate_students_data, validate_rooms_data


class JsonLoader(LoaderInterface): 
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_students(self, file_path: str) -> List[Dict[str, Any]]:
        """Load students data from JSON file."""
        validate_file_path(file_path)
        
        try:
            self.logger.info(f"Loading students from: {file_path}")
            
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise ImportError(f"Students file not found: {file_path}", file_path)
            
            with open(file_path_obj, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            validate_students_data(data)
            self.logger.info(f"Successfully loaded {len(data)} students")
            return data
            
        except json.JSONDecodeError as e:
            raise ImportError(f"Invalid JSON format in students file: {e}", file_path)
        except ValidationError:
            raise
        except Exception as e:
            raise ImportError(f"Failed to load students data: {e}", file_path)
    
    def load_rooms(self, file_path: str) -> List[Dict[str, Any]]:
        validate_file_path(file_path)
        
        try:
            self.logger.info(f"Loading rooms from: {file_path}")
            
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise ImportError(f"Rooms file not found: {file_path}", file_path)
            
            with open(file_path_obj, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            validate_rooms_data(data)
            self.logger.info(f"Successfully loaded {len(data)} rooms")
            return data
            
        except json.JSONDecodeError as e:
            raise ImportError(f"Invalid JSON format in rooms file: {e}", file_path)
        except ValidationError:
            raise
        except Exception as e:
            raise ImportError(f"Failed to load rooms data: {e}", file_path)

