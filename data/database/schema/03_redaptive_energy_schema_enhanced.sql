-- Enhanced Redaptive Energy Portfolio Database Schema
-- Energy-as-a-Service platform for Fortune 500 real estate portfolios
-- Mock database for development and testing with realistic scale

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Drop existing tables if they exist (for development)
DROP TABLE IF EXISTS energy_alerts CASCADE;
DROP TABLE IF EXISTS maintenance_records CASCADE;
DROP TABLE IF EXISTS weather_data CASCADE;
DROP TABLE IF EXISTS utility_bills CASCADE;
DROP TABLE IF EXISTS energy_usage CASCADE;
DROP TABLE IF EXISTS energy_meters CASCADE;
DROP TABLE IF EXISTS equipment CASCADE;
DROP TABLE IF EXISTS buildings CASCADE;
DROP TABLE IF EXISTS portfolios CASCADE;
DROP TABLE IF EXISTS energy_projects CASCADE;
DROP TABLE IF EXISTS project_opportunities CASCADE;
DROP TABLE IF EXISTS sustainability_reports CASCADE;
DROP TABLE IF EXISTS benchmark_data CASCADE;
DROP TABLE IF EXISTS market_rates CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table - Platform users and roles
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'energy_manager', 'field_engineer', 'executive', 'customer')),
    company VARCHAR(255),
    phone VARCHAR(20),
    timezone VARCHAR(50) DEFAULT 'America/Denver',
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Portfolios table - Fortune 500 customer portfolios
CREATE TABLE portfolios (
    portfolio_id VARCHAR(50) PRIMARY KEY,
    portfolio_name VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    headquarters_location VARCHAR(255),
    total_floor_area DECIMAL(15,2), -- square feet
    building_count INTEGER DEFAULT 0,
    annual_revenue DECIMAL(15,2), -- for Fortune 500 context
    employees INTEGER,
    primary_contact_id UUID REFERENCES users(user_id),
    billing_contact_email VARCHAR(255),
    sustainability_goals JSONB, -- net zero targets, etc.
    contract_start_date DATE,
    contract_end_date DATE,
    monthly_fee DECIMAL(10,2),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'pending', 'churned'))
);

