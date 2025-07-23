-- Enhanced Redaptive Sample Data
-- Comprehensive mock data for development and testing
-- Simulates realistic Fortune 500 energy portfolios

-- Clear existing data
TRUNCATE TABLE energy_alerts CASCADE;
TRUNCATE TABLE maintenance_records CASCADE;
TRUNCATE TABLE weather_data CASCADE;
TRUNCATE TABLE utility_bills CASCADE;
TRUNCATE TABLE energy_usage CASCADE;
TRUNCATE TABLE energy_meters CASCADE;
TRUNCATE TABLE equipment CASCADE;
TRUNCATE TABLE buildings CASCADE;
TRUNCATE TABLE portfolios CASCADE;
TRUNCATE TABLE energy_projects CASCADE;
TRUNCATE TABLE project_opportunities CASCADE;
TRUNCATE TABLE sustainability_reports CASCADE;
TRUNCATE TABLE benchmark_data CASCADE;
TRUNCATE TABLE market_rates CASCADE;
TRUNCATE TABLE users CASCADE;

-- Insert Users (Platform users and contacts)
INSERT INTO users (user_id, email, first_name, last_name, role, company, phone, timezone) VALUES
(uuid_generate_v4(), 'sarah.martinez@redaptive.com', 'Sarah', 'Martinez', 'admin', 'Redaptive', '555-0101', 'America/Los_Angeles'),
(uuid_generate_v4(), 'mike.chen@redaptive.com', 'Mike', 'Chen', 'energy_manager', 'Redaptive', '555-0102', 'America/Denver'),
(uuid_generate_v4(), 'alex.rodriguez@redaptive.com', 'Alex', 'Rodriguez', 'field_engineer', 'Redaptive', '555-0103', 'America/Chicago'),
(uuid_generate_v4(), 'lisa.taylor@microsoft.com', 'Lisa', 'Taylor', 'customer', 'Microsoft', '555-0201', 'America/Los_Angeles'),
(uuid_generate_v4(), 'david.johnson@walmart.com', 'David', 'Johnson', 'customer', 'Walmart', '555-0301', 'America/Chicago'),
(uuid_generate_v4(), 'maria.garcia@jpmorgan.com', 'Maria', 'Garcia', 'customer', 'JPMorgan Chase', '555-0401', 'America/New_York'),
(uuid_generate_v4(), 'james.wilson@gm.com', 'James', 'Wilson', 'customer', 'General Motors', '555-0501', 'America/Detroit'),
(uuid_generate_v4(), 'jennifer.brown@amazon.com', 'Jennifer', 'Brown', 'customer', 'Amazon', '555-0601', 'America/Los_Angeles'),
(uuid_generate_v4(), 'robert.davis@apple.com', 'Robert', 'Davis', 'customer', 'Apple', '555-0701', 'America/Los_Angeles'),
(uuid_generate_v4(), 'karen.miller@target.com', 'Karen', 'Miller', 'customer', 'Target', '555-0801', 'America/Chicago');

