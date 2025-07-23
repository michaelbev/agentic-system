# 🏗️ Infrastructure Configuration

This directory contains Docker and infrastructure configuration for the Multi-Agent MCP Orchestration System.

## 📁 Files

- **`docker-compose.dev.yml`** - Development environment configuration
- **`setup-dev.sh`** - Development environment setup script
- **`README.md`** - This file

## 🚀 Quick Start

### **1. Prerequisites**
- Docker and Docker Compose installed
- API keys configured in `.env` file

### **2. Setup Development Environment**
```bash
# From the infrastructure directory
./setup-dev.sh
```

### **3. Manual Setup**
```bash
# Build and start all services
docker-compose -f docker-compose.dev.yml up --build -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

## 🏗️ Services

### **Core Services**
- **orchestration** (port 8080) - Main orchestration service
- **energy-agent** (port 5052) - Energy service booking agent
- **database-agent** (port 5053) - Database operations agent
- **textract-agent** (port 5054) - AWS Textract agent
- **summarize-agent** (port 5055) - Google Gemini summarization agent
- **time-agent** (port 5051) - MCP Time server

### **Infrastructure Services**
- **postgres** (port 5432) - PostgreSQL database
- **redis** (port 6379) - Redis cache
- **prometheus** (port 9090) - Monitoring
- **grafana** (port 3000) - Metrics dashboard

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file in the project root with:

```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-west-2

# Google AI Configuration
GOOGLE_API_KEY=your_google_api_key

# Database Configuration
DB_ADMIN=admin
DB_ADMIN_PASSWORD=your_admin_password
DB_ENERGYAPP_USER=energyapp
DB_ENERGYAPP_PASSWORD=your_app_password

# Timezone
LOCAL_TIMEZONE=America/Denver
```

### **Volume Mounts**
- **`../agents`** → `/app/agents` - Agent code
- **`../data`** → `/app/data` - Data files
- **`../scripts`** → `/app/scripts` - Database scripts
- **`../tests`** → `/app/tests` - Test files
- **`../logs`** → `/app/logs` - Application logs

## 🧪 Development Workflow

### **1. Start Services**
```bash
docker-compose -f docker-compose.dev.yml up -d
```

### **2. Setup Database**
```bash
# Run database setup script
docker-compose -f docker-compose.dev.yml exec postgres psql -U user -d energy_db -f /docker-entrypoint-initdb.d/01-create-tables.sql
```

### **3. Test System**
```bash
# Run tests
docker-compose -f docker-compose.dev.yml exec orchestration python tests/run_tests.py
```

### **4. View Logs**
```bash
# All services
docker-compose -f docker-compose.dev.yml logs -f

# Specific service
docker-compose -f docker-compose.dev.yml logs -f orchestration
```

## 🔍 Monitoring

### **Prometheus**
- URL: http://localhost:9090
- Metrics collection for all services

### **Grafana**
- URL: http://localhost:3000
- Username: `admin`
- Password: `admin`
- Pre-configured dashboards for monitoring

## 🛠️ Troubleshooting

### **Service Won't Start**
```bash
# Check logs
docker-compose -f docker-compose.dev.yml logs [service-name]

# Rebuild and restart
docker-compose -f docker-compose.dev.yml up --build -d
```

### **Database Connection Issues**
```bash
# Check database health
docker-compose -f docker-compose.dev.yml exec postgres pg_isready -U user -d energy_db

# Reset database
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d postgres
```

### **Agent Communication Issues**
```bash
# Check agent health
curl http://localhost:5052/health  # Energy agent
curl http://localhost:5053/health  # Database agent
curl http://localhost:5054/health  # Textract agent
```

## 📝 Useful Commands

```bash
# View all running containers
docker-compose -f docker-compose.dev.yml ps

# Execute commands in containers
docker-compose -f docker-compose.dev.yml exec orchestration python start_agents.py help

# View resource usage
docker stats

# Clean up
docker-compose -f docker-compose.dev.yml down -v --remove-orphans
```

## 🔄 Production Deployment

For production deployment, create a separate `docker-compose.prod.yml` with:
- Proper secrets management
- Load balancing
- SSL termination
- Backup strategies
- Monitoring and alerting

The current `docker-compose.dev.yml` is optimized for development with:
- Volume mounts for hot-reloading
- Debug logging
- Exposed ports for local access
- Development-friendly configuration

## 📚 Related Documentation

- [Main README](../README.md) - System overview
- [Energy Agent Documentation](../docs/agents/ENERGY_ORCHESTRATION.md)
- [Database Agent Documentation](../docs/agents/DATABASE_ORCHESTRATION.md)
- [PDF Agent Documentation](../docs/agents/PDF_ORCHESTRATION.md) 