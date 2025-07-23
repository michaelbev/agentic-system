# 🧪 Testing the Intelligent Orchestrator

This guide explains how to run all tests and examples for the intelligent orchestrator system.

---

## 1. Quick Test (No Dependencies)

From the `apexory/agentic-system/tests/` directory, run:

```bash
PYTHONPATH=../orchestration python unit/quick_test.py
```

Or, from the project root:

```bash
PYTHONPATH=apexory/agentic-system/orchestration python apexory/agentic-system/tests/unit/quick_test.py
```

---

## 2. Full Test Suite (with pytest)

From the project root, run:

```bash
pip install -r apexory/agentic-system/tests/requirements-test.txt
pytest apexory/agentic-system/tests/ -v
```

Or, run specific test categories:

```bash
# Unit tests only
pytest apexory/agentic-system/tests/unit/ -v

# Integration tests only
pytest apexory/agentic-system/tests/integration/ -v

# Setup validation tests only
pytest apexory/agentic-system/tests/setup/ -v
```

---

## 3. Test Runner Script

From the `tests/` directory:

```bash
PYTHONPATH=../orchestration python run_tests.py
```

---

## 4. Test Organization

The tests are now organized into categories:

- **`unit/`** - Unit tests for core functionality
  - `test_intelligent_orchestrator.py` - Comprehensive orchestrator tests
  - `quick_test.py` - Fast validation tests

- **`integration/`** - Integration tests with real agents
  - `test_pdf_summary.py` - PDF processing workflows
  - `test_orchestrator.py` - Intelligent workflow testing
  - `test_agents.py` - Individual agent testing

- **`setup/`** - Setup validation tests
  - `test_mcp_setup.py` - MCP environment validation

- **`files/`** - Test data (PDFs, documents, etc.)

---

## Notes

- `PYTHONPATH=../orchestration` tells Python to look for modules in the orchestration directory, so imports like `from intelligent_orchestrator import ...` work.
- For CI or automation, always set `PYTHONPATH` or use the project root as your working directory.
- If you add new test files, use the same import pattern for consistency.

---

For any issues or questions, see the main `README.md` or ask your friendly AI assistant! 