-- Insert Fortune 500 Portfolios
INSERT INTO portfolios (portfolio_id, portfolio_name, company_name, industry, headquarters_location, total_floor_area, annual_revenue, employees, primary_contact_id, sustainability_goals, contract_start_date, contract_end_date, monthly_fee, status) VALUES
('MSFT_PORTFOLIO', 'Microsoft Corporate Real Estate', 'Microsoft Corporation', 'Technology', 'Redmond, WA', 45000000, 198000000000, 221000, (SELECT user_id FROM users WHERE email = 'lisa.taylor@microsoft.com'), '{"net_zero_target": "2030", "renewable_energy_target": "100% by 2025", "carbon_negative": "by 2030"}', '2023-01-01', '2028-12-31', 125000, 'active'),
('WMT_PORTFOLIO', 'Walmart Real Estate Portfolio', 'Walmart Inc.', 'Retail', 'Bentonville, AR', 850000000, 611000000000, 2300000, (SELECT user_id FROM users WHERE email = 'david.johnson@walmart.com'), '{"net_zero_emissions": "2040", "renewable_energy": "100% by 2035", "zero_waste": "by 2025"}', '2023-03-15', '2030-03-14', 285000, 'active'),
('JPM_PORTFOLIO', 'JPMorgan Chase Facilities', 'JPMorgan Chase & Co.', 'Financial Services', 'New York, NY', 75000000, 119000000000, 271000, (SELECT user_id FROM users WHERE email = 'maria.garcia@jpmorgan.com'), '{"carbon_neutral": "2030", "renewable_energy": "100% by 2030", "sustainable_finance": "$2.5T by 2030"}', '2023-06-01', '2028-05-31', 89000, 'active'),
('GM_PORTFOLIO', 'General Motors Facilities', 'General Motors Company', 'Automotive', 'Detroit, MI', 120000000, 127000000000, 167000, (SELECT user_id FROM users WHERE email = 'james.wilson@gm.com'), '{"carbon_neutral": "2040", "electric_vehicles": "100% by 2035", "renewable_energy": "100% by 2035"}', '2023-09-01', '2030-08-31', 145000, 'active'),
('AMZN_PORTFOLIO', 'Amazon Global Real Estate', 'Amazon.com Inc.', 'E-commerce/Cloud', 'Seattle, WA', 180000000, 513000000000, 1541000, (SELECT user_id FROM users WHERE email = 'jennifer.brown@amazon.com'), '{"net_zero_carbon": "2040", "renewable_energy": "100% by 2030", "climate_pledge": "10 years ahead of Paris Agreement"}', '2024-01-15', '2031-01-14', 195000, 'active'),
('AAPL_PORTFOLIO', 'Apple Campus and Facilities', 'Apple Inc.', 'Technology', 'Cupertino, CA', 25000000, 394000000000, 164000, (SELECT user_id FROM users WHERE email = 'robert.davis@apple.com'), '{"carbon_neutral": "2030", "renewable_energy": "100% achieved", "supply_chain_neutral": "2030"}', '2024-03-01', '2029-02-28', 67000, 'active'),
('TGT_PORTFOLIO', 'Target Store Portfolio', 'Target Corporation', 'Retail', 'Minneapolis, MN', 280000000, 109000000000, 450000, (SELECT user_id FROM users WHERE email = 'karen.miller@target.com'), '{"net_zero_emissions": "2040", "renewable_energy": "100% by 2030", "sustainable_products": "$2B by 2025"}', '2024-05-15', '2032-05-14', 165000, 'active');

-- Insert Buildings (Sample buildings for each portfolio)
INSERT INTO buildings (building_id, portfolio_id, building_name, building_type, floor_area, floors, year_built, year_renovated, address, city, state, zip_code, latitude, longitude, timezone, climate_zone, baseline_consumption_kwh, baseline_cost_annual, peak_demand_kw, operating_hours_per_day, occupancy_max, energy_star_score, leed_certification, utility_provider_electric, utility_provider_gas, utility_account_electric, utility_account_gas, building_automation_system) VALUES

-- Microsoft Buildings
('MSFT_MAIN_CAMPUS', 'MSFT_PORTFOLIO', 'Microsoft Main Campus Building 99', 'office', 1200000, 8, 2012, 2020, '1 Microsoft Way', 'Redmond', 'WA', '98052', 47.6398, -122.1289, 'America/Los_Angeles', '4C', 8500000, 850000, 2100, 12, 3500, 88, 'Gold', 'Puget Sound Energy', 'Puget Sound Energy', 'MSFT-MAIN-001', 'MSFT-GAS-001', 'Honeywell EBI'),
('MSFT_BUILDING_92', 'MSFT_PORTFOLIO', 'Microsoft Building 92', 'office', 650000, 6, 2015, NULL, '14820 NE 36th St', 'Redmond', 'WA', '98052', 47.6389, -122.1305, 'America/Los_Angeles', '4C', 4200000, 420000, 1050, 12, 1800, 92, 'Platinum', 'Puget Sound Energy', 'Puget Sound Energy', 'MSFT-B92-001', 'MSFT-GAS-002', 'Johnson Controls Metasys'),
('MSFT_DATACENTER_QN1', 'MSFT_PORTFOLIO', 'Microsoft Quincy Data Center', 'data_center', 300000, 2, 2019, NULL, '1031 Columbia River Rd', 'Quincy', 'WA', '98848', 47.2345, -119.8525, 'America/Los_Angeles', '5B', 24000000, 1800000, 8500, 24, 150, 85, 'None', 'Grant County PUD', 'Cascade Natural Gas', 'MSFT-QN1-001', 'MSFT-QN1-GAS', 'Schneider Electric EcoStruxure'),

