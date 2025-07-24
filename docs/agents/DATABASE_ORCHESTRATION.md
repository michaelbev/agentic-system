# Database Operations with Intelligent Orchestration

## Overview

The database admin agent has been integrated with the intelligent orchestration system, enabling sophisticated database management and query workflows using PostgreSQL.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Intelligent Orchestration                │
├─────────────────────────────────────────────────────────────┤
│  User Request → Pattern Matching → Workflow Planning →     │
│  Agent Coordination → MCP Communication → Results           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP Agents                              │
├─────────────────┬─────────────────┬─────────────────────────┤
│  DB Admin Agent │   Time Agent    │   Other Agents         │
│   (MCP Server)  │   (MCP Server)  │   (MCP Servers)        │
├─────────────────┼─────────────────┼─────────────────────────┤
│ • query         │ • get_current_  │ • textract             │
│ • insert        │   time          │ • summarize            │
│ • update        │ • convert_time  │ • energy               │
│ • delete        │                 │                        │
│ • schema_info   │                 │                        │
└─────────────────┴─────────────────┴─────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer                           │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL Database with Multiple Schemas                 │
└─────────────────────────────────────────────────────────────┘
```

## Features

### ✅ **Integrated Database Operations**
- **PostgreSQL Integration**: Direct database queries and operations
- **Schema Management**: Database schema information and exploration
- **Pattern Matching**: Database workflows are automatically recognized
- **Multi-Agent Coordination**: Works with time agent and others

### ✅ **Intelligent Workflow Patterns**
- **Data Query**: `"query the database"` → `db-admin.query`
- **Data Insert**: `"insert data into database"` → `db-admin.insert`
- **Data Update**: `"update database records"` → `db-admin.update`
- **Schema Exploration**: `"show database schema"` → `db-admin.schema_info`

### ✅ **Natural Language Processing**
- **Keyword Recognition**: Automatically detects database-related requests
- **Context Understanding**: Extracts relevant parameters from requests
- **Workflow Composition**: Creates appropriate multi-step workflows

## Usage Examples

### 1. Simple Database Query
```python
from orchestration.intelligent.intelligent_orchestrator import process_user_request

result = await process_user_request(
    "query the database for user records",
    query="SELECT * FROM users WHERE active = true",
    limit=10
)
```

### 2. Data Insertion with Time Context
```python
result = await process_user_request(
    "insert a new user record with current timestamp",
    table="users",
    data={
        "name": "John Doe",
        "email": "john@example.com",
        "created_at": "{{time.current_time}}"
    }
)
```

### 3. Schema Exploration
```python
result = await process_user_request(
    "show me the database schema",
    schema="public"
)
```

### 4. Complex Data Operations
```python
result = await process_user_request(
    "update user records and get the count",
    operations=[
        {"type": "update", "table": "users", "set": {"status": "active"}, "where": "last_login > '2024-01-01'"},
        {"type": "query", "sql": "SELECT COUNT(*) FROM users WHERE status = 'active'"}
    ]
)
```

## Workflow Patterns

### Database Query Pattern
```json
{
  "goal": "query database data",
  "keywords": ["query", "select", "database", "data", "records"],
  "steps": [
    {"agent": "db-admin", "tool": "query"}
  ]
}
```

### Data Insertion Pattern
```json
{
  "goal": "insert data into database",
  "keywords": ["insert", "add", "create", "database", "record"],
  "steps": [
    {"agent": "time", "tool": "get_current_time"},
    {"agent": "db-admin", "tool": "insert"}
  ]
}
```

### Schema Exploration Pattern
```json
{
  "goal": "explore database schema",
  "keywords": ["schema", "structure", "tables", "database", "show"],
  "steps": [
    {"agent": "db-admin", "tool": "schema_info"}
  ]
}
```

## Setup and Configuration

### 1. Environment Variables
```bash
# Database Configuration
DB_HOST_ENERGY=localhost
DB_NAME_ENERGY=your_database
DB_USER=your_user
DB_PASSWORD=your_password
DB_PORT_ENERGY=5432

