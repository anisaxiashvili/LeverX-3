"""Room repository for database operations."""
import logging
from typing import List, Dict, Any, Optional

from ...interfaces.repository_interface import RoomRepositoryInterface
from ...database.connection_manager import ConnectionManager
from ...database.transaction_manager import TransactionManager
from ...models.room import Room
from ...exceptions.custom_exceptions import QueryExecutionError


class RoomRepository(RoomRepositoryInterface):    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.transaction_manager = TransactionManager(connection_manager)
        self.logger = logging.getLogger(__name__)
    
    def insert_rooms(self, rooms: List[Dict[str, Any]]) -> int:
        if not rooms:
            return 0
        
        try:
            self.logger.info(f"Inserting {len(rooms)} rooms")
            
            room_models = [Room.from_dict(room_data) for room_data in rooms]
            
            room_tuples = [room.to_db_tuple() for room in room_models]
            
            with self.transaction_manager.transaction() as conn:
                cursor = conn.cursor()
                
                insert_query = """
                INSERT INTO rooms (id, name) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE name = VALUES(name)
                """
                
                cursor.executemany(insert_query, room_tuples)
                affected_rows = cursor.rowcount
                cursor.close()
            
            self.logger.info(f"Successfully inserted {affected_rows} rooms")
            return affected_rows
            
        except Exception as e:
            error_msg = f"Failed to insert rooms: {e}"
            self.logger.error(error_msg)
            raise QueryExecutionError(error_msg)
    
    def get_room_by_id(self, room_id: int) -> Optional[Dict[str, Any]]:
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
                result = cursor.fetchone()
                cursor.close()
                return result
                
        except Exception as e:
            self.logger.error(f"Failed to get room {room_id}: {e}")
            return None
    
    def count_rooms(self) -> int:
        try:
            with self.connection_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM rooms")
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else 0
                
        except Exception as e:
            self.logger.error(f"Failed to count rooms: {e}")
            return 0
