# 🧪 Testing the Intelligent Orchestrator

This guide explains how to run all tests and examples for the intelligent orchestrator system.

---

## 📁 Test Organization

The tests are organized into the following structure:

```
tests/
├── unit/                    # Unit tests for core functionality
│   ├── test_planning.py    # Comprehensive planning tests
│   ├── test_orchestration.py
│   ├── test_tools.py
│   ├── test_agents.py
│   ├── test_config.py
│   ├── test_streaming.py
│   └── quick_test.py
├── integration/             # Integration tests with real agents
│   ├── test_pdf_summary.py
│   ├── test_orchestrator.py
│   ├── test_agents.py
│   └── test_platform.py
├── setup/                   # Setup validation tests
│   └── test_mcp_setup.py
├── demos/                   # Demo scripts for functionality
│   ├── planning_comparison_demo.py
│   └── llm_client_demo.py
├── files/                   # Test data (PDFs, documents, etc.)
└── conftest.py             # Pytest configuration
```

---

## 🚀 Quick Start

### 1. Run All Tests

From the project root:

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
PYTHONPATH=src python -m pytest tests/ -v

# Run specific test categories
PYTHONPATH=src python -m pytest tests/unit/ -v
PYTHONPATH=src python -m pytest tests/integration/ -v
PYTHONPATH=src python -m pytest tests/setup/ -v
```

### 2. Run Demo Scripts

```bash
# Planning comparison demo
PYTHONPATH=src python tests/demos/planning_comparison_demo.py

# LLM client demo
PYTHONPATH=src python tests/demos/llm_client_demo.py
```

### 3. Run Test Runner Script

```bash
PYTHONPATH=src python tests/run_tests.py
```

---

## 🧪 Test Categories

### Unit Tests (`tests/unit/`)

**`test_planning.py`** - Comprehensive planning functionality tests
- Rule-based planning validation
- Learning-based planning validation  
- Hybrid planning strategies
- LLM client functionality
- Agent routing validation

**`test_orchestration.py`** - Orchestration engine tests
- Workflow creation and execution
- Agent coordination
- Error handling

**`test_tools.py`** - Tool functionality tests
- Database tools
- Data processing tools
- MCP client tools

**`test_agents.py`** - Individual agent tests
- Energy monitoring agent
- Energy finance agent
- Portfolio intelligence agent
- System agent

**`test_config.py`** - Configuration tests
- Environment variable loading
- Configuration validation

**`test_streaming.py`** - Streaming functionality tests
- Kafka integration
- Redis integration
- Data streaming

### Integration Tests (`tests/integration/`)

**`test_pdf_summary.py`** - PDF processing workflows
- Document extraction
- Text summarization
- End-to-end PDF processing

**`test_orchestrator.py`** - Intelligent workflow testing
- Multi-agent coordination
- Complex workflow execution

**`test_agents.py`** - Agent integration tests
- Agent communication
- Tool execution
- Data flow between agents

**`test_platform.py`** - Platform-level tests
- System integration
- Performance testing

### Setup Tests (`tests/setup/`)

**`test_mcp_setup.py`** - MCP environment validation
- MCP server setup
- Tool availability
- Environment configuration

### Demo Scripts (`tests/demos/`)

**`planning_comparison_demo.py`** - Planning methods comparison
- Shows different planning approaches
- Demonstrates agent routing
- Compares rule-based vs learning-based

**`llm_client_demo.py`** - LLM client functionality
- API provider testing
- Response generation
- Fallback mechanisms

---

## 🔧 Test Configuration

### Environment Variables

Tests require the following environment variables:

```bash
# LLM Provider Configuration
PREFERRED_LLM_PROVIDER=anthropic  # or openai
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Database Configuration
DB_HOST_ENERGY=localhost
DB_PORT_ENERGY=5432
DB_NAME_ENERGY=energy_db
DB_USER_ENERGY=user
DB_USERPASSWORD_ENERGY=password

# AWS Configuration (for PDF processing)
AWS_REGION=us-west-2
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

### Running Tests Without API Keys

The system gracefully falls back to rule-based planning when API keys are not available:

```bash
# Tests will still pass with fallback mechanisms
PYTHONPATH=src python -m pytest tests/unit/test_planning.py -v
```

---

## 📊 Test Results

### Expected Test Results

- **Unit Tests**: 50+ tests, all should pass
- **Integration Tests**: 10+ tests, may have some failures due to external dependencies
- **Setup Tests**: 6 tests, validates environment configuration
- **Demo Scripts**: Show functionality without assertions

### Common Test Patterns

```python
# Planning test pattern
async def test_planning_method():
    planner = DynamicPlanner()
    result = await planner.create_workflow(query, agents)
    assert result["planning_method"] == "rule_based"
    assert "steps" in result

# LLM client test pattern  
async def test_llm_client():
    client = LLMClient(provider="anthropic")
    response = await client.generate(prompt)
    assert response is not None
    assert len(response) > 0
```

---

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `PYTHONPATH=src` is set
2. **API Key Errors**: Check `.env` file and environment variables
3. **Database Connection**: Verify database is running and accessible
4. **Async/Await**: All async tests use `@pytest.mark.asyncio`

### Debug Mode

Run tests with verbose output:

```bash
PYTHONPATH=src python -m pytest tests/ -v -s
```

### Running Specific Tests

```bash
# Run specific test file
PYTHONPATH=src python -m pytest tests/unit/test_planning.py -v

# Run specific test function
PYTHONPATH=src python -m pytest tests/unit/test_planning.py::TestPlanningMethods::test_rule_based_planning -v

# Run tests matching pattern
PYTHONPATH=src python -m pytest tests/ -k "planning" -v
```

---

For any issues or questions, see the main `README.md` or ask your friendly AI assistant! 