-- Walmart Buildings  
('WMT_SUPER_001', 'WMT_PORTFOLIO', 'Walmart Supercenter #1234', 'retail', 180000, 1, 2008, 2018, '2500 W Main St', 'Bentonville', 'AR', '72712', 36.3729, -94.2088, 'America/Chicago', '3A', 2800000, 280000, 890, 18, 500, 78, 'None', 'Entergy Arkansas', 'CenterPoint Energy', 'WMT-1234-001', 'WMT-1234-GAS', 'Honeywell'),
('WMT_SUPER_002', 'WMT_PORTFOLIO', 'Walmart Supercenter #5678', 'retail', 185000, 1, 2012, NULL, '1200 E Walnut St', 'Rogers', 'AR', '72756', 36.3320, -94.1188, 'America/Chicago', '3A', 2950000, 295000, 920, 18, 520, 82, 'None', 'Entergy Arkansas', 'CenterPoint Energy', 'WMT-5678-001', 'WMT-5678-GAS', 'Johnson Controls'),
('WMT_DC_DALLAS', 'WMT_PORTFOLIO', 'Walmart Distribution Center Dallas', 'warehouse', 1200000, 2, 2010, 2020, '7100 John W Carpenter Fwy', 'Dallas', 'TX', '75247', 32.8370, -96.8295, 'America/Chicago', '3A', 8500000, 765000, 2200, 24, 800, 85, 'Silver', 'Oncor Electric', 'Atmos Energy', 'WMT-DC-DAL-001', 'WMT-DC-DAL-GAS', 'Siemens Desigo'),

-- JPMorgan Buildings
('JPM_TOWER_NYC', 'JPM_PORTFOLIO', 'JPMorgan Chase Tower NYC', 'office', 2500000, 52, 1961, 2016, '270 Park Ave', 'New York', 'NY', '10017', 40.7505, -73.9794, 'America/New_York', '4A', 18500000, 2220000, 4200, 14, 12000, 90, 'Platinum', 'Con Edison', 'Con Edison', 'JPM-NYC-001', 'JPM-NYC-GAS', 'Honeywell EBI'),
('JPM_BROOKLYN', 'JPM_PORTFOLIO', 'JPMorgan Chase Brooklyn Office', 'office', 850000, 12, 2005, 2019, '4 Metrotech Center', 'Brooklyn', 'NY', '11201', 40.6932, -73.9832, 'America/New_York', '4A', 6200000, 744000, 1580, 12, 3500, 87, 'Gold', 'Con Edison', 'National Grid', 'JPM-BRK-001', 'JPM-BRK-GAS', 'Johnson Controls Metasys'),

-- General Motors Buildings
('GM_WARREN_TECH', 'GM_PORTFOLIO', 'GM Warren Technical Center', 'manufacturing', 3200000, 4, 1956, 2015, '30001 Van Dyke Ave', 'Warren', 'MI', '48090', 42.5156, -83.0935, 'America/Detroit', '5A', 35000000, 2800000, 12500, 24, 8000, 82, 'Silver', 'DTE Energy', 'DTE Energy', 'GM-WTC-001', 'GM-WTC-GAS', 'Rockwell Automation'),
('GM_DETROIT_HAM', 'GM_PORTFOLIO', 'GM Detroit-Hamtramck Assembly', 'manufacturing', 4500000, 2, 1985, 2019, '2500 E Grand Blvd', 'Detroit', 'MI', '48211', 42.3682, -83.0567, 'America/Detroit', '5A', 42000000, 3360000, 18000, 24, 3000, 78, 'None', 'DTE Energy', 'DTE Energy', 'GM-DHA-001', 'GM-DHA-GAS', 'Schneider Electric'),

-- Amazon Buildings
('AMZN_HQ2_VAR1', 'AMZN_PORTFOLIO', 'Amazon HQ2 Met Park Campus', 'office', 2100000, 22, 2023, NULL, '1800 S Bell St', 'Arlington', 'VA', '22202', 38.8462, -77.0509, 'America/New_York', '4A', 12000000, 1440000, 3200, 12, 8500, 95, 'Platinum', 'Dominion Energy', 'Washington Gas', 'AMZN-HQ2-001', 'AMZN-HQ2-GAS', 'Honeywell EBI'),
('AMZN_FULFILLMENT_TX', 'AMZN_PORTFOLIO', 'Amazon Fulfillment Center DFW8', 'warehouse', 1000000, 1, 2020, NULL, '2700 Regent Blvd', 'Irving', 'TX', '75063', 32.8140, -96.9489, 'America/Chicago', '3A', 7200000, 648000, 2800, 24, 2500, 83, 'None', 'Oncor Electric', 'Atmos Energy', 'AMZN-DFW8-001', 'AMZN-DFW8-GAS', 'Johnson Controls'),

-- Apple Buildings  
('AAPL_PARK_MAIN', 'AAPL_PORTFOLIO', 'Apple Park Main Building', 'office', 2800000, 4, 2017, NULL, '1 Apple Park Way', 'Cupertino', 'CA', '95014', 37.3349, -122.0090, 'America/Los_Angeles', '3C', 8500000, 1020000, 2100, 12, 12000, 98, 'Platinum', 'PG&E', 'PG&E', 'AAPL-PARK-001', 'AAPL-PARK-GAS', 'Custom Apple BMS'),
('AAPL_INFINITE_LOOP', 'AAPL_PORTFOLIO', 'Apple Infinite Loop Campus', 'office', 850000, 6, 1993, 2013, '1 Infinite Loop', 'Cupertino', 'CA', '95014', 37.3318, -122.0312, 'America/Los_Angeles', '3C', 4200000, 504000, 1050, 12, 2800, 89, 'Gold', 'PG&E', 'PG&E', 'AAPL-IL-001', 'AAPL-IL-GAS', 'Schneider Electric'),

