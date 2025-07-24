# Tools Directory

This directory contains development tools and utilities for the Redaptive Agentic Platform.

## Directory Structure

### `/tests/` - Test Scripts
- **`test_api_logging.py`** - Test API key logging security
- **`test_cli_options.py`** - Test CLI interface options
- **`test_financial_fix.py`** - Test financial analysis functionality
- **`test_scope.py`** - Test scope detection functionality
- **`test_time.py`** - Test time request functionality
- **`test_time_fix.py`** - Test time request fixes

### `/debug/` - Debugging Tools
- **`debug_time.py`** - Debug time request functionality

### `/` - Demo Scripts
- **`demo.py`** - Comprehensive platform demo with system discovery, orchestration, and real-world use cases

## Usage

### User-Facing CLI Tools (in scripts directory)
```bash
# Terminal CLI
./activate_venv.sh python scripts/terminal_cli.py

# Web Interface
./activate_venv.sh python scripts/web_interface.py
# Then open: http://localhost:8080
```

### Test Scripts
```bash
# Run specific tests
./activate_venv.sh python tools/tests/test_time.py
./activate_venv.sh python tools/tests/test_financial_fix.py
```

### Demo Scripts
```bash
# Run comprehensive demo
./activate_venv.sh python tools/demo.py
```

## Demo Features

The `demo.py` script showcases:

- **System Discovery**: Available agents and capabilities
- **Orchestration Engine**: Multi-agent workflow coordination
- **Real-World Use Cases**: Fortune 500 energy portfolio management
- **Architecture Highlights**: Technical stack and scalability features
- **Getting Started**: Next steps for development and deployment 