# Admin Database (for setup)
DB_ADMIN_ENERGY=postgres
DB_ADMIN_ENERGY_PASSWORD=admin_password
```

### 2. Database Setup
```bash
# Run the database setup script
./scripts/setup_database.sh
```

### 3. Agent Startup
```bash
# Start individual agents
python start_agents.py db-admin
python start_agents.py time

# List all available agents
python start_agents.py --list

# Start all agents (for testing)
python start_agents.py --all
```

## Testing

### Integration Tests
```bash
# Test database operations workflow
python tests/integration/test_database_orchestration.py

# Test individual agents
python tests/integration/test_DB_ADMIN_ENERGY_agent.py
```

### Example Usage
```bash
# Run the comprehensive database example
python examples/database_orchestration_example.py
```

## Agent Tools

### DB Admin Agent Tools
- **`query`**: Execute SQL queries on the database
- **`insert`**: Insert data into database tables
- **`update`**: Update existing database records
- **`delete`**: Delete records from database tables
- **`schema_info`**: Get database schema information
- **`table_info`**: Get information about specific tables

### Time Agent Tools
- **`get_current_time`**: Get current time in a specific timezone
- **`convert_time`**: Convert time between timezones

## Benefits of Integration

### 🎯 **Intelligent Workflow Composition**
- Automatically determines which agents and tools to use
- Creates optimal workflows based on user requests
- Handles complex multi-step processes

### 🔄 **Multi-Agent Coordination**
- Coordinates between db-admin and time agents
- Manages agent lifecycle (start/stop/communication)
- Handles MCP protocol communication

### 🧠 **Pattern-Based Planning**
- Recognizes common database operation patterns
- Maps natural language to specific workflows
- Provides fallback to dynamic planning

### 📊 **Comprehensive Tool Discovery**
- Automatically discovers all available tools
- Validates tool schemas and requirements
- Provides tool documentation and examples

## Current Status

### ✅ **Working Features**
- DB admin agent MCP server integration
- Workflow pattern recognition
- Multi-agent coordination
- Tool discovery and validation
- Natural language request processing
- PostgreSQL integration
- Schema exploration capabilities

### 🔧 **Areas for Improvement**
- Query optimization and performance
- Transaction management
- Connection pooling
- Security and access control
- Backup and recovery operations

## Next Steps

1. **Performance Optimization**: Implement query optimization and connection pooling
2. **Security Enhancement**: Add role-based access control and query validation
3. **Transaction Management**: Support for complex transactions
4. **Backup Operations**: Database backup and recovery workflows
5. **Monitoring**: Database performance monitoring and alerting
6. **Documentation**: Add more examples and use cases

## Related Documentation

### **System Overview**
- **[README.md](README.md)** - Complete system architecture and technical overview
- **[MCP_LEARNING_GUIDE.md](MCP_LEARNING_GUIDE.md)** - Learn about the MCP protocol used by agents

### **Other Application Guides**
- **[ENERGY_ORCHESTRATION.md](ENERGY_ORCHESTRATION.md)** - Energy analysis workflows
- **[PDF_ORCHESTRATION.md](PDF_ORCHESTRATION.md)** - Document processing workflows

### **Quick References**
- **System Setup**: See [README.md](README.md#quick-start) for environment setup
- **Agent Management**: See [README.md](README.md#available-agents--tools) for all available agents
- **Testing**: See [README.md](README.md#testing) for comprehensive testing guide

## Conclusion

The database admin agent is fully integrated with the intelligent orchestration system, providing a sophisticated platform for database management and operations. The integration enables natural language processing, intelligent workflow composition, and multi-agent coordination, making it easy to build complex database applications.

The system is ready for production use with proper database configuration and can be extended with additional agents and workflow patterns as needed. 