-- Target Buildings
('TGT_HQ_MPLS', 'TGT_PORTFOLIO', 'Target Headquarters Minneapolis', 'office', 1800000, 12, 2001, 2018, '1000 Nicollet Mall', 'Minneapolis', 'MN', '55403', 44.9692, -93.2745, 'America/Chicago', '6A', 12500000, 1125000, 3200, 12, 8500, 91, 'Gold', 'Xcel Energy', 'CenterPoint Energy', 'TGT-HQ-001', 'TGT-HQ-GAS', 'Johnson Controls Metasys'),
('TGT_STORE_001', 'TGT_PORTFOLIO', 'Target Store T-1001 Eden Prairie', 'retail', 125000, 1, 2015, NULL, '8300 Highway 7', 'Eden Prairie', 'MN', '55344', 44.8547, -93.4678, 'America/Chicago', '6A', 1850000, 166500, 580, 16, 300, 84, 'None', 'Xcel Energy', 'CenterPoint Energy', 'TGT-1001-001', 'TGT-1001-GAS', 'Honeywell');

-- Insert Equipment (Major energy-consuming equipment)
INSERT INTO equipment (equipment_id, building_id, equipment_name, equipment_type, manufacturer, model, capacity_rating, efficiency_rating, installation_date, location_description, energy_type, rated_power_kw, operating_schedule, maintenance_interval_months, status) VALUES

-- Microsoft Equipment
(uuid_generate_v4(), 'MSFT_MAIN_CAMPUS', 'Chiller Plant #1', 'HVAC', 'Carrier', '19XRV', '2000 tons', '0.45 kW/ton', '2012-06-15', 'Central Plant Room B1', 'electricity', 900, '24/7 cooling season', 6, 'operational'),
(uuid_generate_v4(), 'MSFT_MAIN_CAMPUS', 'AHU North Wing', 'HVAC', 'Trane', 'Series R', '75,000 CFM', '85% efficiency', '2012-06-15', 'North Mechanical Room 3F', 'electricity', 125, 'Mon-Fri 6AM-8PM', 12, 'operational'),
(uuid_generate_v4(), 'MSFT_MAIN_CAMPUS', 'LED Lighting Zone A', 'lighting', 'Philips', 'LED Linear', '500 fixtures', '120 lm/W', '2020-03-10', 'Floors 1-4 Open Office', 'electricity', 45, 'Mon-Fri 6AM-8PM', 24, 'operational'),
(uuid_generate_v4(), 'MSFT_DATACENTER_QN1', 'UPS System A', 'power', 'Schneider Electric', 'Galaxy 7000', '2 MVA', '96% efficiency', '2019-08-20', 'UPS Room A', 'electricity', 2000, '24/7', 6, 'operational'),
(uuid_generate_v4(), 'MSFT_DATACENTER_QN1', 'Cooling Plant Primary', 'HVAC', 'Vertiv', 'Liebert XDO', '5000 tons', '0.38 kW/ton', '2019-08-20', 'Central Cooling Plant', 'electricity', 1900, '24/7', 3, 'operational'),

-- Walmart Equipment
(uuid_generate_v4(), 'WMT_SUPER_001', 'HVAC Unit #1', 'HVAC', 'Carrier', 'WeatherExpert 50TCQ', '25 tons', '13 SEER', '2008-11-20', 'Roof Unit 1', 'electricity', 22, 'Store hours + 2hrs', 12, 'operational'),
(uuid_generate_v4(), 'WMT_SUPER_001', 'Refrigeration Rack #1', 'refrigeration', 'Hussmann', 'SMART Rack', '150 HP', 'R-448A', '2018-05-15', 'Back Room Mechanical', 'electricity', 112, '24/7', 6, 'operational'),
(uuid_generate_v4(), 'WMT_SUPER_001', 'LED Retrofit Package', 'lighting', 'Cree', 'CR Series', '800 fixtures', '150 lm/W', '2018-05-15', 'Sales Floor', 'electricity', 85, 'Store hours', 36, 'operational'),
(uuid_generate_v4(), 'WMT_DC_DALLAS', 'Material Handling System', 'motors', 'Honeywell', 'Intelligrated', '500 HP total', 'IE3 Premium', '2010-03-10', 'Warehouse Floor', 'electricity', 373, '24/7', 12, 'operational'),

