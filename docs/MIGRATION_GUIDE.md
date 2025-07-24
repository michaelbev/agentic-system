# Migration Guide: Old Structure → New Structure

## Import Changes

### Old Structure
```python
from agents.portfolio_intelligence_agent import PortfolioIntelligenceAgent
from orchestration.intelligent.intelligent_orchestrator import IntelligentOrchestrator
```

### New Structure  
```python
from redaptive.agents.energy import PortfolioIntelligenceAgent
from redaptive.orchestration import OrchestrationEngine
```

## Agent Registry Changes

### Old
```python
from agents import AGENT_REGISTRY
```

### New
```python
from redaptive.agents import AGENT_REGISTRY
```

## Configuration Changes

### Old
```python
# Manual environment variable handling
DB_HOST_ENERGY = os.getenv('DB_HOST_ENERGY', 'localhost')
```

### New
```python
from redaptive.config import settings
DB_HOST_ENERGY = settings.database.host
```

## Running Agents

### Old
```bash
python start_agents.py
python agents/portfolio_intelligence_agent.py
```

### New
```bash
python -m redaptive portfolio-intelligence
python -m redaptive energy-monitoring
```

## File Locations

| Component | Old Location | New Location |
|-----------|-------------|-------------|
| Agents | `agents/` | `src/redaptive/agents/` |
| Orchestration | `orchestration/` | `src/redaptive/orchestration/` |
| Configuration | Environment variables | `src/redaptive/config/` |
| Tools | `scripts/tools/` | `src/redaptive/tools/` |

## Examples Update

Update your examples by:
1. Changing path insertion: `sys.path.insert(0, str(project_root / "src"))`
2. Updating imports to use `redaptive.*` namespace
3. Using new configuration system
4. Using new orchestration engine

## Removed Files

These files were removed in the restructure:
- `agents/` directory (moved to `src/redaptive/agents/`)
- `orchestration/` directory (moved to `src/redaptive/orchestration/`)  
- `start_agents.py` (replaced by `python -m redaptive`)