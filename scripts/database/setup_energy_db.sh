#!/bin/bash

# Primary Database Setup Script for Redaptive Energy Portfolio Management
# Creates comprehensive energy database schema with sample data
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() { echo -e "${BLUE}🔋 $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# Get project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA_DIR="$PROJECT_ROOT/data/database"

# Database configuration
DB_NAME_ENERGY="energy_db"
DB_ADMIN_ENERGY_USER="postgres"
DB_APP_USER="energy_user"
DB_HOST_ENERGY="${DB_HOST_ENERGY:-localhost}"
DB_PORT_ENERGY="${DB_PORT_ENERGY:-5432}"

# Function to check if PostgreSQL is running
check_postgres() {
    if ! command -v psql &> /dev/null; then
        print_error "PostgreSQL client (psql) not found. Please install PostgreSQL."
        exit 1
    fi
    
    if ! pg_isready -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" &> /dev/null; then
        print_error "PostgreSQL server is not running on $DB_HOST_ENERGY:$DB_PORT_ENERGY"
        print_warning "Please start PostgreSQL server first"
        exit 1
    fi
    
    print_success "PostgreSQL server is running"
}

# Function to create database and user
setup_database() {
    print_status "Setting up energy database..."
    
    # Create database if it doesn't exist
    if ! psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_ADMIN_ENERGY_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME_ENERGY"; then
        print_status "Creating database: $DB_NAME_ENERGY"
        createdb -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_ADMIN_ENERGY_USER" "$DB_NAME_ENERGY"
        print_success "Database '$DB_NAME_ENERGY' created"
    else
        print_warning "Database '$DB_NAME_ENERGY' already exists"
    fi
    
    # Create app user if it doesn't exist
    if ! psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_ADMIN_ENERGY_USER" -t -c "SELECT 1 FROM pg_roles WHERE rolname='$DB_APP_USER'" | grep -q 1; then
        print_status "Creating application user: $DB_APP_USER"
        psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_ADMIN_ENERGY_USER" -c "CREATE USER $DB_APP_USER WITH PASSWORD 'energy123';"
        psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_ADMIN_ENERGY_USER" -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME_ENERGY TO $DB_APP_USER;"
        print_success "User '$DB_APP_USER' created with database privileges"
    else
        print_warning "User '$DB_APP_USER' already exists"
    fi
}

# Function to run SQL scripts
run_sql_scripts() {
    print_status "Running database schema and data scripts..."
    
    # Check if data directory exists
    if [ ! -d "$DATA_DIR" ]; then
        print_error "Data directory not found: $DATA_DIR"
        exit 1
    fi
    
    # Drop existing tables (optional)
    if [ -f "$DATA_DIR/schema/00_drop_tables.sql" ]; then
        print_status "Dropping existing tables..."
        psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_ADMIN_ENERGY_USER" -d "$DB_NAME_ENERGY" -f "$DATA_DIR/schema/00_drop_tables.sql"
    fi
    
    # Create schema
    if [ -f "$DATA_DIR/schema/03_redaptive_energy_schema_enhanced.sql" ]; then
        print_status "Creating enhanced energy schema..."
        psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_ADMIN_ENERGY_USER" -d "$DB_NAME_ENERGY" -f "$DATA_DIR/schema/03_redaptive_energy_schema_enhanced.sql"
        print_success "Enhanced energy schema created"
    elif [ -f "$DATA_DIR/schema/03_redaptive_energy_schema.sql" ]; then
        print_status "Creating energy schema..."
        psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_ADMIN_ENERGY_USER" -d "$DB_NAME_ENERGY" -f "$DATA_DIR/schema/03_redaptive_energy_schema.sql"
        print_success "Energy schema created"
    else
        print_error "No energy schema file found"
        exit 1
    fi
    
    # Insert sample data
    for seed_file in "$DATA_DIR/seed"/04_redaptive_sample_data*.sql; do
        if [ -f "$seed_file" ]; then
            print_status "Loading sample data: $(basename "$seed_file")"
            psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_ADMIN_ENERGY_USER" -d "$DB_NAME_ENERGY" -f "$seed_file"
        fi
    done
    
    print_success "Sample data loaded"
}

# Function to set permissions
set_permissions() {
    print_status "Setting database permissions..."
    
    # Grant permissions to app user
    psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_ADMIN_ENERGY_USER" -d "$DB_NAME_ENERGY" -c "
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_APP_USER;
        GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_APP_USER;
        GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO $DB_APP_USER;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_APP_USER;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_APP_USER;
    "
    
    print_success "Permissions set for $DB_APP_USER"
}

# Function to verify setup
verify_setup() {
    print_status "Verifying database setup..."
    
    # Count tables
    table_count=$(psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_APP_USER" -d "$DB_NAME_ENERGY" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
    print_success "Found $table_count tables"
    
    # Count portfolios
    if psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_APP_USER" -d "$DB_NAME_ENERGY" -c "SELECT COUNT(*) FROM portfolios;" &> /dev/null; then
        portfolio_count=$(psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_APP_USER" -d "$DB_NAME_ENERGY" -t -c "SELECT COUNT(*) FROM portfolios;")
        print_success "Found $portfolio_count portfolios"
    fi
    
    # Count buildings
    if psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_APP_USER" -d "$DB_NAME_ENERGY" -c "SELECT COUNT(*) FROM buildings;" &> /dev/null; then
        building_count=$(psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_APP_USER" -d "$DB_NAME_ENERGY" -t -c "SELECT COUNT(*) FROM buildings;")
        print_success "Found $building_count buildings"
    fi
    
    print_success "Database verification completed"
}

# Main execution
main() {
    print_status "Starting Redaptive Energy Database Setup"
    print_status "Project root: $PROJECT_ROOT"
    print_status "Data directory: $DATA_DIR"
    
    # Check prerequisites
    check_postgres
    
    # Setup database
    setup_database
    
    # Run SQL scripts
    run_sql_scripts
    
    # Set permissions
    set_permissions
    
    # Verify setup
    verify_setup
    
    print_success "Energy database setup completed successfully!"
    print_status "Database: $DB_NAME_ENERGY"
    print_status "User: $DB_APP_USER"
    print_status "Connection: $DB_HOST_ENERGY:$DB_PORT_ENERGY"
    
    print_status "To test the database, run:"
    print_status "  ./scripts/database/test_energy_db.sh"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --force)
            FORCE=true
            shift
            ;;
        --verify-only)
            verify_setup
            exit 0
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --force       Force recreation of database"
            echo "  --verify-only Only verify existing setup"
            echo "  --help        Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main function
main