-- JPMorgan Equipment  
(uuid_generate_v4(), 'JPM_TOWER_NYC', 'Central Chiller Plant', 'HVAC', 'York', 'YMC2', '3500 tons', '0.50 kW/ton', '2016-09-15', 'Mechanical Level B3', 'electricity', 1750, '24/7 Apr-Oct', 6, 'operational'),
(uuid_generate_v4(), 'JPM_TOWER_NYC', 'Emergency Generator #1', 'power', 'Caterpillar', 'C175-20', '4.5 MW', 'Tier 4', '2016-09-15', 'Generator Room B2', 'gas', 4500, 'Emergency/Testing only', 12, 'operational'),
(uuid_generate_v4(), 'JPM_TOWER_NYC', 'High-Speed Elevators', 'motors', 'Otis', 'Gen2 Premier', '32 elevators', 'ReGen Drive', '2016-09-15', 'Elevator Shafts', 'electricity', 480, '24/7', 6, 'operational'),

-- GM Equipment
(uuid_generate_v4(), 'GM_WARREN_TECH', 'Paint Booth Ventilation', 'HVAC', 'Eisenmann', 'EcoInCure', '500,000 CFM', 'Heat Recovery 85%', '2015-07-20', 'Paint Shop Building C', 'electricity', 850, '24/7 production', 3, 'operational'),
(uuid_generate_v4(), 'GM_WARREN_TECH', 'Robotic Welding Line', 'manufacturing', 'Fanuc', 'R-2000iC', '120 robots', 'Servo motors', '2015-07-20', 'Body Shop Line 2', 'electricity', 2400, '24/7 production', 6, 'operational'),
(uuid_generate_v4(), 'GM_DETROIT_HAM', 'Stamping Press Line', 'manufacturing', 'Schuler', 'MSP 600', '600 ton press', 'Variable speed drive', '2019-01-15', 'Stamping Building A', 'electricity', 3200, '24/7 production', 4, 'operational'),

-- Amazon Equipment
(uuid_generate_v4(), 'AMZN_HQ2_VAR1', 'District Cooling Plant', 'HVAC', 'Johnson Controls', 'YORK YMC2', '4000 tons', '0.42 kW/ton', '2023-03-15', 'Central Plant Level B1', 'electricity', 1680, '24/7 Mar-Nov', 6, 'operational'),
(uuid_generate_v4(), 'AMZN_FULFILLMENT_TX', 'Automated Sortation', 'motors', 'Dematic', 'ConveryMax', '2.5 mile conveyor', 'VFD controlled', '2020-11-10', 'Warehouse Floor 1', 'electricity', 1200, '24/7', 12, 'operational'),

-- Apple Equipment
(uuid_generate_v4(), 'AAPL_PARK_MAIN', 'Natural Ventilation System', 'HVAC', 'Custom Design', 'Breathing Building', 'Variable airflow', 'Natural cooling 75%', '2017-04-15', 'Integrated facade', 'electricity', 150, 'Dynamic based on weather', 12, 'operational'),
(uuid_generate_v4(), 'AAPL_PARK_MAIN', 'Solar Panel Array', 'renewable', 'SunPower', 'E-Series', '17 MW DC', '22.2% efficiency', '2017-04-15', 'Rooftop installation', 'electricity', -17000, 'Daylight hours', 24, 'operational'),

-- Target Equipment
(uuid_generate_v4(), 'TGT_HQ_MPLS', 'Central Heating Plant', 'HVAC', 'Cleaver-Brooks', 'ClearFire CFH', '15 MMBtu/hr', '85% efficiency', '2018-08-20', 'Mechanical Room B1', 'gas', 0, 'Oct-Apr heating season', 12, 'operational'),
(uuid_generate_v4(), 'TGT_STORE_001', 'Geothermal Heat Pump', 'HVAC', 'WaterFurnace', 'Envision2', '30 ton', '25 EER', '2015-09-10', 'Mechanical Room', 'electricity', 24, 'Year-round', 12, 'operational');

-- Insert Energy Meters (12k+ meters simulation - showing representative sample)
INSERT INTO energy_meters (meter_id, building_id, equipment_id, meter_name, meter_type, energy_type, meter_location, manufacturer, model, communication_protocol, installation_date, sampling_interval_minutes, units, status) VALUES

