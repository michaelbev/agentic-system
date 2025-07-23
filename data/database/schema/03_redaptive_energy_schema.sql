-- Redaptive Energy Portfolio Database Schema
-- Energy-as-a-Service platform for Fortune 500 real estate portfolios

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing tables if they exist (for development)
DROP TABLE IF EXISTS energy_usage CASCADE;
DROP TABLE IF EXISTS energy_meters CASCADE;
DROP TABLE IF EXISTS buildings CASCADE;
DROP TABLE IF EXISTS portfolios CASCADE;
DROP TABLE IF EXISTS energy_projects CASCADE;
DROP TABLE IF EXISTS project_opportunities CASCADE;
DROP TABLE IF EXISTS sustainability_reports CASCADE;
DROP TABLE IF EXISTS benchmark_data CASCADE;

-- Portfolios table - Fortune 500 customer portfolios
CREATE TABLE portfolios (
    portfolio_id VARCHAR(50) PRIMARY KEY,
    portfolio_name VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    total_floor_area DECIMAL(12,2), -- square feet
    building_count INTEGER DEFAULT 0,
    primary_contact_email VARCHAR(255),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'pending'))
);

-- Buildings table - Individual buildings in portfolios
CREATE TABLE buildings (
    building_id VARCHAR(50) PRIMARY KEY,
    portfolio_id VARCHAR(50) REFERENCES portfolios(portfolio_id),
    building_name VARCHAR(255) NOT NULL,
    building_type VARCHAR(50) NOT NULL, -- office, retail, warehouse, manufacturing, etc.
    floor_area DECIMAL(10,2) NOT NULL, -- square feet
    year_built INTEGER,
    location VARCHAR(255), -- city, state
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    timezone VARCHAR(50) DEFAULT 'America/Denver',
    baseline_consumption DECIMAL(12,2), -- kWh/month
    baseline_cost DECIMAL(10,2), -- $/month
    energy_star_score INTEGER CHECK (energy_star_score BETWEEN 1 AND 100),
    leed_certification VARCHAR(20),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Energy meters table - IoT devices tracking energy usage
CREATE TABLE energy_meters (
    meter_id VARCHAR(50) PRIMARY KEY,
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    meter_type VARCHAR(50) NOT NULL, -- main, sub, equipment-specific
    energy_type VARCHAR(20) NOT NULL, -- electricity, gas, steam, chilled_water
    meter_location VARCHAR(255),
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    installation_date DATE,
    last_reading_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'maintenance', 'error')),
    sampling_interval_minutes INTEGER DEFAULT 15,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Energy usage table - Time series energy consumption data
CREATE TABLE energy_usage (
    usage_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    meter_id VARCHAR(50) REFERENCES energy_meters(meter_id),
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    reading_date TIMESTAMP NOT NULL,
    energy_type VARCHAR(20) NOT NULL,
    energy_consumption DECIMAL(12,4) NOT NULL, -- kWh, therms, etc.
    energy_cost DECIMAL(10,4), -- USD
    demand_kw DECIMAL(10,4), -- peak demand in kW (for electricity)
    power_factor DECIMAL(4,3), -- power factor (for electricity)
    weather_temp_f DECIMAL(5,2), -- outdoor temperature
    occupancy_percentage DECIMAL(5,2), -- building occupancy %
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_building_date (building_id, reading_date),
    INDEX idx_meter_date (meter_id, reading_date),
    INDEX idx_energy_type_date (energy_type, reading_date)
);

