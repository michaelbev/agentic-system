# 🗄️ Database Scripts

Database management scripts for the Redaptive Energy Portfolio Management system.

## 📁 Files

- **`setup_energy_db.sh`** - Primary energy database setup script
- **`test_energy_db.sh`** - Database connectivity and data validation tests
- **`README.md`** - This documentation

## 🚀 Usage

### **Setup Energy Database**
```bash
# Basic setup
./scripts/database/setup_energy_db.sh

# Force recreation of existing database
./scripts/database/setup_energy_db.sh --force

# Verify existing setup only
./scripts/database/setup_energy_db.sh --verify-only
```

### **Test Database**
```bash
# Run all tests
./scripts/database/test_energy_db.sh

# Show database summary only
./scripts/database/test_energy_db.sh --summary-only
```

## 🔧 Setup Features

### **`setup_energy_db.sh`**
- ✅ PostgreSQL server connectivity check
- ✅ Energy database creation
- ✅ Application user setup with proper permissions
- ✅ Enhanced energy schema deployment
- ✅ Fortune 500 sample data loading
- ✅ Comprehensive error handling
- ✅ Setup verification

### **Database Structure Created**
- **Portfolios**: Fortune 500 energy portfolios
- **Buildings**: Real estate properties with energy data
- **Energy Meters**: IoT meter infrastructure (12k+ scale ready)
- **Energy Readings**: Historical and real-time consumption data
- **Projects**: Energy efficiency and EaaS projects
- **Contracts**: Performance-based energy contracts

## 🧪 Test Features

### **`test_energy_db.sh`**
- ✅ Database connection validation
- ✅ Schema integrity checks
- ✅ Sample data verification
- ✅ Agent-specific query testing
- ✅ Performance validation
- ✅ Comprehensive reporting

### **Test Coverage**
- **Connection Tests**: Basic connectivity and authentication
- **Schema Tests**: Table structure and relationships
- **Data Tests**: Sample data presence and integrity
- **Query Tests**: Location and type-based searches
- **Agent Tests**: Portfolio analysis and energy aggregation queries

## 📊 Database Configuration

### **Default Settings**
```bash
DB_NAME_ENERGY="energy_db"
DB_USER="energy_user" 
DB_PASSWORD="energy123"
DB_HOST_ENERGY="localhost"
DB_PORT_ENERGY="5432"
```

### **Environment Variables**
```bash
# Override defaults with environment variables
export DB_HOST_ENERGY="your-db-host"
export DB_PORT_ENERGY="5432"
export DB_USER_ENERGY="your-app-user"
export DB_USERPASSWORD_ENERGY="your-password"
```

## 🔒 Security Notes

- **Admin Separation**: Uses PostgreSQL admin user for setup, app user for runtime
- **Least Privilege**: App user has only necessary permissions
- **Password Security**: Default password should be changed for production
- **Network Security**: Database access should be restricted to application servers

## 🚨 Troubleshooting

### **Common Issues**

**PostgreSQL not running**
```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# Start PostgreSQL (macOS with Homebrew)
brew services start postgresql

# Start PostgreSQL (Linux systemd)
sudo systemctl start postgresql
```

**Permission denied**
```bash
# Ensure you have PostgreSQL admin privileges
sudo -u postgres psql

# Or set PGUSER environment variable
export PGUSER=postgres
```

**Database already exists**
```bash
# Force recreation
./scripts/database/setup_energy_db.sh --force

# Or manually drop and recreate
dropdb energy_db
./scripts/database/setup_energy_db.sh
```

## 📝 Notes

- **Production Ready**: Scripts include comprehensive error handling
- **Idempotent**: Safe to run multiple times
- **Redaptive Specific**: Optimized for energy portfolio management
- **Scalable**: Schema supports 12k+ meters and Fortune 500 portfolios
- **Sample Data**: Includes realistic test data for development