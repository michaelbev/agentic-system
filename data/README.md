# 📊 Data Directory

This directory contains all data files for the Energy as a Service Platform Multi-Agent MCP System.

## 📁 Structure

```
data/
├── database/           # Database schema and seed data
│   ├── schema/         # Database schema files
│   │   ├── 00_drop_tables.sql
│   │   └── 01_schema.sql
│   ├── seed/           # Seed data files
│   │   └── 02_seed_data.sql
│   └── README.md       # Database documentation
├── .gitkeep            # Keep directory in git
└── README.md           # This file
```

## 🗄️ Database Files

### **Schema Files** (`database/schema/`)
- **`00_drop_tables.sql`** - Drops existing tables (cleanup)
- **`01_schema.sql`** - Creates energy database schema and tables

### **Seed Data** (`database/seed/`)
- **`02_seed_data.sql`** - Sample energy portfolio and building data

### **Usage**
```bash
# Setup database using scripts
./scripts/database/setup_database.sh

# Test database setup
./scripts/database/test_database.sh
```

## 🔄 Data Management

### **Adding New Data**
1. Create new SQL files in appropriate subdirectories
2. Update setup scripts to reference new files
3. Test with `test_database.sh`

### **Modifying Existing Data**
1. Edit SQL files in `database/` directory
2. Re-run setup script to apply changes
3. Verify with test script

### **Backup and Restore**
```bash
# Backup database
pg_dump -h 127.0.0.1 -U energy_user energy_db > data/backup.sql

# Restore database
psql -h 127.0.0.1 -U energy_user energy_db < data/backup.sql
```

## 📝 Notes

- Database files are version-controlled for development
- Production deployments should use proper database migration tools
- Seed data includes Fortune 500 energy portfolios across US cities
- Schema supports Energy as a Service platform workflows 