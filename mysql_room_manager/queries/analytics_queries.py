ROOMS_WITH_STUDENT_COUNT_QUERY = """
SELECT 
    r.id as room_id,
    r.name as room_name,
    COALESCE(student_counts.student_count, 0) as student_count
FROM rooms r
LEFT JOIN (
    SELECT 
        room_id,
        COUNT(*) as student_count
    FROM students 
    WHERE room_id IS NOT NULL
    GROUP BY room_id
) student_counts ON r.id = student_counts.room_id
ORDER BY student_count DESC, r.id;
"""

TOP_ROOMS_BY_AVG_AGE_QUERY = """
SELECT 
    r.id as room_id,
    r.name as room_name,
    AVG(s.age_years) as average_age,
    COUNT(s.id) as student_count
FROM rooms r
INNER JOIN students s ON r.id = s.room_id
GROUP BY r.id, r.name
HAVING student_count > 0
ORDER BY average_age ASC, student_count DESC
LIMIT %s;
"""

TOP_ROOMS_BY_AGE_DIFFERENCE_QUERY = """
SELECT 
    r.id as room_id,
    r.name as room_name,
    (MAX(s.age_years) - MIN(s.age_years)) as age_difference,
    MIN(s.age_years) as min_age,
    MAX(s.age_years) as max_age,
    COUNT(s.id) as student_count
FROM rooms r
INNER JOIN students s ON r.id = s.room_id
GROUP BY r.id, r.name
HAVING student_count > 1
ORDER BY age_difference DESC, student_count DESC
LIMIT %s;
"""

MIXED_GENDER_ROOMS_QUERY = """
SELECT 
    r.id as room_id,
    r.name as room_name,
    gender_stats.male_count,
    gender_stats.female_count,
    gender_stats.total_students
FROM rooms r
INNER JOIN (
    SELECT 
        room_id,
        SUM(CASE WHEN sex = 'M' THEN 1 ELSE 0 END) as male_count,
        SUM(CASE WHEN sex = 'F' THEN 1 ELSE 0 END) as female_count,
        COUNT(*) as total_students
    FROM students 
    WHERE room_id IS NOT NULL
    GROUP BY room_id
    HAVING male_count > 0 AND female_count > 0
) gender_stats ON r.id = gender_stats.room_id
ORDER BY gender_stats.total_students DESC, r.id;
"""

PERFORMANCE_TEST_QUERIES = {
    'room_utilization': """
    SELECT 
        COUNT(DISTINCT room_id) as occupied_rooms,
        COUNT(DISTINCT CASE WHEN room_id IS NULL THEN id END) as unassigned_students,
        AVG(room_student_count) as avg_students_per_room
    FROM (
        SELECT room_id, COUNT(*) as room_student_count
        FROM students 
        WHERE room_id IS NOT NULL
        GROUP BY room_id
    ) room_stats;
    """,
    
    'age_distribution': """
    SELECT 
        CASE 
            WHEN age_years < 18 THEN 'Under 18'
            WHEN age_years BETWEEN 18 AND 25 THEN '18-25'
            WHEN age_years BETWEEN 26 AND 35 THEN '26-35'
            ELSE 'Over 35'
        END as age_group,
        COUNT(*) as student_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students), 2) as percentage
    FROM students
    GROUP BY age_group
    ORDER BY MIN(age_years);
    """,
    
    'gender_distribution_by_room': """
    SELECT 
        r.name as room_name,
        COUNT(CASE WHEN s.sex = 'M' THEN 1 END) as male_count,
        COUNT(CASE WHEN s.sex = 'F' THEN 1 END) as female_count,
        COUNT(s.id) as total_students,
        ROUND(COUNT(CASE WHEN s.sex = 'M' THEN 1 END) * 100.0 / COUNT(s.id), 2) as male_percentage
    FROM rooms r
    LEFT JOIN students s ON r.id = s.room_id
    WHERE s.id IS NOT NULL
    GROUP BY r.id, r.name
    ORDER BY total_students DESC;
    """
}