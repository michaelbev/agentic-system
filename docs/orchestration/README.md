# 🎯 Orchestration Package Structure

This directory contains the intelligent multi-agent orchestration system, organized for clarity and maintainability with support for both pattern-based and dynamic AI planning.

## 📁 Directory Structure

```
orchestration/
├── __init__.py                    # Main package exports
├── intelligent_orchestrator.py    # Main entry point (re-exports from intelligent)
├── intelligent/                   # Intelligent, goal-driven orchestration
│   ├── __init__.py
│   ├── intelligent_orchestrator.py
│   ├── base_orchestrator.py
│   ├── workflow_engine.py
│   ├── models.py
│   ├── planners/                  # Workflow planning strategies
│   │   ├── __init__.py
│   │   ├── base_planner.py        # Base planner abstract class
│   │   ├── pattern_planner.py     # Rule-based pattern matching
│   │   ├── dynamic_planner.py     # AI-based dynamic planning (future)
│   │   └── hybrid_planner.py      # Combines pattern + dynamic
│   └── matchers/                  # Intent matching strategies
│       ├── __init__.py
│       ├── keyword_matcher.py     # Keyword-based intent matching
│       ├── semantic_matcher.py    # Semantic intent matching (future)
│       └── intent_analyzer.py     # Intent analysis utilities
├── explicit/                      # (Optional) Explicit/manual workflow orchestrators
│   └── __init__.py
├── examples/                      # Example usage and comparisons
│   ├── __init__.py
│   ├── example_usage.py
│   └── comparison.py
└── README.md
```

## 🚀 Usage

### **Main Entry Point (Recommended)**
```python
from orchestration import process_user_request

# Natural language goal processing
result = await process_user_request("summarize this PDF", file_path="document.pdf")
```

### **Direct Intelligent Access (Advanced)**
```python
from orchestration.intelligent import IntelligentOrchestrator

orchestrator = IntelligentOrchestrator()
result = await orchestrator.execute_intelligent_workflow("summarize this PDF")
```

### **Custom Planning Strategies**
```python
from orchestration import PatternPlanner, DynamicPlanner, HybridPlanner

# Use specific planner
pattern_planner = PatternPlanner()
workflow = pattern_planner.plan_workflow("summarize this PDF")

# Use hybrid planner (pattern + dynamic)
hybrid_planner = HybridPlanner()
workflow = hybrid_planner.plan_workflow("analyze sentiment of this document")
```

### **Intent Analysis**
```python
from orchestration import IntentAnalyzer, KeywordMatcher

# Analyze user intent
analyzer = IntentAnalyzer(KeywordMatcher())
analysis = analyzer.analyze("summarize this PDF", available_tools)
print(f"Intent: {analysis['intent']}")
print(f"Matched tools: {len(analysis['matched_tools'])}")
```

### **Component-Level Access (Development)**
```python
from orchestration.intelligent import PatternPlanner, WorkflowEngine

# Direct component usage for testing/debugging
planner = PatternPlanner()
workflow = planner.plan_workflow("summarize this PDF")
```

## 🔧 Development

### **Adding New Planning Strategies**
1. Create new planner in `intelligent/planners/`
2. Extend `BasePlanner` class
3. Update `planners/__init__.py` to export new planner
4. Update main `__init__.py` if needed for public API

### **Adding New Intent Matchers**
1. Create new matcher in `intelligent/matchers/`
2. Extend `BaseMatcher` class
3. Update `matchers/__init__.py` to export new matcher
4. Update main `__init__.py` if needed for public API

### **Examples and Testing**
- Add new examples to `examples/` directory
- Test files should import from the main package: `from orchestration import ...`

## 🧠 Planning Architecture

### **Current Planning Strategies**

| Planner | Type | Description | Status |
|---------|------|-------------|--------|
| **PatternPlanner** | Rule-based | Uses predefined workflow patterns | ✅ Working |
| **DynamicPlanner** | AI-based | Dynamic workflow composition | 🔧 Future |
| **HybridPlanner** | Combined | Pattern first, dynamic fallback | ✅ Working |

### **Intent Matching Strategies**

| Matcher | Type | Description | Status |
|---------|------|-------------|--------|
| **KeywordMatcher** | Keyword-based | Simple keyword matching | ✅ Working |
| **SemanticMatcher** | Embedding-based | Semantic similarity matching | 🔧 Future |

### **Evolution Path**

1. **Current**: Pattern-based planning with keyword matching
2. **Next**: Add semantic intent matching
3. **Future**: AI-based dynamic workflow planning
4. **Advanced**: Learning-based workflow optimization

## 📚 Documentation

- **Main Documentation**: See `docs/README.md` for detailed usage
- **API Reference**: Check `intelligent/` module docstrings
- **Examples**: See `examples/` directory for usage patterns

## 🎯 Benefits of This Organization

- **Clear Separation**: Intelligent, explicit, and examples code are separated
- **Modular Planning**: Easy to add new planning strategies
- **Flexible Intent Matching**: Support for different intent matching approaches
- **Future-Proof**: Ready for AI-based dynamic planning
- **Easy Navigation**: Developers can quickly find what they need
- **Maintainable**: Each component has a clear responsibility
- **Extensible**: Easy to add new components or examples
- **Backward Compatible**: Main API remains unchanged 