-- Microsoft Meters
('MSFT_MAIN_001', 'MSFT_MAIN_CAMPUS', NULL, 'Building Main Electric Meter', 'main', 'electricity', 'Main Electrical Room', 'Schneider Electric', 'ION9000', 'Ethernet', '2012-06-01', 15, 'kWh', 'active'),
('MSFT_MAIN_002', 'MSFT_MAIN_CAMPUS', NULL, 'North Wing Sub-Meter', 'sub', 'electricity', 'North Wing Panel', 'Schneider Electric', 'ION7650', 'Modbus TCP', '2012-06-01', 15, 'kWh', 'active'),
('MSFT_MAIN_003', 'MSFT_MAIN_CAMPUS', (SELECT equipment_id FROM equipment WHERE equipment_name = 'Chiller Plant #1' AND building_id = 'MSFT_MAIN_CAMPUS'), 'Chiller Plant Meter', 'equipment', 'electricity', 'Chiller MCC', 'Schneider Electric', 'PowerLogic PM5560', 'Modbus RTU', '2012-06-01', 15, 'kWh', 'active'),
('MSFT_QN1_001', 'MSFT_DATACENTER_QN1', NULL, 'Data Center Main Meter', 'main', 'electricity', 'Main Switchgear', 'Schneider Electric', 'ION9000', 'Ethernet', '2019-08-01', 15, 'kWh', 'active'),
('MSFT_QN1_002', 'MSFT_DATACENTER_QN1', (SELECT equipment_id FROM equipment WHERE equipment_name = 'UPS System A' AND building_id = 'MSFT_DATACENTER_QN1'), 'UPS System Meter', 'equipment', 'electricity', 'UPS Room A', 'Schneider Electric', 'PowerLogic PM8000', 'Ethernet', '2019-08-01', 5, 'kWh', 'active'),

-- Walmart Meters
('WMT_1234_001', 'WMT_SUPER_001', NULL, 'Store Main Electric', 'main', 'electricity', 'Main Panel Room', 'GE', 'kV2c-5A', 'BACnet IP', '2008-11-15', 15, 'kWh', 'active'),
('WMT_1234_002', 'WMT_SUPER_001', (SELECT equipment_id FROM equipment WHERE equipment_name = 'Refrigeration Rack #1' AND building_id = 'WMT_SUPER_001'), 'Refrigeration Meter', 'equipment', 'electricity', 'Refrigeration Room', 'Schneider Electric', 'PowerLogic PM3200', 'Modbus RTU', '2018-05-15', 15, 'kWh', 'active'),
('WMT_1234_003', 'WMT_SUPER_001', NULL, 'Natural Gas Meter', 'main', 'gas', 'Gas Meter Enclosure', 'Elster', 'EC-350', 'Pulse output', '2008-11-15', 60, 'therms', 'active'),
('WMT_DAL_001', 'WMT_DC_DALLAS', NULL, 'DC Main Electric', 'main', 'electricity', 'Main Electrical Room', 'Schneider Electric', 'ION8650', 'Ethernet', '2010-03-01', 15, 'kWh', 'active'),

-- JPMorgan Meters
('JPM_NYC_001', 'JPM_TOWER_NYC', NULL, 'Tower Main Meter 1', 'main', 'electricity', 'Main Electrical Vault', 'GE', 'kV2c-5A', 'DNP3', '2016-09-01', 15, 'kWh', 'active'),
('JPM_NYC_002', 'JPM_TOWER_NYC', NULL, 'Tower Main Meter 2', 'main', 'electricity', 'Main Electrical Vault', 'GE', 'kV2c-5A', 'DNP3', '2016-09-01', 15, 'kWh', 'active'),
('JPM_NYC_003', 'JPM_TOWER_NYC', (SELECT equipment_id FROM equipment WHERE equipment_name = 'Central Chiller Plant' AND building_id = 'JPM_TOWER_NYC'), 'Chiller Plant Meter', 'equipment', 'electricity', 'Mechanical B3', 'Schneider Electric', 'ION7650', 'Modbus TCP', '2016-09-01', 15, 'kWh', 'active'),
('JPM_BRK_001', 'JPM_BROOKLYN', NULL, 'Brooklyn Main Electric', 'main', 'electricity', 'Main Electrical Room', 'Schneider Electric', 'ION8650', 'Ethernet', '2019-03-15', 15, 'kWh', 'active'),

-- GM Meters
('GM_WTC_001', 'GM_WARREN_TECH', NULL, 'Warren Tech Main 1', 'main', 'electricity', 'Substation A', 'Schneider Electric', 'ION9000', 'Ethernet', '2015-07-01', 15, 'kWh', 'active'),
('GM_WTC_002', 'GM_WARREN_TECH', NULL, 'Warren Tech Main 2', 'main', 'electricity', 'Substation B', 'Schneider Electric', 'ION9000', 'Ethernet', '2015-07-01', 15, 'kWh', 'active'),
('GM_WTC_003', 'GM_WARREN_TECH', (SELECT equipment_id FROM equipment WHERE equipment_name = 'Paint Booth Ventilation' AND building_id = 'GM_WARREN_TECH'), 'Paint Shop Meter', 'equipment', 'electricity', 'Paint Shop MCC', 'Schneider Electric', 'PowerLogic PM5560', 'Modbus RTU', '2015-07-01', 15, 'kWh', 'active'),
('GM_DHA_001', 'GM_DETROIT_HAM', NULL, 'Detroit Assembly Main', 'main', 'electricity', 'Main Substation', 'GE', 'Multilin 850', 'DNP3', '2019-01-01', 15, 'kWh', 'active'),

