"""
Database configuration and connection management.
"""

import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from contextlib import contextmanager

from .settings import settings


class DatabaseConfig:
    """Database connection and configuration manager."""
    
    def __init__(self):
        self.connection: Optional[psycopg2.extensions.connection] = None
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup database-specific logging."""
        self.logger = logging.getLogger("redaptive.database")
    
    def connect(self) -> psycopg2.extensions.connection:
        """Establish database connection."""
        if self.connection and not self.connection.closed:
            return self.connection
        
        try:
            self.connection = psycopg2.connect(
                host=settings.database.host,
                port=settings.database.port,
                database=settings.database.name,
                user=settings.database.user,
                password=settings.database.password
            )
            self.logger.info("Database connection established successfully")
            return self.connection
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise
    
    def disconnect(self):
        """Close database connection."""
        if self.connection and not self.connection.closed:
            self.connection.close()
            self.logger.info("Database connection closed")
    
    @contextmanager
    def get_cursor(self):
        """Get a database cursor with automatic cleanup."""
        connection = self.connect()
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            connection.commit()
        except Exception as e:
            connection.rollback()
            self.logger.error(f"Database operation failed: {e}")
            raise
        finally:
            cursor.close()
    
    def health_check(self) -> bool:
        """Check database connectivity."""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception as e:
            self.logger.error(f"Database health check failed: {e}")
            return False


# Global database instance
db = DatabaseConfig()