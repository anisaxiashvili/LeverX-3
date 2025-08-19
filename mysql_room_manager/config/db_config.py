import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class DbConfig: 
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = ""
    database: str = "student_room_analytics"
    charset: str = "utf8mb4"
    
    pool_name: str = "student_room_pool"
    pool_size: int = 10
    pool_reset_session: bool = True
    
    connection_timeout: int = 30
    autocommit: bool = False
    
    use_ssl: bool = False
    ssl_ca: Optional[str] = None
    ssl_cert: Optional[str] = None
    ssl_key: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'DbConfig':
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '3306')),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'student_room_analytics'),
            charset=os.getenv('DB_CHARSET', 'utf8mb4'),
            pool_size=int(os.getenv('DB_POOL_SIZE', '10')),
            connection_timeout=int(os.getenv('DB_TIMEOUT', '30')),
            use_ssl=os.getenv('DB_USE_SSL', 'false').lower() == 'true',
            ssl_ca=os.getenv('DB_SSL_CA'),
            ssl_cert=os.getenv('DB_SSL_CERT'),
            ssl_key=os.getenv('DB_SSL_KEY')
        )
    
    def to_conn_dict(self) -> dict: 
        config = {
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'charset': self.charset,
            'connection_timeout': self.connection_timeout,
            'autocommit': self.autocommit,
        }
        
        if self.use_ssl:
            ssl_config = {}
            if self.ssl_ca:
                ssl_config['ca'] = self.ssl_ca
            if self.ssl_cert:
                ssl_config['cert'] = self.ssl_cert
            if self.ssl_key:
                ssl_config['key'] = self.ssl_key
            if ssl_config:
                config['ssl'] = ssl_config
        
        return config
