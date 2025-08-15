import logging
from typing import List, Dict, Any, Optional

from ...interfaces.repository_interface import StudentRepositoryInterface
from ...database.connection_manager import ConnectionManager
from ...database.transaction_manager import TransactionManager
from ...models.student import Student
from ...exceptions.custom_exceptions import QueryExecutionError
from ...utils.date_utils import datetime_to_mysql_string


class StudentRepository(StudentRepositoryInterface):
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.transaction_manager = TransactionManager(connection_manager)
        self.logger = logging.getLogger(__name__)
    
    def insert_students(self, students: List[Dict[str, Any]]) -> int:
        if not students:
            return 0
        
        try:
            self.logger.info(f"Inserting {len(students)} students")
            
            student_models = [Student.from_dict(student_data) for student_data in students]

            student_tuples = []
            for student in student_models:
                student_tuples.append((
                    student.id,
                    student.name,
                    datetime_to_mysql_string(student.birthday),
                    student.sex,
                    student.room
                ))
            
            with self.transaction_manager.transaction() as conn:
                cursor = conn.cursor()
                
                insert_query = """
                INSERT INTO students (id, name, birthday, sex, room_id) 
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    name = VALUES(name),
                    birthday = VALUES(birthday),
                    sex = VALUES(sex),
                    room_id = VALUES(room_id)
                """
                
                cursor.executemany(insert_query, student_tuples)
                affected_rows = cursor.rowcount
                cursor.close()
            
            self.logger.info(f"Successfully inserted {affected_rows} students")
            return affected_rows
            
        except Exception as e:
            error_msg = f"Failed to insert students: {e}"
            self.logger.error(error_msg)
            raise QueryExecutionError(error_msg)
    
    def get_student_by_id(self, student_id: int) -> Optional[Dict[str, Any]]:
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT id, name, birthday, sex, room_id, age_years FROM students WHERE id = %s", 
                    (student_id,)
                )
                result = cursor.fetchone()
                cursor.close()
                return result
                
        except Exception as e:
            self.logger.error(f"Failed to get student {student_id}: {e}")
            return None
    
    def get_students_by_room(self, room_id: int) -> List[Dict[str, Any]]:
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    "SELECT id, name, birthday, sex, room_id, age_years FROM students WHERE room_id = %s", 
                    (room_id,)
                )
                results = cursor.fetchall()
                cursor.close()
                return results
                
        except Exception as e:
            self.logger.error(f"Failed to get students for room {room_id}: {e}")
            return []
    
    def count_students(self) -> int:
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM students")
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else 0
                
        except Exception as e:
            self.logger.error(f"Failed to count students: {e}")
            return 0