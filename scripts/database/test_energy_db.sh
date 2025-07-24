#!/bin/bash

# Database Test Script for Redaptive Energy Portfolio Management
# Tests database connectivity, schema, and sample data
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() { echo -e "${BLUE}🧪 $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# Database configuration
DB_NAME_ENERGY="energy_db"
DB_USER="energy_user"
DB_HOST_ENERGY="${DB_HOST_ENERGY:-localhost}"
DB_PORT_ENERGY="${DB_PORT_ENERGY:-5432}"

# Function to test database connection
test_connection() {
    print_status "Testing energy database connection..."
    
    if psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -c "SELECT 1;" &> /dev/null; then
        print_success "Database connection successful"
        return 0
    else
        print_error "Database connection failed"
        print_warning "Please ensure the database is set up and running"
        return 1
    fi
}

# Function to test database schema
test_schema() {
    print_status "Checking database tables..."
    
    # Get table count
    table_count=$(psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ')
    
    if [ "$table_count" -gt 0 ]; then
        print_success "Found $table_count tables"
    else
        print_error "No tables found"
        return 1
    fi
    
    # Check key tables exist
    key_tables=("portfolios" "buildings" "energy_meters" "energy_readings")
    for table in "${key_tables[@]}"; do
        if psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -c "SELECT 1 FROM $table LIMIT 1;" &> /dev/null; then
            print_success "Table '$table' exists and accessible"
        else
            print_warning "Table '$table' not found or not accessible"
        fi
    done
}

# Function to test sample data
test_data() {
    print_status "Checking energy data..."
    
    # Test portfolios
    if psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -c "SELECT COUNT(*) FROM portfolios;" &> /dev/null; then
        portfolio_count=$(psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -t -c "SELECT COUNT(*) FROM portfolios;" | tr -d ' ')
        print_success "Found $portfolio_count portfolios"
    fi
    
    # Test buildings
    if psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -c "SELECT COUNT(*) FROM buildings;" &> /dev/null; then
        building_count=$(psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -t -c "SELECT COUNT(*) FROM buildings;" | tr -d ' ')
        print_success "Found $building_count buildings"
    fi
    
    # Test energy meters
    if psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -c "SELECT COUNT(*) FROM energy_meters;" &> /dev/null; then
        meter_count=$(psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -t -c "SELECT COUNT(*) FROM energy_meters;" | tr -d ' ')
        print_success "Found $meter_count energy meters"
    fi
}

# Function to test specific queries
test_queries() {
    print_status "Testing facility search functionality..."
    
    # Test location-based search
    if psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -c "SELECT COUNT(*) FROM buildings WHERE city = 'Dallas';" &> /dev/null; then
        dallas_count=$(psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -t -c "SELECT COUNT(*) FROM buildings WHERE city = 'Dallas';" | tr -d ' ')
        print_success "Found $dallas_count buildings in Dallas"
    fi
    
    # Test type-based search
    if psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -c "SELECT COUNT(*) FROM buildings WHERE building_type = 'office';" &> /dev/null; then
        office_count=$(psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -t -c "SELECT COUNT(*) FROM buildings WHERE building_type = 'office';" | tr -d ' ')
        print_success "Found $office_count office buildings"
    fi
}

# Function to test agent functionality
test_agent_queries() {
    print_status "Testing agent-specific queries..."
    
    # Test portfolio analysis query
    if psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -c "
        SELECT p.name, COUNT(b.building_id) as building_count, 
               SUM(b.floor_area) as total_area
        FROM portfolios p 
        LEFT JOIN buildings b ON p.portfolio_id = b.portfolio_id 
        GROUP BY p.portfolio_id, p.name 
        LIMIT 1;
    " &> /dev/null; then
        print_success "Portfolio analysis queries working"
    else
        print_warning "Portfolio analysis queries need verification"
    fi
    
    # Test energy data aggregation
    if psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -c "
        SELECT DATE_TRUNC('month', reading_date) as month,
               SUM(energy_kwh) as total_kwh
        FROM energy_readings 
        WHERE reading_date >= CURRENT_DATE - INTERVAL '6 months'
        GROUP BY DATE_TRUNC('month', reading_date)
        ORDER BY month DESC
        LIMIT 3;
    " &> /dev/null; then
        print_success "Energy aggregation queries working"
    else
        print_warning "Energy aggregation queries need verification"
    fi
}

# Function to display database summary
show_summary() {
    print_status "Database Summary:"
    
    echo "Database: $DB_NAME_ENERGY"
    echo "Host: $DB_HOST_ENERGY:$DB_PORT_ENERGY"
    echo "User: $DB_USER"
    echo ""
    
    # Show table counts
    if test_connection; then
        echo "Table Summary:"
        psql -h "$DB_HOST_ENERGY" -p "$DB_PORT_ENERGY" -U "$DB_USER" -d "$DB_NAME_ENERGY" -c "
            SELECT schemaname, tablename, 
                   pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
            FROM pg_tables 
            WHERE schemaname = 'public' 
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
        " 2>/dev/null || echo "Could not retrieve table information"
    fi
}

# Main test execution
main() {
    print_status "Starting Redaptive Energy Database Tests"
    
    local test_passed=0
    local test_failed=0
    
    # Run connection test
    if test_connection; then
        ((test_passed++))
    else
        ((test_failed++))
        print_error "Cannot proceed without database connection"
        exit 1
    fi
    
    # Run schema tests
    if test_schema; then
        ((test_passed++))
    else
        ((test_failed++))
    fi
    
    # Run data tests
    if test_data; then
        ((test_passed++))
    else
        ((test_failed++))
    fi
    
    # Run query tests
    if test_queries; then
        ((test_passed++))
    else
        ((test_failed++))
    fi
    
    # Run agent query tests
    if test_agent_queries; then
        ((test_passed++))
    else
        ((test_failed++))
    fi
    
    # Show summary
    show_summary
    
    # Final results
    echo ""
    print_success "Tests passed: $test_passed"
    if [ $test_failed -gt 0 ]; then
        print_warning "Tests failed: $test_failed"
    fi
    
    if [ $test_failed -eq 0 ]; then
        print_success "✅ Database test completed successfully!"
        echo ""
        echo "The energy agent should now work correctly!"
    else
        print_warning "⚠️ Some tests failed. Please check the setup."
        exit 1
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --summary-only)
            show_summary
            exit 0
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --summary-only Show database summary only"
            echo "  --help         Show this help message"
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