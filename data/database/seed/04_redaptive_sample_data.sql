-- Redaptive Energy Portfolio Sample Data
-- Sample data for testing the Portfolio Intelligence Agent

-- Insert sample portfolios (Fortune 500 companies)
INSERT INTO portfolios (portfolio_id, portfolio_name, company_name, industry, total_floor_area, building_count, primary_contact_email) VALUES
('PORTFOLIO-001', 'Microsoft Global Offices', 'Microsoft Corporation', 'Technology', 15000000, 50, 'sustainability@microsoft.com'),
('PORTFOLIO-002', 'Walmart Store Network', 'Walmart Inc.', 'Retail', 45000000, 150, 'energy@walmart.com'),
('PORTFOLIO-003', 'JPMorgan Chase Properties', 'JPMorgan Chase & Co.', 'Financial Services', 8500000, 35, 'facilities@jpmorgan.com'),
('PORTFOLIO-004', 'General Motors Facilities', 'General Motors Company', 'Automotive', 12000000, 25, 'energy@gm.com'),
('PORTFOLIO-005', 'Amazon Distribution Centers', 'Amazon.com Inc.', 'E-commerce', 32000000, 75, 'sustainability@amazon.com');

-- Insert sample buildings
INSERT INTO buildings (building_id, portfolio_id, building_name, building_type, floor_area, year_built, location, latitude, longitude, baseline_consumption, baseline_cost, energy_star_score) VALUES
-- Microsoft buildings
('BLDG-MS-001', 'PORTFOLIO-001', 'Microsoft Campus Building 1', 'office', 450000, 2015, 'Redmond, WA', 47.6740, -122.1215, 1200000, 144000, 78),
('BLDG-MS-002', 'PORTFOLIO-001', 'Microsoft Campus Building 2', 'office', 380000, 2018, 'Redmond, WA', 47.6745, -122.1220, 980000, 117600, 85),
('BLDG-MS-003', 'PORTFOLIO-001', 'Microsoft Austin Office', 'office', 275000, 2020, 'Austin, TX', 30.2672, -97.7431, 750000, 90000, 82),
('BLDG-MS-004', 'PORTFOLIO-001', 'Microsoft NYC Office', 'office', 320000, 2016, 'New York, NY', 40.7128, -74.0060, 890000, 133500, 72),

-- Walmart buildings  
('BLDG-WM-001', 'PORTFOLIO-002', 'Walmart Supercenter #1001', 'retail', 185000, 2012, 'Bentonville, AR', 36.3729, -94.2088, 420000, 50400, 65),
('BLDG-WM-002', 'PORTFOLIO-002', 'Walmart Supercenter #1002', 'retail', 180000, 2014, 'Dallas, TX', 32.7767, -96.7970, 410000, 49200, 68),
('BLDG-WM-003', 'PORTFOLIO-002', 'Walmart Distribution Center', 'warehouse', 850000, 2010, 'Phoenix, AZ', 33.4484, -112.0740, 1800000, 216000, 58),
('BLDG-WM-004', 'PORTFOLIO-002', 'Walmart Supercenter #1004', 'retail', 175000, 2016, 'Miami, FL', 25.7617, -80.1918, 390000, 54600, 71),

-- JPMorgan buildings
('BLDG-JP-001', 'PORTFOLIO-003', 'JPMorgan Chase Tower', 'office', 1200000, 2008, 'New York, NY', 40.7555, -73.9747, 3200000, 480000, 75),
('BLDG-JP-002', 'PORTFOLIO-003', 'JPMorgan Chicago Office', 'office', 650000, 2011, 'Chicago, IL', 41.8781, -87.6298, 1750000, 262500, 73),
('BLDG-JP-003', 'PORTFOLIO-003', 'JPMorgan San Francisco Office', 'office', 420000, 2019, 'San Francisco, CA', 37.7749, -122.4194, 1100000, 198000, 81),

-- General Motors buildings
('BLDG-GM-001', 'PORTFOLIO-004', 'GM Technical Center', 'manufacturing', 2800000, 1956, 'Warren, MI', 42.4834, -83.1024, 7500000, 900000, 52),
('BLDG-GM-002', 'PORTFOLIO-004', 'GM Assembly Plant', 'manufacturing', 1200000, 1985, 'Arlington, TX', 32.7357, -97.1081, 3200000, 384000, 48),
('BLDG-GM-003', 'PORTFOLIO-004', 'GM Corporate HQ', 'office', 350000, 2009, 'Detroit, MI', 42.3314, -83.0458, 950000, 142500, 79),

