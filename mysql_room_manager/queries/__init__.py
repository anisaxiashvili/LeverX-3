"""SQL queries for MySQL Student Room Manager."""

from .schema_queries import *
from .analytics_queries import *
from .optimization_queries import *

__all__ = [
    'CREATE_DATABASE_QUERY',
    'CREATE_ROOMS_TABLE_QUERY', 
    'CREATE_STUDENTS_TABLE_QUERY',
    'ROOMS_WITH_STUDENT_COUNT_QUERY',
    'TOP_ROOMS_BY_AVG_AGE_QUERY',
    'TOP_ROOMS_BY_AGE_DIFFERENCE_QUERY',
    'MIXED_GENDER_ROOMS_QUERY',
    'TABLE_SIZE_ANALYSIS_QUERY'
]

