# Examples Directory

This directory contains practical examples demonstrating how to use the intelligent orchestration system for the Energy as a Service Platform.

## Structure

- **`pdf/`** - PDF processing and document analysis examples  
- **`database/`** - Database operations and energy data management examples

## Quick Start

Each example directory contains:
- Orchestration examples showing intelligent agent coordination
- Energy-specific use cases and workflows
- Error handling and best practices

## Running Examples

```bash
# PDF processing examples
python examples/pdf/pdf_orchestration_example.py

# Database operations examples
python examples/database/database_orchestration_example.py
```

## Prerequisites

1. Ensure the energy database is running and configured
2. Set up environment variables in `.env`
3. Install dependencies: `pip install -r requirements.txt`
4. Start required agents: `python start_agents.py [agent_name]`

## Documentation

For detailed documentation on each agent type, see:
- [PDF Agent Documentation](../docs/agents/PDF_ORCHESTRATION.md)
- [Database Agent Documentation](../docs/agents/DATABASE_ORCHESTRATION.md) 