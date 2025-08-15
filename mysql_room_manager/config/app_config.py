"""Application configuration settings."""
from dataclasses import dataclass
from typing import List
from .database_config import DatabaseConfig


@dataclass
class AppConfig:
    APP_NAME: str = "MySQL Student Room Manager"
    APP_VERSION: str = "2.0.0"
    database: DatabaseConfig = None
    
    BATCH_SIZE: int = 1000
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0

    QUERY_TIMEOUT: int = 300
    MAX_QUERY_RESULTS: int = 10000

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = None
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    VALIDATE_INPUT_DATA: bool = True
    STRICT_VALIDATION: bool = True
    
    def __post_init__(self):
        if self.database is None:
            self.database = DatabaseConfig.from_env()

APP_CONFIG = AppConfig()