-- Amazon Meters  
('AMZN_HQ2_001', 'AMZN_HQ2_VAR1', NULL, 'HQ2 Main Electric', 'main', 'electricity', 'Main Electrical Room', 'Schneider Electric', 'ION9000', 'Ethernet', '2023-03-01', 15, 'kWh', 'active'),
('AMZN_HQ2_002', 'AMZN_HQ2_VAR1', (SELECT equipment_id FROM equipment WHERE equipment_name = 'District Cooling Plant' AND building_id = 'AMZN_HQ2_VAR1'), 'Cooling Plant Meter', 'equipment', 'electricity', 'Central Plant', 'Schneider Electric', 'PowerLogic PM8000', 'Ethernet', '2023-03-01', 15, 'kWh', 'active'),
('AMZN_DFW8_001', 'AMZN_FULFILLMENT_TX', NULL, 'Fulfillment Main Electric', 'main', 'electricity', 'Main Panel Room', 'Schneider Electric', 'ION8650', 'Ethernet', '2020-11-01', 15, 'kWh', 'active'),

-- Apple Meters
('AAPL_PARK_001', 'AAPL_PARK_MAIN', NULL, 'Apple Park Main Meter', 'main', 'electricity', 'Central Electrical Room', 'Schneider Electric', 'ION9000', 'Ethernet', '2017-04-01', 15, 'kWh', 'active'),
('AAPL_PARK_002', 'AAPL_PARK_MAIN', (SELECT equipment_id FROM equipment WHERE equipment_name = 'Solar Panel Array' AND building_id = 'AAPL_PARK_MAIN'), 'Solar Generation Meter', 'equipment', 'electricity', 'Solar Inverter Room', 'SMA', 'Sunny Central 2500', 'Modbus TCP', '2017-04-01', 15, 'kWh', 'active'),
('AAPL_IL_001', 'AAPL_INFINITE_LOOP', NULL, 'Infinite Loop Main', 'main', 'electricity', 'Main Electrical Room', 'GE', 'kV2c-5A', 'Modbus RTU', '2013-06-01', 15, 'kWh', 'active'),

-- Target Meters
('TGT_HQ_001', 'TGT_HQ_MPLS', NULL, 'HQ Main Electric 1', 'main', 'electricity', 'Main Electrical Room A', 'Schneider Electric', 'ION8650', 'Ethernet', '2018-08-01', 15, 'kWh', 'active'),
('TGT_HQ_002', 'TGT_HQ_MPLS', NULL, 'HQ Main Electric 2', 'main', 'electricity', 'Main Electrical Room B', 'Schneider Electric', 'ION8650', 'Ethernet', '2018-08-01', 15, 'kWh', 'active'),
('TGT_HQ_003', 'TGT_HQ_MPLS', NULL, 'HQ Natural Gas Meter', 'main', 'gas', 'Gas Meter Room', 'Elster', 'EC-350', 'Pulse output', '2018-08-01', 60, 'therms', 'active'),
('TGT_1001_001', 'TGT_STORE_001', NULL, 'Store Electric Main', 'main', 'electricity', 'Store Electrical Room', 'GE', 'kV2c-5A', 'BACnet IP', '2015-09-01', 15, 'kWh', 'active');

-- Insert Sample Energy Usage Data (Last 3 months)
-- This generates realistic energy consumption patterns
DO $$
DECLARE
    building_record RECORD;
    meter_record RECORD;
    start_date DATE := CURRENT_DATE - INTERVAL '90 days';
    end_date DATE := CURRENT_DATE;
    current_date DATE;
    hour_counter INTEGER;
    base_consumption DECIMAL;
    hourly_consumption DECIMAL;
    daily_variation DECIMAL;
    seasonal_factor DECIMAL;
    weekend_factor DECIMAL;
    occupancy_factor DECIMAL;
    weather_factor DECIMAL;
    temp_f DECIMAL;
    is_weekend BOOLEAN;
    is_holiday BOOLEAN;
    time_of_day INTEGER;
