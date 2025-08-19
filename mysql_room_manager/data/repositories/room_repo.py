"""Room repository for database operations."""
import logging
from typing import List, Dict, Any, Optional

from ...interfaces.repo_interface import RoomRepoInterface
from ...database.conn_manager import ConnManager
from ...database.tx_manager import TxManager
from ...models.room import Room
from ...exceptions.exceptions import QueryError


class RoomRepo(RoomRepoInterface): 
    
    def __init__(self, conn_manager: ConnManager):
        self.conn_manager = conn_manager  
        self.tx_manager = TxManager(conn_manager)
        self.logger = logging.getLogger(__name__)
    
    def insert_rooms(self, rooms: List[Dict[str, Any]]) -> int:
        if not rooms:
            return 0
        
        try:
            self.logger.info(f"Inserting {len(rooms)} rooms")
            
            room_models = [Room.from_dict(room_data) for room_data in rooms]
            
            room_tuples = [room.to_db_tuple() for room in room_models]
            
            with self.tx_manager.transaction() as conn:
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
            raise QueryError(error_msg)
    
    def get_room_by_id(self, room_id: int) -> Optional[Dict[str, Any]]:
        try:
            with self.conn_manager.get_conn() as conn:
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
            with self.conn_manager.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM rooms")
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else 0
                
        except Exception as e:
            self.logger.error(f"Failed to count rooms: {e}")
            return 0