-- Amazon buildings
('BLDG-AM-001', 'PORTFOLIO-005', 'Amazon Fulfillment Center SEA8', 'warehouse', 1100000, 2017, 'Seattle, WA', 47.6062, -122.3321, 2800000, 336000, 62),
('BLDG-AM-002', 'PORTFOLIO-005', 'Amazon Fulfillment Center DFW1', 'warehouse', 950000, 2019, 'Dallas, TX', 32.8998, -97.0403, 2400000, 288000, 67),
('BLDG-AM-003', 'PORTFOLIO-005', 'Amazon Office Building', 'office', 580000, 2021, 'Arlington, VA', 38.8816, -77.0910, 1450000, 217500, 86),
('BLDG-AM-004', 'PORTFOLIO-005', 'Amazon Fulfillment Center LAX2', 'warehouse', 1250000, 2015, 'Los Angeles, CA', 34.0522, -118.2437, 3100000, 465000, 59);

-- Insert sample energy meters
INSERT INTO energy_meters (meter_id, building_id, meter_type, energy_type, meter_location, manufacturer, model, installation_date, sampling_interval_minutes) VALUES
-- Microsoft meters
('METER-MS-001-MAIN', 'BLDG-MS-001', 'main', 'electricity', 'Main Electrical Room', 'Schneider Electric', 'ION8650', '2015-03-15', 15),
('METER-MS-001-HVAC', 'BLDG-MS-001', 'sub', 'electricity', 'HVAC Equipment Room', 'Schneider Electric', 'ION7650', '2015-03-15', 15),
('METER-MS-002-MAIN', 'BLDG-MS-002', 'main', 'electricity', 'Main Electrical Room', 'Schneider Electric', 'ION8650', '2018-06-10', 15),
('METER-MS-003-MAIN', 'BLDG-MS-003', 'main', 'electricity', 'Main Electrical Room', 'Schneider Electric', 'ION8650', '2020-01-20', 15),
('METER-MS-004-MAIN', 'BLDG-MS-004', 'main', 'electricity', 'Main Electrical Room', 'Schneider Electric', 'ION8650', '2016-09-12', 15),

-- Walmart meters
('METER-WM-001-MAIN', 'BLDG-WM-001', 'main', 'electricity', 'Main Electrical Room', 'Itron', 'Sentinel', '2012-05-08', 15),
('METER-WM-002-MAIN', 'BLDG-WM-002', 'main', 'electricity', 'Main Electrical Room', 'Itron', 'Sentinel', '2014-07-22', 15),
('METER-WM-003-MAIN', 'BLDG-WM-003', 'main', 'electricity', 'Main Electrical Room', 'Itron', 'Sentinel', '2010-11-15', 15),
('METER-WM-004-MAIN', 'BLDG-WM-004', 'main', 'electricity', 'Main Electrical Room', 'Itron', 'Sentinel', '2016-03-05', 15),

-- JPMorgan meters
('METER-JP-001-MAIN', 'BLDG-JP-001', 'main', 'electricity', 'Main Electrical Room', 'GE', 'Multilin EPM9650', '2008-12-01', 15),
('METER-JP-002-MAIN', 'BLDG-JP-002', 'main', 'electricity', 'Main Electrical Room', 'GE', 'Multilin EPM9650', '2011-04-18', 15),
('METER-JP-003-MAIN', 'BLDG-JP-003', 'main', 'electricity', 'Main Electrical Room', 'GE', 'Multilin EPM9650', '2019-08-30', 15),

-- General Motors meters
('METER-GM-001-MAIN', 'BLDG-GM-001', 'main', 'electricity', 'Main Electrical Room', 'ABB', 'M2M', '2010-06-12', 15),
('METER-GM-001-GAS', 'BLDG-GM-001', 'main', 'gas', 'Gas Meter Building', 'Honeywell', 'Echostream', '2010-06-12', 60),
('METER-GM-002-MAIN', 'BLDG-GM-002', 'main', 'electricity', 'Main Electrical Room', 'ABB', 'M2M', '2011-09-25', 15),
('METER-GM-003-MAIN', 'BLDG-GM-003', 'main', 'electricity', 'Main Electrical Room', 'ABB', 'M2M', '2009-11-08', 15),

