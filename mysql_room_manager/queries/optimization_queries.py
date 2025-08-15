TABLE_SIZE_ANALYSIS_QUERY = """
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) as table_size_mb,
    ROUND((data_length / 1024 / 1024), 2) as data_size_mb,
    ROUND((index_length / 1024 / 1024), 2) as index_size_mb,
    table_rows
FROM information_schema.tables 
WHERE table_schema = %s
ORDER BY table_size_mb DESC;
"""

INDEX_USAGE_ANALYSIS_QUERY = """
SELECT 
    table_name,
    index_name,
    column_name,
    cardinality,
    CASE 
        WHEN non_unique = 0 THEN 'UNIQUE'
        ELSE 'NON-UNIQUE'
    END as index_type
FROM information_schema.statistics 
WHERE table_schema = %s
ORDER BY table_name, index_name;
"""

EXPLAIN_QUERY_TEMPLATE = "EXPLAIN FORMAT=JSON {query}"

SLOW_QUERY_ANALYSIS = """
SELECT 
    sql_text,
    exec_count,
    avg_timer_wait/1000000000000 as avg_exec_time_sec,
    max_timer_wait/1000000000000 as max_exec_time_sec,
    sum_timer_wait/1000000000000 as total_exec_time_sec
FROM performance_schema.events_statements_summary_by_digest
WHERE schema_name = %s
ORDER BY avg_timer_wait DESC
LIMIT 10;
"""