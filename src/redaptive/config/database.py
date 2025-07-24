"""
Database configuration and connection management.
"""

import logging
from typing import Optional
from contextlib import contextmanager

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    psycopg2 = None
    RealDictCursor = None
    PSYCOPG2_AVAILABLE = False

from .settings import settings


class DatabaseConfig:
    """Database connection and configuration manager."""
    
    def __init__(self):
        self.connection = None
        self._setup_logging()
        
        if not PSYCOPG2_AVAILABLE:
            self.logger.warning("psycopg2 not available - database functionality disabled")
    
    def _setup_logging(self):
        """Setup database-specific logging."""
        self.logger = logging.getLogger("redaptive.database")
    
    def connect(self):
        """Establish database connection."""
        if not PSYCOPG2_AVAILABLE:
            raise RuntimeError("psycopg2 not available - install psycopg2-binary to enable database functionality")
            
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
        if not PSYCOPG2_AVAILABLE:
            raise RuntimeError("psycopg2 not available - install psycopg2-binary to enable database functionality")
            
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
        if not PSYCOPG2_AVAILABLE:
            self.logger.warning("Database health check failed: psycopg2 not available")
            return False
            
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception as e:
            self.logger.error(f"Database health check failed: {e}")
            return False


# Global database instance
db = DatabaseConfig()