-- Amazon meters
('METER-AM-001-MAIN', 'BLDG-AM-001', 'main', 'electricity', 'Main Electrical Room', 'Siemens', 'SENTRON PAC', '2017-02-28', 15),
('METER-AM-002-MAIN', 'BLDG-AM-002', 'main', 'electricity', 'Main Electrical Room', 'Siemens', 'SENTRON PAC', '2019-01-15', 15),
('METER-AM-003-MAIN', 'BLDG-AM-003', 'main', 'electricity', 'Main Electrical Room', 'Siemens', 'SENTRON PAC', '2021-03-10', 15),
('METER-AM-004-MAIN', 'BLDG-AM-004', 'main', 'electricity', 'Main Electrical Room', 'Siemens', 'SENTRON PAC', '2015-12-08', 15);

-- Insert sample energy usage data (last 30 days)
-- This creates realistic time series data for testing
INSERT INTO energy_usage (meter_id, building_id, reading_date, energy_type, energy_consumption, energy_cost, demand_kw, weather_temp_f, occupancy_percentage)
SELECT 
    m.meter_id,
    m.building_id,
    generate_series(
        CURRENT_DATE - INTERVAL '30 days',
        CURRENT_DATE - INTERVAL '1 day',
        INTERVAL '1 hour'
    ) as reading_date,
    m.energy_type,
    -- Generate realistic consumption based on building type and time
    CASE 
        WHEN b.building_type = 'office' THEN 
            b.baseline_consumption / 720.0 * (0.8 + 0.4 * random()) * 
            CASE WHEN EXTRACT(hour FROM generate_series) BETWEEN 8 AND 18 THEN 1.2 ELSE 0.6 END
        WHEN b.building_type = 'retail' THEN 
            b.baseline_consumption / 720.0 * (0.9 + 0.2 * random()) *
            CASE WHEN EXTRACT(hour FROM generate_series) BETWEEN 10 AND 22 THEN 1.1 ELSE 0.7 END
        WHEN b.building_type = 'warehouse' THEN 
            b.baseline_consumption / 720.0 * (0.85 + 0.3 * random()) *
            CASE WHEN EXTRACT(hour FROM generate_series) BETWEEN 6 AND 18 THEN 1.0 ELSE 0.8 END
        WHEN b.building_type = 'manufacturing' THEN 
            b.baseline_consumption / 720.0 * (0.9 + 0.2 * random()) *
            CASE WHEN EXTRACT(hour FROM generate_series) BETWEEN 6 AND 22 THEN 1.0 ELSE 0.9 END
        ELSE b.baseline_consumption / 720.0 * (0.8 + 0.4 * random())
    END as energy_consumption,
    -- Calculate cost (assuming $0.12/kWh average)
    (CASE 
        WHEN b.building_type = 'office' THEN 
            b.baseline_consumption / 720.0 * (0.8 + 0.4 * random()) * 
            CASE WHEN EXTRACT(hour FROM generate_series) BETWEEN 8 AND 18 THEN 1.2 ELSE 0.6 END
        WHEN b.building_type = 'retail' THEN 
            b.baseline_consumption / 720.0 * (0.9 + 0.2 * random()) *
            CASE WHEN EXTRACT(hour FROM generate_series) BETWEEN 10 AND 22 THEN 1.1 ELSE 0.7 END
        WHEN b.building_type = 'warehouse' THEN 
            b.baseline_consumption / 720.0 * (0.85 + 0.3 * random()) *
            CASE WHEN EXTRACT(hour FROM generate_series) BETWEEN 6 AND 18 THEN 1.0 ELSE 0.8 END
        WHEN b.building_type = 'manufacturing' THEN 
            b.baseline_consumption / 720.0 * (0.9 + 0.2 * random()) *
            CASE WHEN EXTRACT(hour FROM generate_series) BETWEEN 6 AND 22 THEN 1.0 ELSE 0.9 END
        ELSE b.baseline_consumption / 720.0 * (0.8 + 0.4 * random())
    END) * 0.12 as energy_cost,
    -- Generate demand data (kW)
    CASE 
        WHEN m.energy_type = 'electricity' THEN
            (b.baseline_consumption / 720.0 * (0.8 + 0.4 * random())) * 1.2
        ELSE NULL
    END as demand_kw,
    -- Generate weather data (temperature in Fahrenheit)
    65 + 20 * sin(2 * pi() * EXTRACT(doy FROM generate_series) / 365.0) + 10 * random() - 5 as weather_temp_f,
    -- Generate occupancy data
    CASE 
        WHEN b.building_type = 'office' THEN 
            CASE WHEN EXTRACT(hour FROM generate_series) BETWEEN 8 AND 18 THEN 75 + 20 * random() ELSE 5 + 10 * random() END
        WHEN b.building_type = 'retail' THEN 
            CASE WHEN EXTRACT(hour FROM generate_series) BETWEEN 10 AND 22 THEN 40 + 30 * random() ELSE 5 + 10 * random() END
        ELSE 80 + 15 * random()
    END as occupancy_percentage