-- Buildings table - Individual buildings in portfolios
CREATE TABLE buildings (
    building_id VARCHAR(50) PRIMARY KEY,
    portfolio_id VARCHAR(50) REFERENCES portfolios(portfolio_id),
    building_name VARCHAR(255) NOT NULL,
    building_type VARCHAR(50) NOT NULL, -- office, retail, warehouse, manufacturing, data_center, hospital, school
    floor_area DECIMAL(12,2) NOT NULL, -- square feet
    floors INTEGER DEFAULT 1,
    year_built INTEGER,
    year_renovated INTEGER,
    address VARCHAR(500),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    country VARCHAR(50) DEFAULT 'USA',
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    timezone VARCHAR(50) DEFAULT 'America/Denver',
    climate_zone VARCHAR(10), -- ASHRAE climate zones 1A-8B
    baseline_consumption_kwh DECIMAL(15,2), -- annual kWh
    baseline_cost_annual DECIMAL(12,2), -- annual $/year
    peak_demand_kw DECIMAL(10,2),
    operating_hours_per_day DECIMAL(4,2) DEFAULT 12,
    occupancy_max INTEGER, -- max occupants
    energy_star_score INTEGER CHECK (energy_star_score BETWEEN 1 AND 100),
    leed_certification VARCHAR(20), -- None, Certified, Silver, Gold, Platinum
    other_certifications VARCHAR(255),
    utility_provider_electric VARCHAR(255),
    utility_provider_gas VARCHAR(255),
    utility_account_electric VARCHAR(100),
    utility_account_gas VARCHAR(100),
    building_automation_system VARCHAR(100), -- BAS/BMS system
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Equipment table - HVAC and other major energy-consuming equipment
CREATE TABLE equipment (
    equipment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    equipment_name VARCHAR(255) NOT NULL,
    equipment_type VARCHAR(100) NOT NULL, -- HVAC, lighting, motors, chillers, boilers, etc.
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    capacity_rating VARCHAR(100), -- tons, HP, kW, etc.
    efficiency_rating VARCHAR(50), -- SEER, EER, COP, etc.
    installation_date DATE,
    last_maintenance_date DATE,
    warranty_expiration DATE,
    location_description VARCHAR(255),
    energy_type VARCHAR(20) DEFAULT 'electricity', -- electricity, gas, steam
    rated_power_kw DECIMAL(10,2),
    operating_schedule VARCHAR(255), -- business hours, 24/7, etc.
    maintenance_interval_months INTEGER DEFAULT 12,
    status VARCHAR(20) DEFAULT 'operational' CHECK (status IN ('operational', 'maintenance', 'offline', 'replaced')),
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Energy meters table - IoT devices tracking energy usage (12k+ meters)
CREATE TABLE energy_meters (
    meter_id VARCHAR(50) PRIMARY KEY,
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    equipment_id UUID REFERENCES equipment(equipment_id), -- optional equipment association
    meter_name VARCHAR(255),
    meter_type VARCHAR(50) NOT NULL, -- main, sub, equipment, circuit_level
    energy_type VARCHAR(20) NOT NULL, -- electricity, gas, steam, chilled_water, hot_water
    meter_location VARCHAR(255),
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    communication_protocol VARCHAR(50), -- BACnet, Modbus, Ethernet, wireless
    ip_address INET,
    installation_date DATE,
    calibration_date DATE,
    next_calibration_date DATE,
    accuracy_class VARCHAR(10), -- meter accuracy class
    ct_ratio VARCHAR(20), -- current transformer ratio for electrical meters
    multiplier DECIMAL(8,4) DEFAULT 1.0,
    units VARCHAR(20) NOT NULL, -- kWh, kW, therms, gallons, tons
    min_reading DECIMAL(15,4) DEFAULT 0,
    max_reading DECIMAL(15,4),
    last_reading_date TIMESTAMP,
    last_reading_value DECIMAL(15,4),
    data_quality_score DECIMAL(3,2) DEFAULT 1.0, -- 0.0 to 1.0
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'maintenance', 'error', 'offline')),
    sampling_interval_minutes INTEGER DEFAULT 15,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Weather data table - External weather conditions for analysis
CREATE TABLE weather_data (
    weather_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    reading_date TIMESTAMP NOT NULL,
    temperature_f DECIMAL(5,2),
    humidity_percent DECIMAL(5,2),
    solar_irradiance DECIMAL(8,2), -- W/m²
    wind_speed_mph DECIMAL(5,2),
    cloud_cover_percent DECIMAL(5,2),
    precipitation_inches DECIMAL(6,4),
    heating_degree_days DECIMAL(6,2),
    cooling_degree_days DECIMAL(6,2),
    data_source VARCHAR(100) DEFAULT 'NOAA', -- weather data provider
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_weather_building_date (building_id, reading_date)
);

-- Energy usage table - Time series energy consumption data (massive scale)
CREATE TABLE energy_usage (
    usage_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    meter_id VARCHAR(50) REFERENCES energy_meters(meter_id),
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    reading_date TIMESTAMP NOT NULL,
    energy_type VARCHAR(20) NOT NULL,
    energy_consumption DECIMAL(15,6) NOT NULL, -- kWh, therms, etc.
    energy_cost DECIMAL(12,6), -- USD
    rate_schedule VARCHAR(50), -- utility rate schedule
    demand_kw DECIMAL(12,4), -- peak demand in kW (for electricity)
    power_factor DECIMAL(4,3), -- power factor (for electricity)
    voltage_v DECIMAL(8,2), -- average voltage
    current_a DECIMAL(10,4), -- average current
    frequency_hz DECIMAL(6,3), -- frequency
    reactive_power_kvar DECIMAL(12,4), -- reactive power
    apparent_power_kva DECIMAL(12,4), -- apparent power
    thd_voltage_percent DECIMAL(5,2), -- total harmonic distortion
    thd_current_percent DECIMAL(5,2),
    weather_temp_f DECIMAL(5,2), -- outdoor temperature at time of reading
    occupancy_count INTEGER, -- actual occupants (if available)
    occupancy_percentage DECIMAL(5,2), -- building occupancy %
    is_holiday BOOLEAN DEFAULT false,
    is_weekend BOOLEAN DEFAULT false,
    time_of_use_period VARCHAR(20), -- peak, off_peak, shoulder
    data_quality VARCHAR(20) DEFAULT 'good', -- good, estimated, questionable, missing
    anomaly_score DECIMAL(5,4), -- ML-generated anomaly score (0-1)
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_building_date (building_id, reading_date),
    INDEX idx_meter_date (meter_id, reading_date),
    INDEX idx_energy_type_date (energy_type, reading_date),
    INDEX idx_anomaly_score (anomaly_score DESC)
);

-- Energy alerts table - Real-time monitoring alerts
CREATE TABLE energy_alerts (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    meter_id VARCHAR(50) REFERENCES energy_meters(meter_id),
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    alert_type VARCHAR(50) NOT NULL, -- anomaly, offline, high_usage, demand_spike, equipment_fault
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    detected_value DECIMAL(15,4),
    expected_value DECIMAL(15,4),
    threshold_value DECIMAL(15,4),
    confidence_score DECIMAL(3,2), -- ML confidence 0.0-1.0
    detection_timestamp TIMESTAMP NOT NULL,
    assigned_engineer_id UUID REFERENCES users(user_id),
    estimated_cost_impact DECIMAL(10,2), -- potential cost impact
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'acknowledged', 'investigating', 'resolved', 'false_positive')),
    resolution_notes TEXT,
    resolved_by_id UUID REFERENCES users(user_id),
    resolved_timestamp TIMESTAMP,
    escalation_level INTEGER DEFAULT 1,
    notification_sent BOOLEAN DEFAULT false,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_alerts_status_severity (status, severity),
    INDEX idx_alerts_building_detection (building_id, detection_timestamp DESC)
);

