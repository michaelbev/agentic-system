# Energy Database Setup

This directory contains the database schema and seed data for the Energy as a Service platform.

## Quick Setup (if you have PostgreSQL running)

### Option 1: Automated Setup (Recommended)
```bash
# Copy example environment file
cp ../../.env.example ../../.env

# Edit .env file with your database settings (optional)
# nano ../../.env

# Run the automated setup script
../../scripts/database/setup_database.sh
```

### Option 2: Manual Setup
```bash
# Create the database
createdb energy_db

# Create user
createuser energy_user

# Run the schema setup
psql energy_db < schema/01_schema.sql

# Add sample data
psql energy_db < seed/02_seed_data.sql
```

## Environment Variables

Set these environment variables for the energy agents to connect:

```bash
export DB_HOST_ENERGY=127.0.0.1
export DB_PORT_ENERGY=5432
export DB_NAME_ENERGY=energy_db
export DB_USER_ENERGY=energy_user
export DB_USERPASSWORD_ENERGY=your_password
```

## Test the Setup

Once the database is running, you can test the energy agent:

```python
from agents.energy_agent import EnergyAgent

agent = EnergyAgent()
result = await agent.search_facilities(location="Dallas", limit=5)
print(f"Found {result['facilities_found']} facilities in Dallas")
```

## Sample Data

The database includes:
- 5 energy portfolios across Fortune 500 companies
- 18 buildings across the United States
- Energy consumption data, meters, and projects
- Sustainability reports and benchmark data
- Project opportunities and analytics

## Schema Overview

- `portfolios` - Company energy portfolios
- `buildings` - Energy facilities and properties
- `energy_meters` - Metering infrastructure
- `energy_usage` - Time-series consumption data
- `energy_projects` - Energy efficiency projects
- `project_opportunities` - Identified savings opportunities
- `sustainability_reports` - Environmental reporting
- `benchmark_data` - Industry comparison data 