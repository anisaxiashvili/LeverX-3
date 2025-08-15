__version__ = "2.0.0"
__author__ = "MySQL Student Room Analytics Team"
__description__ = "Enterprise MySQL solution for student-room analytics with query optimization"

# Main API exports
from .services.data_import_service import DataImportService
from .services.analytics_service import AnalyticsService
from .services.database_optimization_service import DatabaseOptimizationService
from .database.connection_manager import ConnectionManager
from .database.schema_manager import SchemaManager
from .cli.cli_controller import CLIController

__all__ = [
    'DataImportService',
    'AnalyticsService', 
    'DatabaseOptimizationService',
    'ConnectionManager',
    'SchemaManager',
    'CLIController',
    '__version__'
]