BEGIN
    -- Loop through each meter
    FOR meter_record IN 
        SELECT em.meter_id, em.building_id, em.energy_type, em.sampling_interval_minutes,
               b.building_type, b.baseline_consumption_kwh, b.operating_hours_per_day
        FROM energy_meters em
        JOIN buildings b ON em.building_id = b.building_id
        WHERE em.status = 'active'
    LOOP
        -- Calculate base consumption per interval
        IF meter_record.energy_type = 'electricity' THEN
            base_consumption := (meter_record.baseline_consumption_kwh / 365.0 / 24.0) * (meter_record.sampling_interval_minutes / 60.0);
        ELSIF meter_record.energy_type = 'gas' THEN
            base_consumption := (meter_record.baseline_consumption_kwh * 0.1 / 365.0 / 24.0) * (meter_record.sampling_interval_minutes / 60.0); -- Convert to therms
        END IF;
        
        current_date := start_date;
        WHILE current_date <= end_date LOOP
            hour_counter := 0;
            WHILE hour_counter < 24 LOOP
                -- Skip some intervals to simulate realistic data collection
                IF EXTRACT(dow FROM current_date) != 0 OR random() > 0.02 THEN -- Skip 2% randomly, except Sundays
                    
                    -- Calculate factors for realistic consumption patterns
                    is_weekend := EXTRACT(dow FROM current_date) IN (0, 6);
                    is_holiday := current_date IN ('2024-07-04', '2024-11-28', '2024-12-25', '2024-01-01'); -- Sample holidays
                    time_of_day := hour_counter;
                    
                    -- Seasonal factor (summer peak for cooling, winter for heating)
                    seasonal_factor := 1.0 + 0.3 * sin(2 * pi() * EXTRACT(doy FROM current_date) / 365.0);
                    
                    -- Weekend factor
                    weekend_factor := CASE 
                        WHEN is_weekend AND meter_record.building_type IN ('office') THEN 0.3
                        WHEN is_weekend AND meter_record.building_type IN ('retail') THEN 0.8
                        WHEN is_weekend AND meter_record.building_type IN ('manufacturing', 'data_center', 'warehouse') THEN 0.9
                        ELSE 1.0
                    END;
                    
                    -- Time of day factor (business hours vs off-hours)
                    occupancy_factor := CASE
                        WHEN meter_record.building_type = 'office' AND time_of_day BETWEEN 8 AND 18 THEN 1.2
                        WHEN meter_record.building_type = 'retail' AND time_of_day BETWEEN 9 AND 21 THEN 1.1
                        WHEN meter_record.building_type IN ('manufacturing', 'data_center') THEN 1.0 -- 24/7 operation
                        WHEN time_of_day BETWEEN 22 AND 6 THEN 0.6 -- Night time reduced load
                        ELSE 0.8
                    END;
                    
                    -- Weather factor (temperature-dependent load)
                    temp_f := 65 + 25 * sin(2 * pi() * (EXTRACT(doy FROM current_date) - 100) / 365.0) + (random() - 0.5) * 20;
                    weather_factor := 1.0 + 0.004 * abs(temp_f - 70); -- Increased load when temp deviates from 70F
                    
                    -- Daily variation (random factor)
                    daily_variation := 0.8 + random() * 0.4; -- +/- 20% variation
                    
                    -- Calculate final consumption
                    hourly_consumption := base_consumption * seasonal_factor * weekend_factor * occupancy_factor * weather_factor * daily_variation;
                    
                    -- Add some anomalies (5% chance of anomaly)
                    IF random() < 0.05 THEN
                        hourly_consumption := hourly_consumption * (0.5 + random() * 2.0); -- 50% to 250% of normal
                    END IF;
                    
                    -- Insert energy usage record
                    INSERT INTO energy_usage (
                        meter_id, building_id, reading_date, energy_type, energy_consumption,
                        energy_cost, demand_kw, weather_temp_f, occupancy_percentage,
                        is_holiday, is_weekend, data_quality, anomaly_score
                    ) VALUES (
                        meter_record.meter_id,
                        meter_record.building_id,
                        current_date + (hour_counter * INTERVAL '1 hour'),
                        meter_record.energy_type,
                        hourly_consumption,
                        hourly_consumption * (0.08 + random() * 0.04), -- $0.08-0.12 per kWh
                        CASE WHEN meter_record.energy_type = 'electricity' THEN hourly_consumption * (0.7 + random() * 0.6) ELSE NULL END,
                        temp_f,
                        CASE WHEN is_weekend THEN 20 + random() * 30 ELSE 60 + random() * 40 END,
                        is_holiday,
                        is_weekend,
                        CASE WHEN random() < 0.9 THEN 'good' WHEN random() < 0.95 THEN 'estimated' ELSE 'questionable' END,
                        CASE WHEN random() < 0.05 THEN random() ELSE 0 END
                    );
                END IF;
                
                hour_counter := hour_counter + 1;
            END LOOP;
            current_date := current_date + INTERVAL '1 day';
        END LOOP;
    END LOOP;
END $$;