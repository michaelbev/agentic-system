# Energy Analysis Examples

This directory demonstrates **intelligent workflow orchestration** for energy-as-a-service operations. The examples show how natural language requests are automatically transformed into complex multi-agent workflows.

## 🎯 What This Demonstrates

The intelligent orchestration system provides a revolutionary approach to energy management:

- **Natural Language Interface**: Request complex operations using simple English
- **Automatic Workflow Planning**: System plans optimal workflows without manual configuration
- **Multi-Agent Coordination**: Coordinates multiple specialized agents (energy, time, summarization)
- **Error Handling**: Graceful handling of failures and partial results
- **Scalable Architecture**: Easily extensible for new energy services and analysis types

## 📁 Files

- `energy_orchestration_example.py` - Comprehensive demonstration of intelligent energy workflows
- `README.md` - This documentation file

## 🚀 Quick Start

```bash
# Activate virtual environment and run the example
./activate_venv.sh python examples/energy/energy_orchestration_example.py
```

## 💡 Examples Included

### 1. **Energy Data Analysis**
- **Request**: "analyze energy consumption for this building"
- **What happens**: System identifies this as data analysis, fetches energy data, processes it
- **Agents used**: Energy agent → Summarization agent
- **Result**: Structured energy consumption data with analysis

### 2. **Service Booking**
- **Request**: "schedule an energy audit for next week"
- **What happens**: System recognizes service booking intent, schedules audit
- **Agents used**: Time agent → Energy agent
- **Result**: Scheduled audit with confirmation details

### 3. **Facility Search**
- **Request**: "find office buildings in Denver for energy services"
- **What happens**: System searches facilities matching criteria
- **Agents used**: Energy agent
- **Result**: List of matching facilities with details

### 4. **Multi-step Analysis**
- **Request**: "analyze energy consumption trends and provide efficiency recommendations"
- **What happens**: Complex analysis involving data retrieval, trend analysis, and recommendations
- **Agents used**: Energy agent → Summarization agent
- **Result**: Comprehensive analysis with actionable insights

## 🧠 Intelligence Features

### Pattern Recognition
The system automatically recognizes different types of energy-related requests:
- **Analysis patterns**: "analyze", "consumption", "efficiency", "usage"
- **Booking patterns**: "schedule", "book", "appointment", "audit"
- **Search patterns**: "find", "search", "locate", "buildings"

### Workflow Planning
For each request, the system:
1. **Analyzes intent** using keyword matching and pattern recognition
2. **Plans optimal workflow** by selecting appropriate agents and tools
3. **Executes steps** in the correct order with proper error handling
4. **Aggregates results** into a coherent response

### Multi-Agent Coordination
The system coordinates multiple specialized agents:
- **Energy Agent**: Facility search, energy data, service booking
- **Time Agent**: Current time, timezone conversion, scheduling
- **Summarization Agent**: Text analysis, report generation, insights

## 🔧 Technical Details

### Agent Tools Available
- `search_facilities` - Search for energy facilities by location and type
- `check_service_availability` - Check availability of energy services
- `book_service` - Book energy services for facilities
- `get_facility_energy_data` - Retrieve energy consumption data

### Request Parameters
Different examples use different parameter structures:
- **Data analysis**: `facility_id`, `date_range`, `energy_type`
- **Service booking**: `facility_id`, `service_type`, `service_date`, `customer_name`, `customer_email`
- **Facility search**: `location`, `facility_type`, `min_capacity`

## 📊 Expected Output

The examples provide rich, structured output showing:
- **Request analysis**: How the system interpreted your request
- **Workflow planning**: What steps were planned and why
- **Execution details**: Results from each step in the workflow
- **Aggregated results**: Final structured response
- **Error handling**: Graceful handling of any issues

## 🛠️ Prerequisites

### Required
- Python 3.11+ with virtual environment activated
- Project dependencies installed (`requirements.txt`)

### Optional (for full functionality)
- **Database connection**: PostgreSQL with energy data
- **External APIs**: AWS credentials for enhanced features
- **Running agents**: Energy, time, and summarization agents

### Running Without Prerequisites
The examples will work even without databases or external APIs:
- **Planning demonstration**: Shows how workflows are planned
- **Mock responses**: Simulated responses for missing components
- **Error handling**: Demonstrates graceful degradation

## 🎓 Learning Objectives

After running these examples, you'll understand:
1. **How natural language requests become workflows**
2. **The power of intelligent orchestration**
3. **Multi-agent coordination patterns**
4. **Error handling and recovery strategies**
5. **Extensibility for new energy services**

## 🚀 Next Steps

- **Extend patterns**: Add new workflow patterns for your use cases
- **Add agents**: Create specialized agents for your domain
- **Integrate APIs**: Connect to real energy management systems
- **Build UI**: Create web interfaces using the intelligent orchestration engine

---

🎯 **The goal is to show how complex energy operations can be simplified through intelligent orchestration, making advanced energy management accessible through natural language.**