-- Utility bills table - Monthly utility bills for validation
CREATE TABLE utility_bills (
    bill_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    utility_type VARCHAR(20) NOT NULL, -- electric, gas, water, steam
    utility_company VARCHAR(255) NOT NULL,
    account_number VARCHAR(100),
    bill_date DATE NOT NULL,
    service_period_start DATE NOT NULL,
    service_period_end DATE NOT NULL,
    total_usage DECIMAL(15,4) NOT NULL,
    total_cost DECIMAL(12,2) NOT NULL,
    usage_units VARCHAR(20) NOT NULL, -- kWh, therms, gallons
    rate_schedule VARCHAR(100),
    demand_charge DECIMAL(10,2),
    energy_charge DECIMAL(10,2),
    delivery_charge DECIMAL(10,2),
    taxes_and_fees DECIMAL(10,2),
    late_fees DECIMAL(8,2) DEFAULT 0,
    peak_demand_kw DECIMAL(10,2),
    power_factor DECIMAL(4,3),
    fuel_adjustment DECIMAL(8,4),
    renewable_energy_credit DECIMAL(8,2),
    bill_document_path VARCHAR(500), -- path to scanned bill PDF
    processed_by_ai BOOLEAN DEFAULT false,
    extraction_confidence DECIMAL(3,2), -- AI extraction confidence
    validation_status VARCHAR(20) DEFAULT 'pending' CHECK (validation_status IN ('pending', 'validated', 'discrepancy', 'manual_review')),
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_bills_building_date (building_id, bill_date DESC)
);

-- Market rates table - Energy market pricing data
CREATE TABLE market_rates (
    rate_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    region VARCHAR(100) NOT NULL, -- ISO/RTO region: ERCOT, CAISO, PJM, etc.
    utility_company VARCHAR(255),
    rate_type VARCHAR(50) NOT NULL, -- electricity, natural_gas, carbon_credit, renewable_credit
    rate_schedule VARCHAR(100), -- tariff schedule name
    customer_class VARCHAR(50), -- commercial, industrial, residential
    time_of_use_period VARCHAR(20), -- peak, off_peak, shoulder, super_off_peak
    effective_date DATE NOT NULL,
    expiration_date DATE,
    energy_rate DECIMAL(10,6), -- $/kWh or $/therm
    demand_rate DECIMAL(10,4), -- $/kW
    connection_fee DECIMAL(8,2),
    delivery_rate DECIMAL(10,6),
    transmission_rate DECIMAL(10,6),
    distribution_rate DECIMAL(10,6),
    renewable_portfolio_rate DECIMAL(10,6),
    carbon_price DECIMAL(8,4), -- $/ton CO2
    tier_threshold DECIMAL(12,2), -- usage threshold for tiered rates
    tier_number INTEGER DEFAULT 1,
    minimum_bill DECIMAL(8,2),
    maximum_bill DECIMAL(12,2),
    seasonal_adjustment DECIMAL(6,4) DEFAULT 1.0,
    data_source VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_rates_region_date (region, effective_date DESC),
    INDEX idx_rates_company_schedule (utility_company, rate_schedule)
);

