class StudentRoomError(Exception):
    pass


class DbConnError(StudentRoomError):
    
    def __init__(self, message: str, host: str = None, database: str = None):
        self.host = host
        self.database = database
        super().__init__(message)


class SchemaError(StudentRoomError): 
    pass


class ImportError(StudentRoomError): 
    
    def __init__(self, message: str, file_path: str = None, record_count: int = None):
        self.file_path = file_path
        self.record_count = record_count
        super().__init__(message)


class QueryError(StudentRoomError):  
    
    def __init__(self, message: str, query: str = None, params: tuple = None):
        self.query = query
        self.params = params
        super().__init__(message)


class ValidationError(StudentRoomError):
    pass


class ConfigError(StudentRoomError): 
    pass


class UnsupportedFormatError(StudentRoomError):
    def __init__(self, format_name: str, supported_formats: list):
        self.format_name = format_name
        self.supported_formats = supported_formats
        message = f"Unsupported format '{format_name}'. Supported formats: {', '.join(supported_formats)}"
        super().__init__(message)