FROM energy_meters m
JOIN buildings b ON m.building_id = b.building_id
WHERE m.energy_type = 'electricity'
LIMIT 50000; -- Limit to prevent excessive data generation

-- Insert sample energy projects
INSERT INTO energy_projects (building_id, project_name, project_type, technology_description, installation_cost, annual_savings_kwh, annual_savings_cost, project_roi, payback_years, carbon_reduction_tons, project_status, start_date, completion_date) VALUES
('BLDG-MS-001', 'LED Lighting Retrofit', 'LED', 'Replace 2,500 fluorescent fixtures with LED', 875000, 360000, 43200, 1.98, 2.5, 144, 'completed', '2023-03-01', '2023-05-15'),
('BLDG-MS-002', 'HVAC Optimization', 'HVAC', 'Smart HVAC controls and variable speed drives', 1200000, 294000, 35280, 1.47, 4.2, 117.6, 'completed', '2023-06-01', '2023-09-30'),
('BLDG-WM-001', 'Solar Installation', 'Solar', '500kW rooftop solar system', 1250000, 750000, 90000, 2.88, 1.8, 300, 'completed', '2023-01-15', '2023-04-20'),
('BLDG-WM-003', 'LED Warehouse Lighting', 'LED', 'High-bay LED fixtures with smart controls', 1500000, 540000, 64800, 1.73, 2.9, 216, 'in_progress', '2024-02-01', NULL),
('BLDG-JP-001', 'Building Automation Upgrade', 'HVAC', 'Advanced building management system', 2800000, 960000, 115200, 1.64, 3.1, 384, 'approved', '2024-06-01', NULL),
('BLDG-GM-001', 'Energy Recovery System', 'HVAC', 'Heat recovery ventilation system', 3200000, 1125000, 135000, 1.69, 2.96, 450, 'planned', NULL, NULL),
('BLDG-AM-001', 'Solar + Battery Storage', 'Solar', '800kW solar with 2MWh battery storage', 4500000, 1200000, 144000, 1.28, 3.9, 480, 'approved', '2024-08-01', NULL);

-- Insert sample project opportunities
INSERT INTO project_opportunities (building_id, opportunity_type, description, estimated_cost, annual_savings, estimated_roi, payback_years, carbon_reduction_tons, implementation_complexity, priority_score) VALUES
-- Microsoft opportunities
('BLDG-MS-003', 'LED', 'LED lighting retrofit for entire building', 650000, 78000, 2.4, 1.7, 156, 'low', 85),
('BLDG-MS-004', 'HVAC', 'HVAC system optimization and controls upgrade', 950000, 133500, 1.8, 2.4, 267, 'medium', 78),
('BLDG-MS-004', 'Solar', 'Rooftop solar installation - 400kW system', 1000000, 72000, 1.44, 4.6, 288, 'high', 65),

-- Walmart opportunities  
('BLDG-WM-002', 'LED', 'LED retrofit with daylight harvesting controls', 425000, 61500, 2.9, 1.4, 123, 'low', 92),
('BLDG-WM-004', 'HVAC', 'High-efficiency rooftop units replacement', 780000, 109200, 2.2, 1.8, 218.4, 'medium', 88),
('BLDG-WM-003', 'Solar', 'Large-scale solar installation - 1MW system', 2500000, 180000, 1.44, 4.6, 720, 'high', 72),

