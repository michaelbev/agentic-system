# Database Agent Examples

This directory contains examples demonstrating database operations and management using intelligent orchestration.

## Files

- **`database_orchestration_example.py`** - Main orchestration example showing database operation workflows

## Features Demonstrated

- Database querying and analysis
- Energy consumption pattern analysis
- Database maintenance and optimization
- Data migration workflows

## Running the Example

```bash
# From the project root
python examples/database/database_orchestration_example.py
```

## Prerequisites

1. Database must be running with energy data
2. Database admin agent must be started: `python start_agents.py DB_ADMIN_ENERGY`
3. Environment variables configured in `.env`

## Expected Output

The example will demonstrate:
- Complex database queries
- Data analysis and reporting
- Database maintenance tasks
- Multi-step data operations

## Documentation

For detailed information about the database agent, see [DATABASE_ORCHESTRATION.md](../../docs/agents/DATABASE_ORCHESTRATION.md). 