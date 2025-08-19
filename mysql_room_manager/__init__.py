__version__ = "2.0.0"
__author__ = "MySQL Student Room Analytics Team"
__description__ = "Enterprise MySQL solution for student-room analytics with query optimization"

from .services.import_svc import ImportSvc
from .services.analytics_svc import AnalyticsSvc
from .services.opt_svc import OptSvc
from .database.conn_manager import ConnManager
from .database.schema_mgr import SchemaMgr
from .cli.controller import Controller

__all__ = [
    'ImportSvc',      
    'AnalyticsSvc',   
    'OptSvc',         
    'ConnManager',    
    'SchemaMgr',      
    'Controller',     
    '__version__'
]