-- JPMorgan opportunities
('BLDG-JP-002', 'Building_Automation', 'Smart building controls and energy management', 1300000, 262500, 3.2, 1.3, 525, 'medium', 95),
('BLDG-JP-003', 'Window_Upgrade', 'High-performance windows and facade improvements', 2100000, 198000, 1.9, 2.1, 396, 'high', 68),

-- General Motors opportunities
('BLDG-GM-002', 'Process_Optimization', 'Manufacturing equipment efficiency improvements', 5000000, 576000, 2.3, 1.7, 1152, 'high', 85),
('BLDG-GM-003', 'Geothermal', 'Geothermal heating and cooling system', 1800000, 213750, 2.4, 1.7, 427.5, 'high', 75),

-- Amazon opportunities
('BLDG-AM-002', 'Lighting_Controls', 'Advanced lighting controls with occupancy sensors', 380000, 57600, 3.0, 1.4, 115.2, 'low', 90),
('BLDG-AM-004', 'Cool_Roof', 'Cool roof installation for temperature reduction', 625000, 93000, 2.98, 1.3, 186, 'medium', 82);

-- Insert sample benchmark data
INSERT INTO benchmark_data (building_type, region, benchmark_type, energy_use_intensity, carbon_intensity, cost_per_sqft, percentile_25, percentile_50, percentile_75, sample_size, data_year, source) VALUES
('office', 'National', 'energy_star', 92.1, 52.8, 3.21, 78.5, 92.1, 108.7, 15000, 2024, 'EPA Energy Star Portfolio Manager'),
('retail', 'National', 'energy_star', 124.5, 71.2, 4.15, 105.2, 124.5, 145.8, 8500, 2024, 'EPA Energy Star Portfolio Manager'),
('warehouse', 'National', 'energy_star', 68.3, 39.1, 2.85, 58.1, 68.3, 79.2, 4200, 2024, 'EPA Energy Star Portfolio Manager'),
('manufacturing', 'National', 'energy_star', 156.8, 89.7, 5.42, 132.4, 156.8, 185.1, 3500, 2024, 'EPA Energy Star Portfolio Manager'),
('office', 'West', 'energy_star', 89.7, 48.5, 3.45, 76.2, 89.7, 105.3, 3200, 2024, 'EPA Energy Star Portfolio Manager'),
('office', 'Northeast', 'energy_star', 95.4, 58.2, 3.85, 81.1, 95.4, 112.8, 4500, 2024, 'EPA Energy Star Portfolio Manager'),
('retail', 'South', 'energy_star', 128.9, 75.4, 3.95, 109.2, 128.9, 150.1, 2800, 2024, 'EPA Energy Star Portfolio Manager'),
('warehouse', 'Midwest', 'energy_star', 71.2, 42.3, 2.65, 60.5, 71.2, 82.8, 1500, 2024, 'EPA Energy Star Portfolio Manager');

-- Update portfolio building counts
UPDATE portfolios SET building_count = (
    SELECT COUNT(*) FROM buildings WHERE buildings.portfolio_id = portfolios.portfolio_id
);

-- Update portfolio total floor area
UPDATE portfolios SET total_floor_area = (
    SELECT SUM(floor_area) FROM buildings WHERE buildings.portfolio_id = portfolios.portfolio_id
);

-- Update energy meter last reading dates
UPDATE energy_meters SET last_reading_date = (
    SELECT MAX(reading_date) FROM energy_usage WHERE energy_usage.meter_id = energy_meters.meter_id
);

-- Add some sample sustainability reports
INSERT INTO sustainability_reports (portfolio_id, report_type, reporting_period_start, reporting_period_end, total_energy_consumption, total_energy_cost, total_carbon_emissions, scope_1_emissions, scope_2_emissions, energy_intensity, carbon_intensity, energy_star_avg_score, projects_completed, total_savings_kwh, total_savings_cost) VALUES
('PORTFOLIO-001', 'executive', '2024-01-01', '2024-03-31', 12500000, 1500000, 5000, 200, 4800, 85.2, 45.3, 79, 2, 654000, 78480),
('PORTFOLIO-002', 'detailed', '2024-01-01', '2024-03-31', 28750000, 3450000, 11500, 500, 11000, 125.8, 72.1, 65, 1, 750000, 90000),
('PORTFOLIO-003', 'investor', '2024-01-01', '2024-03-31', 18200000, 2184000, 7280, 150, 7130, 94.7, 54.8, 76, 0, 0, 0);

COMMIT;