# 🔧 Scripts Directory

This directory contains utility scripts organized by clear functional categories.

## 📁 Structure

```
scripts/
├── database/              # Database management and setup
│   ├── setup_energy_db.sh     # Primary energy database setup
│   ├── test_energy_db.sh       # Database connectivity tests
│   └── README.md               # Database script documentation
├── ide/                   # IDE-specific configurations
│   ├── generate_cursor_mcp.py  # Cursor IDE MCP configuration
│   ├── configure_cursor.sh     # Cursor setup automation
│   └── README.md               # IDE integration guide
├── tools/                 # Standalone utility tools
│   ├── mcp_client.py           # Production MCP client
│   ├── start_agents.py         # Agent startup utility
│   └── README.md               # Tools documentation
├── examples/              # Example and learning scripts
│   ├── mcp_example.py          # MCP protocol learning example
│   ├── orchestration_demo.py   # Orchestration demonstration
│   └── README.md               # Examples guide
└── README.md              # This file
```

## 🗄️ Database Scripts

### **Primary Database Setup**
```bash
# Setup energy database with current schema
./scripts/database/setup_energy_db.sh

# Test database connectivity and data
./scripts/database/test_energy_db.sh
```

## 🎯 IDE Integration

### **Cursor IDE Setup**
```bash
# Generate Cursor MCP configuration
python scripts/ide/generate_cursor_mcp.py

# Full Cursor setup automation
./scripts/ide/configure_cursor.sh
```

## 🛠️ Utility Tools

### **MCP Client**
```bash
# Production-ready MCP client for testing
python scripts/tools/mcp_client.py
```

### **Agent Management**
```bash
# Start individual agents
python scripts/tools/start_agents.py energy-monitoring
python scripts/tools/start_agents.py energy-finance
```

## 📚 Examples and Learning

### **MCP Protocol Learning**
```bash
# Learn MCP protocol implementation
python scripts/examples/mcp_example.py
```

### **Orchestration Demo**
```bash
# Demonstrate intelligent orchestration
python scripts/examples/orchestration_demo.py
```

## 🚀 Quick Start

### **1. Setup Database**
```bash
./scripts/database/setup_energy_db.sh
./scripts/database/test_energy_db.sh
```

### **2. Configure IDE (if using Cursor)**
```bash
python scripts/ide/generate_cursor_mcp.py
```

### **3. Test MCP Client**
```bash
python scripts/tools/mcp_client.py
```

### **4. Run Examples**
```bash
python scripts/examples/orchestration_demo.py
```

## 📝 Organization Principles

- **Functional grouping**: Scripts grouped by primary purpose
- **Clear naming**: File names indicate exact function
- **Single responsibility**: Each script has one clear purpose
- **Production vs. learning**: Clear separation between production tools and examples
- **IDE-specific**: IDE configurations isolated from general tools

## 🔄 Migration from Old Structure

The scripts have been reorganized for clarity:

**Old Structure Issues Fixed**:
- ❌ `generate_mcp_json.py` → ✅ `generate_cursor_mcp.py` (accurate naming)
- ❌ Redundant MCP clients → ✅ Single production client + learning example
- ❌ Multiple database scripts → ✅ Single current setup + test scripts
- ❌ Mixed purposes in directories → ✅ Clear functional separation

**Benefits**:
- 🎯 Clear file purposes
- 🗂️ Logical organization
- 🔧 Reduced redundancy
- 📚 Better learning path
- 🚀 Easier maintenance