CREATE_DATABASE_QUERY = """
CREATE DATABASE IF NOT EXISTS {database_name}
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
"""

CREATE_ROOMS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS rooms (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_rooms_name (name)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

CREATE_STUDENTS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    sex ENUM('M', 'F') NOT NULL,
    room_id INT NULL,
    age_years INT GENERATED ALWAYS AS (
        TIMESTAMPDIFF(YEAR, birthday, CURDATE())
    ) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_students_name (name),
    INDEX idx_students_birthday (birthday),
    INDEX idx_students_sex (sex),
    INDEX idx_students_room_id (room_id),
    INDEX idx_students_age (age_years),
    INDEX idx_students_room_sex (room_id, sex),
    INDEX idx_students_room_age (room_id, age_years),
    
    CONSTRAINT fk_students_room 
        FOREIGN KEY (room_id) REFERENCES rooms(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

DROP_STUDENTS_TABLE_QUERY = "DROP TABLE IF EXISTS students;"
DROP_ROOMS_TABLE_QUERY = "DROP TABLE IF EXISTS rooms;"

TABLE_EXISTS_QUERY = """
SELECT COUNT(*) as table_count
FROM information_schema.tables 
WHERE table_schema = %s AND table_name = %s;
"""

OPTIMIZATION_INDEXES = [
    """
    CREATE INDEX IF NOT EXISTS idx_students_composite_analytics 
    ON students (room_id, sex, age_years, birthday);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_students_age_range 
    ON students (age_years, room_id);
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_rooms_students_count 
    ON students (room_id) USING BTREE;
    """
]

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




