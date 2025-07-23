#!/usr/bin/env python3
"""
MCP Database Admin Agent
Provides database administration tools using PostgreSQL and MCP protocol
"""

import asyncio
import logging
import json
import os
from typing import Dict, Any, Optional, List
import sys

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

from .base_mcp_server import BaseMCPServer

class DatabaseAdminAgent(BaseMCPServer):
    def __init__(self):
        super().__init__("db-admin-agent", "1.0.0")
        self.connection = None
        self.setup_database()
        self.setup_tools()
        
    def setup_database(self):
        """Setup database connection"""
        try:
            # Get database connection parameters from environment
            db_host = os.getenv('DB_HOST', 'localhost')
            db_port = os.getenv('DB_PORT', '5432')
            db_name = os.getenv('DB_NAME', 'energy_db')
            db_user = os.getenv('DB_ENERGYAPP_USER', 'energy_user')
            db_password = os.getenv('DB_ENERGYAPP_PASSWORD', '')
            
            # Create connection
            self.connection = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password
            )
            logging.info("Database connection established successfully")
        except Exception as e:
            logging.error(f"Failed to connect to database: {e}")
    
    def setup_tools(self):
        """Register database administration tools"""
        self.register_tool(
            "list_tables",
            "List all tables in the database",
            self.list_tables,
            {
                "type": "object",
                "properties": {
                    "schema": {
                        "type": "string",
                        "description": "Schema name to list tables from",
                        "default": "public"
                    }
                },
                "required": []
            }
        )
        
        self.register_tool(
            "describe_table",
            "Describe table structure and columns",
            self.describe_table,
            {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table to describe"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema name",
                        "default": "public"
                    }
                },
                "required": ["table_name"]
            }
        )
        
        self.register_tool(
            "execute_query",
            "Execute a SQL query and return results",
            self.execute_query,
            {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of rows to return",
                        "default": 100
                    }
                },
                "required": ["query"]
            }
        )
        
        self.register_tool(
            "get_table_info",
            "Get detailed information about a table",
            self.get_table_info,
            {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema name",
                        "default": "public"
                    }
                },
                "required": ["table_name"]
            }
        )
        
        self.register_tool(
            "list_schemas",
            "List all schemas in the database",
            self.list_schemas,
            {
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        
        self.register_tool(
            "get_database_stats",
            "Get database statistics and information",
            self.get_database_stats,
            {
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    
    async def list_tables(self, schema: str = "public"):
        """List all tables in the specified schema"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT 
                    table_name,
                    table_type
                FROM information_schema.tables 
                WHERE table_schema = %s
                ORDER BY table_name
                """
                cursor.execute(query, (schema,))
                tables = cursor.fetchall()
                
                return {
                    "schema": schema,
                    "tables": [dict(table) for table in tables],
                    "count": len(tables)
                }
        except Exception as e:
            return {"error": f"Failed to list tables: {str(e)}"}
    
    async def describe_table(self, table_name: str, schema: str = "public"):
        """Describe table structure and columns"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get column information
                column_query = """
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default,
                    character_maximum_length,
                    numeric_precision,
                    numeric_scale
                FROM information_schema.columns 
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position
                """
                cursor.execute(column_query, (schema, table_name))
                columns = cursor.fetchall()
                
                # Get primary key information
                pk_query = """
                SELECT 
                    kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                WHERE tc.constraint_type = 'PRIMARY KEY' 
                    AND tc.table_schema = %s 
                    AND tc.table_name = %s
                """
                cursor.execute(pk_query, (schema, table_name))
                primary_keys = [row['column_name'] for row in cursor.fetchall()]
                
                # Get foreign key information
                fk_query = """
                SELECT 
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu 
                    ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                    AND tc.table_schema = %s 
                    AND tc.table_name = %s
                """
                cursor.execute(fk_query, (schema, table_name))
                foreign_keys = cursor.fetchall()
                
                return {
                    "table_name": table_name,
                    "schema": schema,
                    "columns": [dict(col) for col in columns],
                    "primary_keys": primary_keys,
                    "foreign_keys": [dict(fk) for fk in foreign_keys],
                    "column_count": len(columns)
                }
        except Exception as e:
            return {"error": f"Failed to describe table: {str(e)}"}
    
    async def execute_query(self, query: str, limit: int = 100):
        """Execute a SQL query and return results"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Add LIMIT if not present and query is SELECT
                if query.strip().upper().startswith('SELECT') and 'LIMIT' not in query.upper():
                    query += f" LIMIT {limit}"
                
                cursor.execute(query)
                
                if query.strip().upper().startswith('SELECT'):
                    results = cursor.fetchall()
                    return {
                        "query": query,
                        "results": [dict(row) for row in results],
                        "row_count": len(results),
                        "columns": [desc[0] for desc in cursor.description] if cursor.description else []
                    }
                else:
                    self.connection.commit()
                    return {
                        "query": query,
                        "message": "Query executed successfully",
                        "affected_rows": cursor.rowcount
                    }
        except Exception as e:
            return {"error": f"Failed to execute query: {str(e)}"}
    
    async def get_table_info(self, table_name: str, schema: str = "public"):
        """Get detailed information about a table"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get row count
                count_query = sql.SQL("SELECT COUNT(*) as row_count FROM {}.{}").format(
                    sql.Identifier(schema),
                    sql.Identifier(table_name)
                )
                cursor.execute(count_query)
                row_count = cursor.fetchone()['row_count']
                
                # Get table size
                size_query = """
                SELECT 
                    pg_size_pretty(pg_total_relation_size(%s)) as table_size,
                    pg_size_pretty(pg_relation_size(%s)) as data_size
                """
                full_table_name = f"{schema}.{table_name}"
                cursor.execute(size_query, (full_table_name, full_table_name))
                size_info = cursor.fetchone()
                
                # Get sample data
                sample_query = sql.SQL("SELECT * FROM {}.{} LIMIT 5").format(
                    sql.Identifier(schema),
                    sql.Identifier(table_name)
                )
                cursor.execute(sample_query)
                sample_data = cursor.fetchall()
                
                return {
                    "table_name": table_name,
                    "schema": schema,
                    "row_count": row_count,
                    "table_size": size_info['table_size'],
                    "data_size": size_info['data_size'],
                    "sample_data": [dict(row) for row in sample_data]
                }
        except Exception as e:
            return {"error": f"Failed to get table info: {str(e)}"}
    
    async def list_schemas(self):
        """List all schemas in the database"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT 
                    schema_name,
                    schema_owner
                FROM information_schema.schemata
                WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
                ORDER BY schema_name
                """
                cursor.execute(query)
                schemas = cursor.fetchall()
                
                return {
                    "schemas": [dict(schema) for schema in schemas],
                    "count": len(schemas)
                }
        except Exception as e:
            return {"error": f"Failed to list schemas: {str(e)}"}
    
    async def get_database_stats(self):
        """Get database statistics and information"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get database name and size
                db_query = """
                SELECT 
                    current_database() as database_name,
                    pg_size_pretty(pg_database_size(current_database())) as database_size
                """
                cursor.execute(db_query)
                db_info = cursor.fetchone()
                
                # Get table count
                table_query = """
                SELECT COUNT(*) as table_count
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                """
                cursor.execute(table_query)
                table_count = cursor.fetchone()['table_count']
                
                # Get connection info
                cursor.execute("SELECT version() as version")
                version = cursor.fetchone()['version']
                
                return {
                    "database_name": db_info['database_name'],
                    "database_size": db_info['database_size'],
                    "table_count": table_count,
                    "version": version,
                    "connection_status": "connected"
                }
        except Exception as e:
            return {"error": f"Failed to get database stats: {str(e)}"}

async def main():
    """Start the Database Admin Agent"""
    logging.basicConfig(stream=sys.stderr)
    
    agent = DatabaseAdminAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main()) 