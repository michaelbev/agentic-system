"""
Database utility tools for the Redaptive platform.
"""

import logging
from typing import Dict, List, Any, Optional
from contextlib import contextmanager
from redaptive.config.database import db

logger = logging.getLogger(__name__)

class DatabaseTool:
    """Utility class for common database operations."""
    
    @staticmethod
    @contextmanager
    def get_cursor():
        """Get a database cursor with automatic cleanup."""
        with db.get_cursor() as cursor:
            yield cursor
    
    @staticmethod
    def health_check() -> Dict[str, Any]:
        """Perform database health check."""
        try:
            is_healthy = db.health_check()
            return {
                "status": "healthy" if is_healthy else "unhealthy",
                "database": "energy_db",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "database": "energy_db",
                "timestamp": "2024-01-01T00:00:00Z"
            }
    
    @staticmethod
    def execute_query(query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute a database query and return results."""
        try:
            with DatabaseTool.get_cursor() as cursor:
                cursor.execute(query, params or ())
                if cursor.description:
                    return [dict(row) for row in cursor.fetchall()]
                return []
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    @staticmethod
    def get_table_info(table_name: str) -> Dict[str, Any]:
        """Get information about a database table."""
        try:
            query = """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = %s
            ORDER BY ordinal_position
            """
            columns = DatabaseTool.execute_query(query, (table_name,))
            
            count_query = f"SELECT COUNT(*) as row_count FROM {table_name}"
            count_result = DatabaseTool.execute_query(count_query)
            row_count = count_result[0]['row_count'] if count_result else 0
            
            return {
                "table_name": table_name,
                "columns": columns,
                "row_count": row_count
            }
        except Exception as e:
            logger.error(f"Failed to get table info for {table_name}: {e}")
            raise