-- Energy projects table - EaaS projects and implementations
CREATE TABLE energy_projects (
    project_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    project_name VARCHAR(255) NOT NULL,
    project_type VARCHAR(50) NOT NULL, -- LED, HVAC, solar, storage, etc.
    technology_description TEXT,
    installation_cost DECIMAL(12,2) NOT NULL,
    annual_savings_kwh DECIMAL(12,2),
    annual_savings_cost DECIMAL(10,2),
    project_roi DECIMAL(5,3), -- return on investment ratio
    payback_years DECIMAL(4,2),
    carbon_reduction_tons DECIMAL(8,2), -- tons CO2 reduced annually
    project_status VARCHAR(20) DEFAULT 'planned' CHECK (project_status IN 
        ('planned', 'approved', 'in_progress', 'completed', 'cancelled')),
    start_date DATE,
    completion_date DATE,
    warranty_years INTEGER,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Project opportunities table - Identified energy efficiency opportunities
CREATE TABLE project_opportunities (
    opportunity_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    opportunity_type VARCHAR(50) NOT NULL,
    description TEXT,
    estimated_cost DECIMAL(12,2),
    annual_savings DECIMAL(10,2),
    estimated_roi DECIMAL(5,3),
    payback_years DECIMAL(4,2),
    carbon_reduction_tons DECIMAL(8,2),
    implementation_complexity VARCHAR(20) CHECK (implementation_complexity IN ('low', 'medium', 'high')),
    priority_score INTEGER CHECK (priority_score BETWEEN 1 AND 100),
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'identified' CHECK (status IN 
        ('identified', 'under_review', 'approved', 'rejected', 'converted_to_project'))
);

-- Sustainability reports table - ESG and sustainability reporting
CREATE TABLE sustainability_reports (
    report_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id VARCHAR(50) REFERENCES portfolios(portfolio_id),
    report_type VARCHAR(50) NOT NULL, -- executive, detailed, regulatory, investor
    reporting_period_start DATE NOT NULL,
    reporting_period_end DATE NOT NULL,
    total_energy_consumption DECIMAL(15,2), -- kWh
    total_energy_cost DECIMAL(12,2), -- USD
    total_carbon_emissions DECIMAL(10,2), -- tons CO2
    scope_1_emissions DECIMAL(10,2), -- direct emissions
    scope_2_emissions DECIMAL(10,2), -- indirect emissions from electricity
    energy_intensity DECIMAL(8,4), -- kWh/sqft
    carbon_intensity DECIMAL(8,4), -- tons CO2/sqft
    energy_star_avg_score DECIMAL(5,2),
    projects_completed INTEGER DEFAULT 0,
    total_savings_kwh DECIMAL(15,2),
    total_savings_cost DECIMAL(12,2),
    report_data JSONB, -- flexible storage for detailed report data
    generated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    generated_by VARCHAR(100) DEFAULT 'portfolio-intelligence-agent'
);

-- Benchmark data table - Industry benchmarking information
CREATE TABLE benchmark_data (
    benchmark_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_type VARCHAR(50) NOT NULL,
    region VARCHAR(100),
    benchmark_type VARCHAR(50) NOT NULL, -- energy_star, cbecs, industry
    energy_use_intensity DECIMAL(8,2), -- kWh/sqft/year
    carbon_intensity DECIMAL(8,4), -- kg CO2/sqft/year
    cost_per_sqft DECIMAL(6,2), -- $/sqft/year
    percentile_25 DECIMAL(8,2),
    percentile_50 DECIMAL(8,2), -- median
    percentile_75 DECIMAL(8,2),
    sample_size INTEGER,
    data_year INTEGER,
    source VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_portfolios_company ON portfolios(company_name);
CREATE INDEX idx_buildings_portfolio ON buildings(portfolio_id);
CREATE INDEX idx_buildings_type_location ON buildings(building_type, location);
CREATE INDEX idx_energy_usage_building_date ON energy_usage(building_id, reading_date DESC);
CREATE INDEX idx_energy_usage_type_date ON energy_usage(energy_type, reading_date DESC);
CREATE INDEX idx_energy_meters_building ON energy_meters(building_id);
CREATE INDEX idx_projects_building_status ON energy_projects(building_id, project_status);
CREATE INDEX idx_opportunities_building_priority ON project_opportunities(building_id, priority_score DESC);
CREATE INDEX idx_reports_portfolio_date ON sustainability_reports(portfolio_id, reporting_period_end DESC);

-- Create views for common queries

-- Portfolio summary view
CREATE VIEW portfolio_summary AS
SELECT 
    p.portfolio_id,
    p.portfolio_name,
    p.company_name,
    p.industry,
    COUNT(b.building_id) as building_count,
    SUM(b.floor_area) as total_floor_area,
    AVG(b.energy_star_score) as avg_energy_star_score,
    COUNT(ep.project_id) as total_projects,
    SUM(ep.annual_savings_cost) as total_annual_savings
FROM portfolios p
LEFT JOIN buildings b ON p.portfolio_id = b.portfolio_id
LEFT JOIN energy_projects ep ON b.building_id = ep.building_id AND ep.project_status = 'completed'
GROUP BY p.portfolio_id, p.portfolio_name, p.company_name, p.industry;

-- Building energy performance view
CREATE VIEW building_energy_performance AS
SELECT 
    b.building_id,
    b.building_name,
    b.building_type,
    b.floor_area,
    AVG(eu.energy_consumption) as avg_monthly_consumption,
    AVG(eu.energy_cost) as avg_monthly_cost,
    (AVG(eu.energy_consumption) / b.floor_area) as consumption_per_sqft,
    (AVG(eu.energy_cost) / b.floor_area) as cost_per_sqft,
    COUNT(eu.usage_id) as reading_count,
    MAX(eu.reading_date) as last_reading_date
FROM buildings b
LEFT JOIN energy_usage eu ON b.building_id = eu.building_id
WHERE eu.reading_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY b.building_id, b.building_name, b.building_type, b.floor_area;

-- Energy opportunity pipeline view
CREATE VIEW opportunity_pipeline AS
SELECT 
    po.building_id,
    b.building_name,
    po.opportunity_type,
    COUNT(*) as opportunity_count,
    SUM(po.estimated_cost) as total_estimated_cost,
    SUM(po.annual_savings) as total_annual_savings,
    AVG(po.estimated_roi) as avg_roi,
    AVG(po.payback_years) as avg_payback_years,
    SUM(po.carbon_reduction_tons) as total_carbon_reduction
FROM project_opportunities po
JOIN buildings b ON po.building_id = b.building_id
WHERE po.status IN ('identified', 'under_review', 'approved')
GROUP BY po.building_id, b.building_name, po.opportunity_type;

-- Add comments for documentation
COMMENT ON TABLE portfolios IS 'Fortune 500 customer real estate portfolios';
COMMENT ON TABLE buildings IS 'Individual buildings within customer portfolios';
COMMENT ON TABLE energy_meters IS 'IoT energy monitoring devices (12k+ meters)';
COMMENT ON TABLE energy_usage IS 'Time series energy consumption data from meters';
COMMENT ON TABLE energy_projects IS 'EaaS energy efficiency and renewable projects';
COMMENT ON TABLE project_opportunities IS 'Identified energy optimization opportunities';
COMMENT ON TABLE sustainability_reports IS 'ESG and sustainability performance reports';
COMMENT ON TABLE benchmark_data IS 'Industry benchmarking reference data';

-- Grant permissions (adjust as needed for your environment)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO redaptive_user;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO redaptive_readonly;