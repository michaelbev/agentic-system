# Redaptive Agentic AI Platform

A production-ready Energy-as-a-Service (EaaS) platform with intelligent orchestration, multi-agent workflows, and comprehensive energy portfolio management capabilities.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment
- Required dependencies (see `requirements.txt`)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd agentic-system

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

### AI/ML Credentials (Optional)
To enable learning-based planning and document processing, add these to your `.env` file:

```bash
# AI/ML Provider Credentials
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Preferred LLM Provider for Learning-based Planning
# Options: "openai" or "anthropic"
PREFERRED_LLM_PROVIDER=openai
```

**Note**: Without API keys, the system will use rule-based planning (keyword matching) instead of learning-based planning.



### AWS Credentials (Optional)
For PDF document processing with AWS Textract:

```bash
# AWS Credentials for Textract
AWS_REGION=your_aws_region_here
AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
# AWS_SESSION_TOKEN=your_session_token  # Only needed if using temporary credentials
```

### Credential Types and Purposes

#### **AI/ML Provider Credentials**
- **OPENAI_API_KEY**: Enables learning-based workflow planning using GPT models
- **ANTHROPIC_API_KEY**: Enables learning-based workflow planning using Claude models
- **GOOGLE_API_KEY**: Enables AI document summarization using Google Gemini

#### **AWS Credentials** 
- **AWS_REGION**: AWS region for Textract services
- **AWS_ACCESS_KEY_ID**: AWS access key for authentication
- **AWS_SECRET_ACCESS_KEY**: AWS secret key for authentication
- **Purpose**: PDF document processing and text extraction



### Verify Credentials
Check your credential setup:
```bash
./activate_venv.sh python scripts/check_credentials.py
```
```

### Running the Platform

#### Option 1: Terminal CLI
```bash
./activate_venv.sh python scripts/terminal_cli.py
```

#### Option 2: Web Interface (Recommended)
```bash
./activate_venv.sh python scripts/web_interface.py
# Then open: http://localhost:8080
```

## 📁 Project Structure

```
agentic-system/
├── src/                    # Main source code
│   └── redaptive/         # Core platform modules
│       ├── agents/         # AI agents (energy, content, system)
│       ├── orchestration/  # Workflow orchestration engine
│       ├── config/         # Configuration management
│       ├── streaming/      # Real-time data streaming
│       └── tools/          # Utility tools
├── scripts/                # User-facing CLI tools
│   ├── web_interface.py   # Web-based interface
│   ├── terminal_cli.py    # Terminal-based CLI
│   └── check_credentials.py # Credential validation tool
├── tools/                  # Development tools and utilities
│   ├── tests/             # Test scripts
│   ├── debug/             # Debugging tools
│   └── README.md          # Tools documentation
├── examples/               # Usage examples
│   ├── energy/            # Energy analysis examples
│   ├── pdf/               # Document processing examples
│   └── database/          # Database operation examples
├── docs/                   # Documentation
│   ├── architecture/      # Architecture documentation
│   ├── agents/            # Agent documentation
│   ├── api/               # API documentation
│   └── deployment/        # Deployment guides
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   ├── test_*.py         # Planning method tests
│   └── debug_*.py        # Debug scripts
├── data/                   # Data and database schemas
├── infrastructure/         # Docker and deployment configs
├── .env.example           # Environment configuration template
└── requirements.txt        # Python dependencies
```

## 🎯 Core Features

### 🤖 Intelligent Agents
- **Portfolio Intelligence Agent** - Portfolio analysis and optimization
- **Energy Monitoring Agent** - Real-time energy consumption monitoring
- **Energy Finance Agent** - Financial analysis and ROI calculations
- **Document Processing Agent** - PDF and document analysis
- **Summarization Agent** - AI-powered text summarization
- **System Agent** - System-level operations (time, scope checking)

### 🔄 Orchestration Engine
- **Intent Matching** - Natural language request understanding
- **Workflow Planning** - Dynamic workflow creation with LLM and hardcoded fallback
- **Multi-Agent Coordination** - Seamless agent collaboration
- **Scope Detection** - Intelligent request filtering
- **Planning Method Tracking** - Transparency into LLM vs hardcoded planning decisions

### 📊 Energy-as-a-Service Capabilities
- **Energy Consumption Analysis** - Building and portfolio-level insights
- **Financial Optimization** - ROI calculations and contract optimization
- **Portfolio Management** - Multi-site energy portfolio oversight
- **Document Processing** - Utility bill and report analysis
- **Real-time Monitoring** - IoT sensor data processing

## 🎮 Usage Examples

### Time and Date Requests
```
"What is the current time?"
"Get the current date"
```

### Financial Analysis
```
"Calculate ROI for LED retrofit project for building 123"
"Show me financial analysis for energy efficiency project"
```

### Energy Analysis
```
"Analyze energy consumption for building 456"
"Find energy optimization opportunities"
```

### Portfolio Management
```
"Show me portfolio performance metrics"
"Generate sustainability report"
```

### Document Processing
```
"Summarize this utility bill document"
"Extract data from energy report"
```

## 🧠 Planning Method Tracking

The system now provides transparency into which planning method was used for each request:

### Learning-based Planning (AI-powered)
```
🧠 Planning Method: Learning-based (AI-powered)
💭 Planning Reason: Learning-based planner used successfully
```

### Rule-based Planning (Systematic)
```
🔧 Planning Method: Rule-based (Systematic)
💭 Planning Reason: Energy-specific date query detected via keyword matching
```

### Hybrid Planning (Best of Both)
- **Primary**: Learning-based for intelligent, flexible planning
- **Fallback**: Rule-based system for reliability
- **Transparency**: See which method was used and why

## 🔧 Development

### Running Tests
```bash
# Run all tests
./activate_venv.sh python -m pytest tests/

# Run planning method tests
./activate_venv.sh python tests/test_planning_method.py
./activate_venv.sh python tests/test_hybrid_planner.py
./activate_venv.sh python tests/test_llm_planner.py

# Debug LLM functionality
./activate_venv.sh python tests/debug_llm.py
```

### Development Tools
```bash
# Run comprehensive demo
./activate_venv.sh python tools/demo.py
```

## 📚 Documentation

- **[Architecture Guide](docs/architecture/ARCHITECTURE_EVOLUTION_PLAN.md)** - System architecture and evolution
- **[Agent Documentation](docs/agents/)** - Detailed agent capabilities
- **[API Documentation](docs/api/)** - API reference and examples
- **[Deployment Guide](docs/deployment/)** - Production deployment instructions
- **[Migration Guide](docs/MIGRATION_GUIDE.md)** - System migration procedures

## 🛠️ Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:
- Database connections
- API keys (Google, AWS)
- Logging levels
- Agent configurations

### Database Setup
```bash
# Set up energy portfolio database
./scripts/database/setup_energy_db.sh
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is proprietary to Redaptive. All rights reserved.

## 🆘 Support

For support and questions:
- Check the [documentation](docs/)
- Review [examples](examples/)
- Run [tests](tools/tests/) to verify functionality