-- Energy projects table - EaaS projects and implementations
CREATE TABLE energy_projects (
    project_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    project_name VARCHAR(255) NOT NULL,
    project_type VARCHAR(50) NOT NULL, -- LED_retrofit, HVAC_upgrade, solar_installation, battery_storage, etc.
    technology_description TEXT,
    vendor_name VARCHAR(255),
    equipment_ids UUID[], -- array of equipment IDs being upgraded/replaced
    installation_cost DECIMAL(15,2) NOT NULL,
    labor_cost DECIMAL(12,2),
    equipment_cost DECIMAL(12,2),
    permitting_cost DECIMAL(8,2),
    other_costs DECIMAL(10,2),
    financing_type VARCHAR(50), -- cash, loan, lease, ppa, eaas
    financing_term_years INTEGER,
    interest_rate DECIMAL(5,4),
    annual_savings_kwh DECIMAL(15,2),
    annual_savings_cost DECIMAL(12,2),
    monthly_savings_cost DECIMAL(10,2),
    peak_demand_reduction_kw DECIMAL(10,2),
    project_roi DECIMAL(6,3), -- return on investment ratio
    payback_years DECIMAL(5,2),
    npv_20_year DECIMAL(15,2), -- net present value over 20 years
    irr_percent DECIMAL(5,2), -- internal rate of return
    carbon_reduction_tons_annual DECIMAL(10,2), -- tons CO2 reduced annually
    rebates_available DECIMAL(10,2), -- utility rebates
    tax_credits_available DECIMAL(10,2), -- federal/state tax credits
    project_status VARCHAR(20) DEFAULT 'planned' CHECK (project_status IN 
        ('planned', 'design', 'approved', 'procurement', 'installation', 'commissioning', 'completed', 'cancelled')),
    planned_start_date DATE,
    actual_start_date DATE,
    planned_completion_date DATE,
    actual_completion_date DATE,
    warranty_years INTEGER DEFAULT 5,
    maintenance_contract BOOLEAN DEFAULT false,
    performance_guarantee_years INTEGER,
    savings_guarantee_percent DECIMAL(5,2),
    project_manager_id UUID REFERENCES users(user_id),
    installation_contractor VARCHAR(255),
    commissioning_agent VARCHAR(255),
    milestone_data JSONB, -- project milestones and status
    risk_factors TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Maintenance records table - Equipment maintenance tracking
CREATE TABLE maintenance_records (
    maintenance_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    equipment_id UUID REFERENCES equipment(equipment_id),
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    maintenance_type VARCHAR(50) NOT NULL, -- preventive, corrective, emergency, inspection
    work_order_number VARCHAR(100),
    scheduled_date DATE,
    actual_date DATE,
    technician_name VARCHAR(255),
    contractor_company VARCHAR(255),
    description TEXT NOT NULL,
    work_performed TEXT,
    parts_replaced TEXT,
    labor_hours DECIMAL(5,2),
    labor_cost DECIMAL(8,2),
    parts_cost DECIMAL(8,2),
    total_cost DECIMAL(10,2),
    downtime_hours DECIMAL(6,2),
    next_maintenance_date DATE,
    equipment_condition VARCHAR(20) CHECK (equipment_condition IN ('excellent', 'good', 'fair', 'poor', 'critical')),
    efficiency_impact DECIMAL(5,2), -- % efficiency change
    notes TEXT,
    photos_path VARCHAR(500),
    completion_status VARCHAR(20) DEFAULT 'completed' CHECK (completion_status IN ('scheduled', 'in_progress', 'completed', 'cancelled')),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Project opportunities table - Identified energy efficiency opportunities  
CREATE TABLE project_opportunities (
    opportunity_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id VARCHAR(50) REFERENCES buildings(building_id),
    opportunity_type VARCHAR(50) NOT NULL,
    opportunity_category VARCHAR(50) NOT NULL, -- lighting, hvac, envelope, controls, renewable, storage
    title VARCHAR(255) NOT NULL,
    description TEXT,
    identified_by VARCHAR(100) DEFAULT 'portfolio-intelligence-agent',
    analysis_method VARCHAR(100), -- energy_audit, ml_analysis, benchmark_comparison, etc.
    confidence_level VARCHAR(20) CHECK (confidence_level IN ('low', 'medium', 'high')),
    estimated_cost DECIMAL(15,2),
    cost_accuracy VARCHAR(20) DEFAULT 'rough' CHECK (cost_accuracy IN ('rough', 'budget', 'detailed')),
    annual_savings_kwh DECIMAL(15,2),
    annual_savings_cost DECIMAL(12,2),
    demand_reduction_kw DECIMAL(10,2),
    estimated_roi DECIMAL(6,3),
    payback_years DECIMAL(5,2),
    carbon_reduction_tons DECIMAL(10,2),
    additional_benefits TEXT, -- comfort, reliability, etc.
    implementation_complexity VARCHAR(20) CHECK (implementation_complexity IN ('low', 'medium', 'high')),
    estimated_duration_weeks INTEGER,
    prerequisites TEXT,
    potential_rebates DECIMAL(10,2),
    utility_programs VARCHAR(255),
    priority_score INTEGER CHECK (priority_score BETWEEN 1 AND 100),
    market_maturity VARCHAR(20) CHECK (market_maturity IN ('emerging', 'developing', 'mature')),
    technology_risk VARCHAR(20) CHECK (technology_risk IN ('low', 'medium', 'high')),
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_by_id UUID REFERENCES users(user_id),
    review_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'identified' CHECK (status IN 
        ('identified', 'under_review', 'approved', 'rejected', 'converted_to_project', 'on_hold'))
);

-- Sustainability reports table - ESG and sustainability reporting
CREATE TABLE sustainability_reports (
    report_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id VARCHAR(50) REFERENCES portfolios(portfolio_id),
    building_id VARCHAR(50) REFERENCES buildings(building_id), -- NULL for portfolio-level reports
    report_type VARCHAR(50) NOT NULL, -- executive, detailed, regulatory, investor, monthly, annual
    report_format VARCHAR(30) DEFAULT 'executive' CHECK (report_format IN ('executive', 'detailed', 'dashboard', 'regulatory')),
    reporting_period_start DATE NOT NULL,
    reporting_period_end DATE NOT NULL,
    total_energy_consumption_kwh DECIMAL(20,2), -- kWh
    total_energy_cost DECIMAL(15,2), -- USD
    electricity_consumption_kwh DECIMAL(20,2),
    gas_consumption_therms DECIMAL(15,2),
    steam_consumption_mmbtu DECIMAL(15,2),
    water_consumption_gallons DECIMAL(15,2),
    renewable_energy_kwh DECIMAL(20,2),
    renewable_energy_percent DECIMAL(5,2),
    total_carbon_emissions_tons DECIMAL(12,2), -- tons CO2
    scope_1_emissions DECIMAL(12,2), -- direct emissions
    scope_2_emissions DECIMAL(12,2), -- indirect emissions from electricity
    scope_3_emissions DECIMAL(12,2), -- other indirect emissions
    carbon_intensity_per_sqft DECIMAL(8,4), -- tons CO2/sqft
    energy_intensity_kwh_per_sqft DECIMAL(8,2), -- kWh/sqft
    energy_cost_per_sqft DECIMAL(6,2), -- $/sqft
    energy_star_avg_score DECIMAL(5,2),
    leed_buildings_count INTEGER DEFAULT 0,
    green_certified_area_sqft DECIMAL(15,2),
    projects_completed INTEGER DEFAULT 0,
    projects_in_progress INTEGER DEFAULT 0,
    total_savings_kwh DECIMAL(20,2),
    total_savings_cost DECIMAL(15,2),
    carbon_reduction_tons DECIMAL(12,2),
    water_savings_gallons DECIMAL(15,2),
    waste_diverted_tons DECIMAL(10,2),
    benchmark_percentile INTEGER, -- compared to industry
    year_over_year_improvement DECIMAL(5,2), -- % improvement
    sustainability_goals_met INTEGER DEFAULT 0,
    sustainability_goals_total INTEGER DEFAULT 0,
    report_data JSONB, -- flexible storage for detailed report data
    charts_and_graphs JSONB, -- visualization data
    executive_summary TEXT,
    key_findings TEXT,
    recommendations TEXT,
    methodology_notes TEXT,
    data_quality_score DECIMAL(3,2) DEFAULT 1.0,
    generated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    generated_by VARCHAR(100) DEFAULT 'portfolio-intelligence-agent',
    reviewed_by_id UUID REFERENCES users(user_id),
    review_date TIMESTAMP,
    approval_status VARCHAR(20) DEFAULT 'draft' CHECK (approval_status IN ('draft', 'review', 'approved', 'published'))
);

-- Benchmark data table - Industry benchmarking information
CREATE TABLE benchmark_data (
    benchmark_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_type VARCHAR(50) NOT NULL,
    climate_zone VARCHAR(10),
    region VARCHAR(100),
    benchmark_type VARCHAR(50) NOT NULL, -- energy_star, cbecs, boma, ashrae
    energy_use_intensity DECIMAL(8,2), -- kWh/sqft/year
    energy_cost_intensity DECIMAL(6,2), -- $/sqft/year  
    carbon_intensity DECIMAL(8,4), -- kg CO2/sqft/year
    water_intensity DECIMAL(8,2), -- gallons/sqft/year
    percentile_10 DECIMAL(8,2),
    percentile_25 DECIMAL(8,2),
    percentile_50 DECIMAL(8,2), -- median
    percentile_75 DECIMAL(8,2),
    percentile_90 DECIMAL(8,2),
    sample_size INTEGER,
    floor_area_min DECIMAL(12,2), -- sqft
    floor_area_max DECIMAL(12,2), -- sqft
    operating_hours_min DECIMAL(4,1),
    operating_hours_max DECIMAL(4,1),
    data_year INTEGER,
    source VARCHAR(100),
    methodology VARCHAR(255),
    data_quality VARCHAR(20) DEFAULT 'good',
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_benchmark_type_region (building_type, region),
    INDEX idx_benchmark_data_year (data_year DESC)
);

-- Create advanced indexes for performance at scale
CREATE INDEX idx_portfolios_company ON portfolios(company_name);
CREATE INDEX idx_portfolios_industry_status ON portfolios(industry, status);
CREATE INDEX idx_buildings_portfolio ON buildings(portfolio_id);
CREATE INDEX idx_buildings_type_location ON buildings(building_type, city, state);
CREATE INDEX idx_buildings_energy_star ON buildings(energy_star_score DESC) WHERE energy_star_score IS NOT NULL;
CREATE INDEX idx_equipment_building_type ON equipment(building_id, equipment_type);
CREATE INDEX idx_meters_building_type ON energy_meters(building_id, energy_type);
CREATE INDEX idx_meters_status_location ON energy_meters(status, meter_location) WHERE status = 'active';
CREATE INDEX idx_usage_building_date_type ON energy_usage(building_id, reading_date DESC, energy_type);
CREATE INDEX idx_usage_meter_date_consumption ON energy_usage(meter_id, reading_date DESC, energy_consumption);
CREATE INDEX idx_usage_anomaly_high ON energy_usage(anomaly_score DESC, building_id) WHERE anomaly_score > 0.7;
CREATE INDEX idx_alerts_open_critical ON energy_alerts(building_id, detection_timestamp DESC) WHERE status = 'open' AND severity IN ('high', 'critical');
CREATE INDEX idx_bills_building_type_date ON utility_bills(building_id, utility_type, bill_date DESC);
CREATE INDEX idx_projects_building_status_type ON energy_projects(building_id, project_status, project_type);
CREATE INDEX idx_projects_roi_payback ON energy_projects(project_roi DESC, payback_years) WHERE project_status = 'completed';
CREATE INDEX idx_opportunities_building_priority ON project_opportunities(building_id, priority_score DESC, status);
CREATE INDEX idx_opportunities_type_roi ON project_opportunities(opportunity_type, estimated_roi DESC) WHERE status IN ('identified', 'approved');
CREATE INDEX idx_reports_portfolio_date ON sustainability_reports(portfolio_id, reporting_period_end DESC);
CREATE INDEX idx_maintenance_equipment_date ON maintenance_records(equipment_id, actual_date DESC);

-- Create GIN indexes for JSONB columns
CREATE INDEX idx_sustainability_report_data ON sustainability_reports USING GIN (report_data);
CREATE INDEX idx_portfolio_goals ON portfolios USING GIN (sustainability_goals);
CREATE INDEX idx_project_milestones ON energy_projects USING GIN (milestone_data);

-- Create views for common queries and dashboards

-- Real-time portfolio dashboard view
CREATE VIEW portfolio_dashboard AS
SELECT 
    p.portfolio_id,
    p.portfolio_name,
    p.company_name,
    p.industry,
    COUNT(DISTINCT b.building_id) as building_count,
    SUM(b.floor_area) as total_floor_area,
    AVG(b.energy_star_score) as avg_energy_star_score,
    COUNT(DISTINCT CASE WHEN em.status = 'active' THEN em.meter_id END) as active_meters,
    COUNT(DISTINCT CASE WHEN ea.status = 'open' AND ea.severity IN ('high', 'critical') THEN ea.alert_id END) as critical_alerts,
    COUNT(DISTINCT CASE WHEN ep.project_status = 'completed' THEN ep.project_id END) as completed_projects,
    SUM(CASE WHEN ep.project_status = 'completed' THEN ep.annual_savings_cost ELSE 0 END) as total_annual_savings,
    COUNT(DISTINCT CASE WHEN po.status IN ('identified', 'approved') THEN po.opportunity_id END) as active_opportunities,
    SUM(CASE WHEN po.status IN ('identified', 'approved') THEN po.annual_savings_cost ELSE 0 END) as opportunity_savings_potential
FROM portfolios p
LEFT JOIN buildings b ON p.portfolio_id = b.portfolio_id
LEFT JOIN energy_meters em ON b.building_id = em.building_id
LEFT JOIN energy_alerts ea ON b.building_id = ea.building_id AND ea.created_date >= CURRENT_DATE - INTERVAL '30 days'
LEFT JOIN energy_projects ep ON b.building_id = ep.building_id
LEFT JOIN project_opportunities po ON b.building_id = po.building_id
WHERE p.status = 'active'
GROUP BY p.portfolio_id, p.portfolio_name, p.company_name, p.industry;

-- Building energy performance view with latest data
CREATE VIEW building_energy_performance AS
SELECT 
    b.building_id,
    b.building_name,
    b.portfolio_id,
    b.building_type,
    b.floor_area,
    b.energy_star_score,
    COUNT(DISTINCT em.meter_id) as meter_count,
    COUNT(DISTINCT CASE WHEN em.status = 'active' THEN em.meter_id END) as active_meters,
    latest_usage.avg_monthly_consumption_kwh,
    latest_usage.avg_monthly_cost,
    latest_usage.consumption_per_sqft,
    latest_usage.cost_per_sqft,
    latest_usage.last_reading_date,
    latest_usage.data_quality_avg,
    COUNT(CASE WHEN ea.status = 'open' AND ea.severity IN ('high', 'critical') THEN 1 END) as open_critical_alerts
FROM buildings b
LEFT JOIN energy_meters em ON b.building_id = em.building_id
LEFT JOIN (
    SELECT 
        building_id,
        AVG(energy_consumption) as avg_monthly_consumption_kwh,
        AVG(energy_cost) as avg_monthly_cost,
        MAX(reading_date) as last_reading_date,
        AVG(CASE WHEN data_quality = 'good' THEN 1.0 WHEN data_quality = 'estimated' THEN 0.8 ELSE 0.5 END) as data_quality_avg
    FROM energy_usage
    WHERE reading_date >= CURRENT_DATE - INTERVAL '12 months'
    GROUP BY building_id
) latest_usage ON b.building_id = latest_usage.building_id
LEFT JOIN energy_alerts ea ON b.building_id = ea.building_id AND ea.created_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 
    b.building_id, b.building_name, b.portfolio_id, b.building_type, b.floor_area, b.energy_star_score,
    latest_usage.avg_monthly_consumption_kwh, latest_usage.avg_monthly_cost, 
    latest_usage.consumption_per_sqft, latest_usage.cost_per_sqft, 
    latest_usage.last_reading_date, latest_usage.data_quality_avg;

-- Energy opportunity pipeline with ROI analysis
CREATE VIEW opportunity_pipeline AS
SELECT 
    po.building_id,
    b.building_name,
    b.portfolio_id,
    po.opportunity_type,
    po.opportunity_category,
    COUNT(*) as opportunity_count,
    SUM(po.estimated_cost) as total_estimated_cost,
    SUM(po.annual_savings_cost) as total_annual_savings,
    AVG(po.estimated_roi) as avg_roi,
    AVG(po.payback_years) as avg_payback_years,
    SUM(po.carbon_reduction_tons) as total_carbon_reduction,
    AVG(po.priority_score) as avg_priority_score,
    COUNT(CASE WHEN po.confidence_level = 'high' THEN 1 END) as high_confidence_count,
    SUM(CASE WHEN po.confidence_level = 'high' THEN po.annual_savings_cost ELSE 0 END) as high_confidence_savings
FROM project_opportunities po
JOIN buildings b ON po.building_id = b.building_id
WHERE po.status IN ('identified', 'under_review', 'approved')
GROUP BY po.building_id, b.building_name, b.portfolio_id, po.opportunity_type, po.opportunity_category;

-- Alert summary for operations dashboard
CREATE VIEW alert_summary AS
SELECT 
    ea.building_id,
    b.building_name,
    b.portfolio_id,
    ea.alert_type,
    ea.severity,
    COUNT(*) as alert_count,
    MIN(ea.detection_timestamp) as earliest_alert,
    MAX(ea.detection_timestamp) as latest_alert,
    AVG(ea.confidence_score) as avg_confidence,
    COUNT(CASE WHEN ea.assigned_engineer_id IS NOT NULL THEN 1 END) as assigned_count,
    SUM(ea.estimated_cost_impact) as total_estimated_impact
FROM energy_alerts ea
JOIN buildings b ON ea.building_id = b.building_id
WHERE ea.status IN ('open', 'acknowledged', 'investigating')
  AND ea.detection_timestamp >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY ea.building_id, b.building_name, b.portfolio_id, ea.alert_type, ea.severity;

-- Monthly energy summary for reporting
CREATE VIEW monthly_energy_summary AS
SELECT 
    b.building_id,
    b.building_name,
    b.portfolio_id,
    DATE_TRUNC('month', eu.reading_date) as month,
    eu.energy_type,
    SUM(eu.energy_consumption) as total_consumption,
    SUM(eu.energy_cost) as total_cost,
    AVG(eu.demand_kw) as avg_demand_kw,
    MAX(eu.demand_kw) as peak_demand_kw,
    AVG(eu.weather_temp_f) as avg_temperature,
    COUNT(*) as reading_count,
    AVG(CASE WHEN eu.data_quality = 'good' THEN 1.0 WHEN eu.data_quality = 'estimated' THEN 0.8 ELSE 0.5 END) as data_quality_score
FROM energy_usage eu
JOIN buildings b ON eu.building_id = b.building_id
WHERE eu.reading_date >= CURRENT_DATE - INTERVAL '24 months'
GROUP BY b.building_id, b.building_name, b.portfolio_id, DATE_TRUNC('month', eu.reading_date), eu.energy_type;

-- Add comprehensive table comments for documentation
COMMENT ON TABLE users IS 'Platform users with role-based access control';
COMMENT ON TABLE portfolios IS 'Fortune 500 customer real estate portfolios with contract details';
COMMENT ON TABLE buildings IS 'Individual buildings within customer portfolios with detailed characteristics';
COMMENT ON TABLE equipment IS 'Major energy-consuming equipment (HVAC, lighting, motors, etc.)';
COMMENT ON TABLE energy_meters IS 'IoT energy monitoring devices (supporting 12k+ meters)';
COMMENT ON TABLE weather_data IS 'External weather conditions for energy analysis correlation';
COMMENT ON TABLE energy_usage IS 'Time series energy consumption data with quality metrics and anomaly scores';
COMMENT ON TABLE energy_alerts IS 'Real-time monitoring alerts for anomalies and equipment issues';
COMMENT ON TABLE utility_bills IS 'Monthly utility bills for cost validation and benchmarking';
COMMENT ON TABLE market_rates IS 'Energy market pricing data for cost optimization';
COMMENT ON TABLE energy_projects IS 'EaaS energy efficiency and renewable projects with financial analysis';
COMMENT ON TABLE maintenance_records IS 'Equipment maintenance tracking for predictive maintenance';
COMMENT ON TABLE project_opportunities IS 'Identified energy optimization opportunities with ROI analysis';
COMMENT ON TABLE sustainability_reports IS 'ESG and sustainability performance reports with detailed metrics';
COMMENT ON TABLE benchmark_data IS 'Industry benchmarking reference data for performance comparison';

-- Functions for common calculations

-- Function to calculate energy intensity
CREATE OR REPLACE FUNCTION calculate_energy_intensity(building_id_param VARCHAR(50), start_date DATE, end_date DATE)
RETURNS DECIMAL(8,2) AS $$
DECLARE
    total_consumption DECIMAL(20,2);
    building_area DECIMAL(12,2);
    days_in_period INTEGER;
    annual_intensity DECIMAL(8,2);
BEGIN
    -- Get total consumption for period
    SELECT COALESCE(SUM(energy_consumption), 0) INTO total_consumption
    FROM energy_usage 
    WHERE building_id = building_id_param 
      AND reading_date BETWEEN start_date AND end_date
      AND energy_type = 'electricity';
    
    -- Get building floor area
    SELECT floor_area INTO building_area
    FROM buildings 
    WHERE building_id = building_id_param;
    
    -- Calculate days in period
    SELECT (end_date - start_date) + 1 INTO days_in_period;
    
    -- Annualize the intensity (kWh/sqft/year)
    IF building_area > 0 AND days_in_period > 0 THEN
        annual_intensity := (total_consumption / building_area) * (365.0 / days_in_period);
        RETURN annual_intensity;
    ELSE
        RETURN 0;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate carbon emissions
CREATE OR REPLACE FUNCTION calculate_carbon_emissions(energy_kwh DECIMAL(20,2), region VARCHAR(100) DEFAULT 'US_AVERAGE')
RETURNS DECIMAL(12,2) AS $$
DECLARE
    emission_factor DECIMAL(8,6);
    carbon_tons DECIMAL(12,2);
BEGIN
    -- Simplified emission factors (tons CO2/MWh)
    CASE region
        WHEN 'CAISO' THEN emission_factor := 0.233; -- California - cleaner grid
        WHEN 'ERCOT' THEN emission_factor := 0.366; -- Texas
        WHEN 'PJM' THEN emission_factor := 0.340; -- Mid-Atlantic
        WHEN 'NYISO' THEN emission_factor := 0.268; -- New York
        ELSE emission_factor := 0.386; -- US Average
    END CASE;
    
    -- Convert kWh to tons CO2
    carbon_tons := (energy_kwh / 1000.0) * emission_factor;
    RETURN carbon_tons;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions (adjust as needed for your environment)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO redaptive_user;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO redaptive_readonly;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO redaptive_user;

-- Create materialized views for performance (refresh periodically)
CREATE MATERIALIZED VIEW mv_daily_building_summary AS
SELECT 
    building_id,
    DATE(reading_date) as summary_date,
    energy_type,
    SUM(energy_consumption) as daily_consumption,
    SUM(energy_cost) as daily_cost,
    AVG(demand_kw) as avg_demand,
    MAX(demand_kw) as peak_demand,
    AVG(weather_temp_f) as avg_temperature,
    COUNT(*) as reading_count
FROM energy_usage
WHERE reading_date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY building_id, DATE(reading_date), energy_type;

CREATE UNIQUE INDEX ON mv_daily_building_summary (building_id, summary_date, energy_type);

-- Refresh materialized view daily (set up cron job or scheduled task)
-- REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_building_summary;