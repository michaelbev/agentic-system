# Redaptive Agentic AI Platform

A modern, production-ready multi-agent AI system for Energy-as-a-Service (EaaS) portfolio management and optimization.

## 🚀 Overview

The Redaptive Agentic Platform provides intelligent automation for Fortune 500 energy portfolios through specialized AI agents that handle real-time IoT monitoring, financial optimization, and portfolio intelligence.

### Key Capabilities

- **Real-time Energy Monitoring**: Process 12,000+ energy meters (48k+ data points/hour)
- **Portfolio Intelligence**: Strategic analysis and optimization for large-scale energy portfolios  
- **Financial Optimization**: EaaS revenue optimization and ROI analysis
- **Document Processing**: Automated processing of energy reports and contracts
- **Multi-Agent Orchestration**: Intelligent workflow coordination between agents

## 🏗️ Architecture

```
src/redaptive/
├── agents/           # AI agent implementations
│   ├── base/         # Base MCP server framework
│   ├── energy/       # Energy domain agents
│   └── content/      # Content processing agents
├── orchestration/    # Multi-agent coordination
├── tools/           # Shared utilities
├── config/          # Configuration management
└── models/          # Data models and schemas
```

### Agent Overview

| Agent | Purpose | Tools |
|-------|---------|-------|
| **Portfolio Intelligence** | Strategic energy analysis | 9 tools for portfolio optimization |
| **Energy Monitoring** | Real-time IoT processing | 6 tools for meter data and alerts |
| **Energy Finance** | EaaS revenue optimization | 6 tools for financial analysis |
| **Document Processing** | PDF and report analysis | Document extraction and processing |
| **Summarization** | Content summarization | Text analysis and synthesis |

## 🚦 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (optional, for IoT streaming)

### Installation

```bash
# Clone the repository
git clone https://github.com/redaptive/agentic-platform.git
cd agentic-platform

# Install dependencies
pip install -e .

# Setup database
scripts/setup/setup_database.sh

# Configure environment
cp .env.example .env
# Edit .env with your database credentials
```

### Running Agents

```bash
# Start individual agents
python -m redaptive portfolio-intelligence
python -m redaptive energy-monitoring
python -m redaptive energy-finance

# Or use the orchestration engine
python -m redaptive.orchestration
```

## 🔧 Configuration

Configuration is managed through environment variables and the `src/redaptive/config/` module:

```python
from redaptive.config import settings

# Database settings
print(settings.database.host)
print(settings.database.name)

# Agent settings  
print(settings.agents.max_concurrent_agents)
print(settings.agents.default_timeout)
```

### Environment Variables

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=energy_db
DB_ENERGYAPP_USER=energy_user
DB_ENERGYAPP_PASSWORD=your_password

# Agents
MAX_CONCURRENT_AGENTS=10
AGENT_TIMEOUT=30
LOG_LEVEL=INFO

# Orchestration
ENABLE_INTELLIGENT_ROUTING=true
MAX_WORKFLOW_DEPTH=10
```

## 📊 Usage Examples

### Portfolio Analysis

```python
from redaptive.agents.energy import PortfolioIntelligenceAgent

agent = PortfolioIntelligenceAgent()

# Analyze portfolio energy usage
result = await agent.analyze_portfolio_energy_usage(
    portfolio_id="portfolio_001",
    date_range={
        "start_date": "2024-01-01", 
        "end_date": "2024-12-31"
    }
)

print(f"Total consumption: {result['portfolio_metrics']['total_consumption']} kWh")
```

### Real-time Monitoring

```python
from redaptive.agents.energy import EnergyMonitoringAgent

monitor = EnergyMonitoringAgent()

# Process meter data
result = await monitor.process_meter_data(
    meter_id="meter_12345",
    readings=[
        {"timestamp": "2024-01-01T12:00:00Z", "value": 150.5, "unit": "kWh"}
    ]
)
```

### Multi-Agent Workflow

```python
from redaptive.orchestration import OrchestrationEngine

engine = OrchestrationEngine()
await engine.initialize_agents(["portfolio-intelligence", "energy-monitoring"])

workflow = {
    "steps": [
        {
            "agent": "portfolio-intelligence",
            "tool": "analyze_portfolio_energy_usage",
            "parameters": {"portfolio_id": "portfolio_001", "date_range": {...}}
        },
        {
            "agent": "energy-monitoring", 
            "tool": "detect_anomalies",
            "parameters": {"meter_ids": ["meter_001", "meter_002"]}
        }
    ]
}

result = await engine.execute_workflow("workflow_001", workflow)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest -m "not slow"  # Skip slow tests

# With coverage
pytest --cov=redaptive --cov-report=html
```

## 📈 Monitoring & Observability

The platform includes built-in observability features:

- **Health Checks**: Database and agent health monitoring
- **Metrics**: Performance and usage metrics
- **Logging**: Structured logging with correlation IDs
- **Tracing**: Request tracing across agents (optional)

## 🚀 Deployment

### Docker

```bash
# Build image
docker build -t redaptive-platform .

# Run with docker-compose
docker-compose up -d
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f deployment/kubernetes/
```

## 🔒 Security

- Database connections use connection pooling and prepared statements
- Agent communication follows MCP security guidelines
- Environment-based configuration management
- No hardcoded secrets or credentials

## 📚 Documentation

- [Agent Development Guide](docs/agents/development.md)
- [Orchestration Guide](docs/orchestration/guide.md)
- [API Reference](docs/api/reference.md)
- [Deployment Guide](docs/deployment/guide.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🆘 Support

- [GitHub Issues](https://github.com/redaptive/agentic-platform/issues)
- [Documentation](https://docs.redaptive.com/agentic-platform)
- Email: ai-support@redaptive.com