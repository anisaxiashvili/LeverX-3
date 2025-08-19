"""Application constants."""

class Commands:
    IMPORT = 'import'
    ANALYTICS = 'analytics'
    OPTIMIZE = 'optimize'
    DATABASE = 'database'

class AnalyticsOpts:
    REPORT = 'report'
    ROOM_COUNTS = 'room_counts'
    YOUNGEST_ROOMS = 'youngest_rooms'
    AGE_GAPS = 'age_gaps'
    MIXED_GENDER = 'mixed_gender'

class DbOps:
    INIT = 'init'
    DROP = 'drop'
    STATUS = 'status'

class OptOps:
    ANALYZE = 'analyze'
    RECOMMENDATIONS = 'recommendations'

class Formats:
    JSON = 'json'
    XML = 'xml'

class Tables:
    ROOMS = 'rooms'
    STUDENTS = 'students'

