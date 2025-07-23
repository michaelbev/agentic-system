-- Enhanced Redaptive Sample Data - Part 2
-- Additional sample data for comprehensive testing

-- Insert Market Rates (Energy pricing data)
INSERT INTO market_rates (region, utility_company, rate_type, rate_schedule, customer_class, time_of_use_period, effective_date, energy_rate, demand_rate, data_source) VALUES
-- California (CAISO)
('CAISO', 'PG&E', 'electricity', 'E-19', 'commercial', 'peak', '2024-01-01', 0.25842, 18.26, 'PG&E Tariff'),
('CAISO', 'PG&E', 'electricity', 'E-19', 'commercial', 'off_peak', '2024-01-01', 0.18945, 18.26, 'PG&E Tariff'),
('CAISO', 'PG&E', 'electricity', 'E-20', 'industrial', 'peak', '2024-01-01', 0.23156, 16.82, 'PG&E Tariff'),
('CAISO', 'PG&E', 'electricity', 'E-20', 'industrial', 'off_peak', '2024-01-01', 0.16789, 16.82, 'PG&E Tariff'),

-- Texas (ERCOT)
('ERCOT', 'Oncor Electric', 'electricity', 'Large General Service', 'commercial', 'peak', '2024-01-01', 0.12875, 8.95, 'Oncor Tariff'),
('ERCOT', 'Oncor Electric', 'electricity', 'Large General Service', 'commercial', 'off_peak', '2024-01-01', 0.09234, 8.95, 'Oncor Tariff'),

-- New York (NYISO)
('NYISO', 'Con Edison', 'electricity', 'General Large', 'commercial', 'peak', '2024-01-01', 0.18945, 25.68, 'Con Ed Tariff'),
('NYISO', 'Con Edison', 'electricity', 'General Large', 'commercial', 'off_peak', '2024-01-01', 0.13254, 25.68, 'Con Ed Tariff'),

-- Washington State  
('WECC', 'Puget Sound Energy', 'electricity', 'Schedule 40', 'commercial', 'peak', '2024-01-01', 0.09875, 12.45, 'PSE Tariff'),
('WECC', 'Puget Sound Energy', 'electricity', 'Schedule 40', 'commercial', 'off_peak', '2024-01-01', 0.08234, 12.45, 'PSE Tariff'),

-- Natural Gas Rates
('US_AVERAGE', 'Various', 'natural_gas', 'Commercial', 'commercial', NULL, '2024-01-01', 1.25, NULL, 'EIA'),
('CALIFORNIA', 'PG&E', 'natural_gas', 'G-NR1', 'commercial', NULL, '2024-01-01', 1.85, NULL, 'PG&E'),
('TEXAS', 'Atmos Energy', 'natural_gas', 'Commercial', 'commercial', NULL, '2024-01-01', 1.05, NULL, 'Atmos');

-- Insert Benchmark Data (Industry performance standards)
INSERT INTO benchmark_data (building_type, climate_zone, region, benchmark_type, energy_use_intensity, energy_cost_intensity, carbon_intensity, percentile_25, percentile_50, percentile_75, sample_size, data_year, source) VALUES
-- Office Buildings
('office', '4C', 'Pacific Northwest', 'energy_star', 45.2, 4.85, 12.5, 38.5, 45.2, 52.8, 1250, 2023, 'ENERGY STAR Portfolio Manager'),
('office', '3A', 'South Central', 'energy_star', 52.8, 5.25, 18.2, 44.2, 52.8, 62.5, 2100, 2023, 'ENERGY STAR Portfolio Manager'),
('office', '4A', 'Northeast', 'energy_star', 48.6, 6.85, 15.8, 41.2, 48.6, 58.4, 3500, 2023, 'ENERGY STAR Portfolio Manager'),
('office', '3C', 'California', 'energy_star', 42.8, 8.25, 11.2, 36.5, 42.8, 49.6, 1800, 2023, 'ENERGY STAR Portfolio Manager'),
('office', '6A', 'Upper Midwest', 'energy_star', 55.2, 5.45, 22.5, 46.8, 55.2, 65.8, 890, 2023, 'ENERGY STAR Portfolio Manager'),
('office', '5A', 'Great Lakes', 'energy_star', 58.5, 5.85, 24.2, 49.2, 58.5, 68.9, 1200, 2023, 'ENERGY STAR Portfolio Manager'),

-- Retail Buildings
('retail', '3A', 'South Central', 'energy_star', 68.5, 6.25, 22.8, 58.2, 68.5, 78.6, 1450, 2023, 'ENERGY STAR Portfolio Manager'),
('retail', '6A', 'Upper Midwest', 'energy_star', 72.8, 6.85, 29.5, 62.4, 72.8, 84.2, 650, 2023, 'ENERGY STAR Portfolio Manager'),

-- Warehouse/Distribution
('warehouse', '3A', 'South Central', 'energy_star', 28.5, 2.85, 9.8, 22.4, 28.5, 35.6, 980, 2023, 'ENERGY STAR Portfolio Manager'),
('warehouse', '5A', 'Great Lakes', 'energy_star', 32.8, 3.25, 13.2, 26.8, 32.8, 39.5, 560, 2023, 'ENERGY STAR Portfolio Manager'),

-- Manufacturing
('manufacturing', '5A', 'Great Lakes', 'cbecs', 125.8, 8.45, 48.5, 98.5, 125.8, 158.6, 450, 2023, 'EIA CBECS'),
('manufacturing', '3A', 'South Central', 'cbecs', 118.5, 7.85, 42.8, 95.2, 118.5, 145.8, 380, 2023, 'EIA CBECS'),

-- Data Centers
('data_center', '4C', 'Pacific Northwest', 'ashrae', 450.8, 28.5, 118.5, 385.2, 450.8, 528.6, 125, 2023, 'ASHRAE TC 9.9'),
('data_center', '3A', 'South Central', 'ashrae', 485.6, 32.8, 165.8, 412.8, 485.6, 568.9, 98, 2023, 'ASHRAE TC 9.9');

-- Insert Energy Projects (Completed and planned EaaS projects)
INSERT INTO energy_projects (building_id, project_name, project_type, technology_description, vendor_name, installation_cost, annual_savings_kwh, annual_savings_cost, project_roi, payback_years, carbon_reduction_tons_annual, project_status, planned_start_date, actual_start_date, planned_completion_date, actual_completion_date, warranty_years) VALUES

-- Microsoft Projects (Completed)
('MSFT_MAIN_CAMPUS', 'LED Lighting Retrofit Phase 1', 'LED_retrofit', 'Replace 500 T8 fluorescent fixtures with LED linear fixtures, add occupancy sensors', 'Philips Lighting', 285000, 450000, 45000, 0.158, 6.3, 124.5, 'completed', '2020-01-15', '2020-02-01', '2020-04-30', '2020-03-28', 10),
('MSFT_BUILDING_92', 'HVAC Controls Upgrade', 'HVAC_upgrade', 'Install advanced BAS controls with AI optimization algorithms', 'Johnson Controls', 425000, 680000, 68000, 0.160, 6.3, 188.4, 'completed', '2021-05-01', '2021-05-15', '2021-08-31', '2021-07-22', 5),
('MSFT_DATACENTER_QN1', 'Free Cooling Economizer', 'HVAC_upgrade', 'Install air-side economizer system for 8 months/year free cooling', 'Schneider Electric', 850000, 2800000, 210000, 0.247, 4.0, 775.2, 'completed', '2022-03-01', '2022-03-15', '2022-09-30', '2022-08-15', 7),

-- Walmart Projects
('WMT_SUPER_001', 'Refrigeration System Upgrade', 'refrigeration_upgrade', 'Replace R-22 system with CO2 transcritical refrigeration', 'Hussmann Corporation', 185000, 320000, 32000, 0.173, 5.8, 88.6, 'completed', '2018-03-01', '2018-05-15', '2018-07-31', '2018-07-28', 5),
('WMT_DC_DALLAS', 'Solar Installation Phase 1', 'solar_installation', '2.5 MW rooftop solar PV system with 25-year PPA', 'Tesla Energy', 0, 3500000, 315000, 999.0, 0.0, 968.5, 'completed', '2021-08-01', '2021-09-15', '2022-02-28', '2022-01-15', 25),

-- JPMorgan Projects
('JPM_TOWER_NYC', 'Chiller Plant Optimization', 'HVAC_upgrade', 'Install VFDs on chiller plant, upgrade controls with predictive analytics', 'Carrier Corporation', 1250000, 1850000, 222000, 0.178, 5.6, 512.2, 'completed', '2017-01-15', '2017-02-01', '2017-06-30', '2017-05-28', 10),
('JPM_BROOKLYN', 'Window Replacement Project', 'envelope_upgrade', 'Replace single-pane windows with high-performance triple-pane units', 'Guardian Glass', 2850000, 1200000, 144000, 0.051, 19.8, 332.4, 'completed', '2019-06-01', '2019-08-15', '2020-03-31', '2020-02-28', 20),

-- GM Projects (In Progress/Planned)
('GM_WARREN_TECH', 'Compressed Air System Upgrade', 'motors_upgrade', 'Replace oversized compressors with right-sized VFD units', 'Atlas Copco', 425000, 890000, 71200, 0.168, 6.0, 246.4, 'in_progress', '2024-06-01', '2024-07-15', '2024-12-31', NULL, 5),
('GM_DETROIT_HAM', 'Waste Heat Recovery System', 'heat_recovery', 'Capture waste heat from furnaces for building heating', 'Honeywell', 1850000, 2400000, 192000, 0.104, 9.6, 664.8, 'approved', '2024-09-01', NULL, '2025-06-30', NULL, 15),

-- Amazon Projects  
('AMZN_HQ2_VAR1', 'Smart Building Controls', 'controls_upgrade', 'AI-powered building automation with occupancy-based optimization', 'Honeywell', 650000, 1100000, 132000, 0.203, 4.9, 304.6, 'completed', '2023-06-01', '2023-07-01', '2023-12-31', '2023-11-15', 5),
('AMZN_FULFILLMENT_TX', 'LED High Bay Retrofit', 'LED_retrofit', 'Replace 1,200 metal halide high bay fixtures with LED', 'Cree Lighting', 385000, 850000, 76500, 0.199, 5.0, 235.4, 'completed', '2021-10-01', '2021-11-15', '2022-02-28', '2022-01-30', 10),

-- Apple Projects
('AAPL_PARK_MAIN', 'Battery Storage System', 'battery_storage', '17 MWh battery storage system for peak shaving and grid services', 'Tesla Energy', 8500000, 0, 850000, 0.100, 10.0, 0, 'completed', '2018-01-01', '2018-03-15', '2018-09-30', '2018-08-15', 10),
('AAPL_INFINITE_LOOP', 'Geothermal System Retrofit', 'HVAC_upgrade', 'Install geothermal heat pump system to replace gas boilers', 'ClimateMaster', 1250000, 580000, 69600, 0.056, 18.0, 160.6, 'planned', '2024-11-01', NULL, '2025-08-31', NULL, 20),

-- Target Projects
('TGT_HQ_MPLS', 'Energy Management System', 'controls_upgrade', 'Advanced EMS with machine learning optimization algorithms', 'Schneider Electric', 485000, 920000, 82800, 0.171, 5.9, 254.8, 'in_progress', '2024-05-01', '2024-06-15', '2024-11-30', NULL, 5),
('TGT_STORE_001', 'Heat Pump Upgrade', 'HVAC_upgrade', 'Replace gas heating with high-efficiency heat pumps', 'Trane', 125000, 85000, 10200, 0.082, 12.3, 23.5, 'approved', '2024-10-01', NULL, '2025-01-31', NULL, 10);

-- Insert Project Opportunities (AI-identified opportunities)
INSERT INTO project_opportunities (building_id, opportunity_type, opportunity_category, title, description, identified_by, analysis_method, confidence_level, estimated_cost, annual_savings_kwh, annual_savings_cost, estimated_roi, payback_years, carbon_reduction_tons, implementation_complexity, priority_score, status) VALUES

-- Microsoft Opportunities
('MSFT_MAIN_CAMPUS', 'advanced_controls', 'controls', 'AI-Powered HVAC Optimization', 'Implement machine learning algorithms for predictive HVAC control based on occupancy patterns and weather forecasts', 'portfolio-intelligence-agent', 'ml_analysis', 'high', 350000, 580000, 58000, 0.166, 6.0, 160.6, 'medium', 85, 'identified'),
('MSFT_BUILDING_92', 'envelope_upgrade', 'envelope', 'Smart Window Film Installation', 'Install electrochromic smart glass film to reduce cooling loads and improve daylighting', 'portfolio-intelligence-agent', 'energy_audit', 'medium', 485000, 420000, 50400, 0.104, 9.6, 116.4, 'medium', 72, 'identified'),
('MSFT_DATACENTER_QN1', 'liquid_cooling', 'cooling', 'Direct Liquid Cooling for Servers', 'Implement direct-to-chip liquid cooling to reduce PUE from 1.4 to 1.15', 'portfolio-intelligence-agent', 'benchmark_comparison', 'high', 1250000, 4200000, 315000, 0.252, 4.0, 1162.8, 'high', 92, 'under_review'),

-- Walmart Opportunities
('WMT_SUPER_001', 'demand_response', 'controls', 'Automated Demand Response Program', 'Participate in utility demand response with automated load shedding during peak periods', 'portfolio-intelligence-agent', 'utility_analysis', 'high', 45000, 0, 12000, 0.267, 3.8, 0, 'low', 78, 'identified'),
('WMT_SUPER_002', 'solar_installation', 'renewable', 'Rooftop Solar PV System', '850 kW rooftop solar installation with 25-year PPA structure', 'portfolio-intelligence-agent', 'solar_analysis', 'high', 0, 1200000, 108000, 999.0, 0.0, 332.4, 'medium', 88, 'approved'),
('WMT_DC_DALLAS', 'energy_storage', 'storage', 'Battery Storage for Peak Shaving', '5 MWh battery system to reduce demand charges and provide grid services', 'portfolio-intelligence-agent', 'financial_analysis', 'medium', 2850000, 0, 285000, 0.100, 10.0, 0, 'medium', 75, 'identified'),

-- JPMorgan Opportunities
('JPM_TOWER_NYC', 'cogeneration', 'power', 'Natural Gas Cogeneration System', 'Install 2 MW CHP system for baseload power and heating', 'portfolio-intelligence-agent', 'feasibility_study', 'medium', 3500000, 5800000, 696000, 0.199, 5.0, 1606.4, 'high', 89, 'under_review'),
('JPM_BROOKLYN', 'led_retrofit', 'lighting', 'LED Lighting Conversion', 'Convert remaining fluorescent lighting to LED with daylight harvesting', 'portfolio-intelligence-agent', 'lighting_audit', 'high', 185000, 320000, 38400, 0.208, 4.8, 88.6, 'low', 82, 'identified'),

-- GM Opportunities
('GM_WARREN_TECH', 'waste_heat_recovery', 'heat_recovery', 'Industrial Waste Heat Recovery', 'Capture waste heat from manufacturing processes for space heating', 'field_engineer_analysis', 'thermal_audit', 'high', 850000, 1400000, 112000, 0.132, 7.6, 387.6, 'medium', 84, 'identified'),
('GM_DETROIT_HAM', 'motor_upgrades', 'motors', 'Premium Efficiency Motor Replacement', 'Replace standard motors with premium efficiency IE4 motors during maintenance', 'portfolio-intelligence-agent', 'equipment_analysis', 'high', 425000, 680000, 54400, 0.128, 7.8, 188.4, 'low', 76, 'identified'),

-- Amazon Opportunities
('AMZN_HQ2_VAR1', 'thermal_storage', 'storage', 'Thermal Energy Storage System', 'Install ice storage system for cooling load shifting and demand reduction', 'portfolio-intelligence-agent', 'load_analysis', 'medium', 1250000, 850000, 102000, 0.082, 12.3, 235.4, 'high', 71, 'identified'),
('AMZN_FULFILLMENT_TX', 'skylights', 'daylighting', 'Daylighting with Smart Skylights', 'Install programmable skylights with automated dimming controls', 'portfolio-intelligence-agent', 'daylighting_study', 'medium', 285000, 380000, 34200, 0.120, 8.3, 105.2, 'medium', 68, 'identified'),

-- Apple Opportunities
('AAPL_PARK_MAIN', 'thermal_comfort', 'controls', 'Personal Comfort Controls', 'Implement desk-level environmental controls for optimal comfort and energy savings', 'portfolio-intelligence-agent', 'occupant_survey', 'medium', 185000, 280000, 33600, 0.182, 5.5, 77.6, 'low', 73, 'identified'),
('AAPL_INFINITE_LOOP', 'electric_vehicle_charging', 'infrastructure', 'EV Charging Infrastructure', 'Install 50 Level 2 EV charging stations with solar canopies', 'portfolio-intelligence-agent', 'transportation_analysis', 'high', 385000, 0, 15000, 0.039, 25.7, 0, 'medium', 65, 'identified'),

-- Target Opportunities
('TGT_HQ_MPLS', 'air_sealing', 'envelope', 'Building Envelope Air Sealing', 'Comprehensive air sealing program to reduce infiltration loads', 'portfolio-intelligence-agent', 'blower_door_test', 'high', 125000, 420000, 37800, 0.302, 3.3, 116.4, 'low', 79, 'identified'),
('TGT_STORE_001', 'refrigeration_controls', 'refrigeration', 'Advanced Refrigeration Controls', 'Install floating head pressure controls and suction pressure optimization', 'portfolio-intelligence-agent', 'refrigeration_audit', 'high', 85000, 180000, 16200, 0.191, 5.2, 49.8, 'low', 74, 'identified');

-- Insert Utility Bills (Sample monthly bills for validation)
INSERT INTO utility_bills (building_id, utility_type, utility_company, account_number, bill_date, service_period_start, service_period_end, total_usage, total_cost, usage_units, rate_schedule, demand_charge, energy_charge, delivery_charge, taxes_and_fees, peak_demand_kw, validation_status) VALUES

-- Microsoft Bills
('MSFT_MAIN_CAMPUS', 'electric', 'Puget Sound Energy', 'MSFT-MAIN-001', '2024-06-15', '2024-05-15', '2024-06-14', 680500, 67250.85, 'kWh', 'Schedule 40', 26500.00, 32450.50, 6250.25, 2050.10, 2100, 'validated'),
('MSFT_MAIN_CAMPUS', 'electric', 'Puget Sound Energy', 'MSFT-MAIN-001', '2024-05-15', '2024-04-15', '2024-05-14', 715200, 71875.40, 'kWh', 'Schedule 40', 26500.00, 36125.75, 6485.30, 2764.35, 2100, 'validated'),
('MSFT_DATACENTER_QN1', 'electric', 'Grant County PUD', 'MSFT-QN1-001', '2024-06-20', '2024-05-20', '2024-06-19', 1950000, 146250.00, 'kWh', 'Industrial', 68000.00, 58500.00, 15750.00, 4000.00, 8500, 'validated'),

-- Walmart Bills  
('WMT_SUPER_001', 'electric', 'Entergy Arkansas', 'WMT-1234-001', '2024-06-25', '2024-05-25', '2024-06-24', 235800, 28296.00, 'kWh', 'Large General Service', 8005.00, 16982.40, 2354.60, 954.00, 890, 'validated'),
('WMT_DC_DALLAS', 'electric', 'Oncor Electric', 'WMT-DC-DAL-001', '2024-06-28', '2024-05-28', '2024-06-27', 680000, 61200.00, 'kWh', 'Large General Service', 19690.00, 34000.00, 6120.00, 1390.00, 2200, 'validated'),

-- JPMorgan Bills
('JPM_TOWER_NYC', 'electric', 'Con Edison', 'JPM-NYC-001', '2024-06-30', '2024-05-30', '2024-06-29', 1485000, 267300.00, 'kWh', 'General Large', 107800.00, 133650.00, 17838.00, 8012.00, 4200, 'validated'),
('JPM_TOWER_NYC', 'gas', 'Con Edison', 'JPM-NYC-GAS', '2024-06-30', '2024-05-30', '2024-06-29', 15800, 29640.00, 'therms', 'General Service', 0, 25740.00, 2844.00, 1056.00, NULL, 'validated'),

-- GM Bills
('GM_WARREN_TECH', 'electric', 'DTE Energy', 'GM-WTC-001', '2024-06-22', '2024-05-22', '2024-06-21', 2850000, 228000.00, 'kWh', 'General Primary', 112500.00, 85500.00, 22800.00, 7200.00, 12500, 'validated'),
('GM_DETROIT_HAM', 'electric', 'DTE Energy', 'GM-DHA-001', '2024-06-24', '2024-05-24', '2024-06-23', 3500000, 287000.00, 'kWh', 'General Primary', 162000.00, 105000.00, 14350.00, 5650.00, 18000, 'validated'),

-- Amazon Bills
('AMZN_HQ2_VAR1', 'electric', 'Dominion Energy', 'AMZN-HQ2-001', '2024-06-18', '2024-05-18', '2024-06-17', 985000, 118200.00, 'kWh', 'General Service', 51200.00, 59100.00, 5910.00, 1990.00, 3200, 'validated'),
('AMZN_FULFILLMENT_TX', 'electric', 'Oncor Electric', 'AMZN-DFW8-001', '2024-06-26', '2024-05-26', '2024-06-25', 580000, 52200.00, 'kWh', 'Large General Service', 25060.00, 23200.00, 2900.00, 1040.00, 2800, 'validated'),

-- Apple Bills
('AAPL_PARK_MAIN', 'electric', 'PG&E', 'AAPL-PARK-001', '2024-06-21', '2024-05-21', '2024-06-20', 685000, 137000.00, 'kWh', 'E-20', 38360.00, 82125.00, 13700.00, 2815.00, 2100, 'validated'),
('AAPL_INFINITE_LOOP', 'electric', 'PG&E', 'AAPL-IL-001', '2024-06-21', '2024-05-21', '2024-06-20', 348000, 69600.00, 'kWh', 'E-19', 19110.00, 41700.00, 6960.00, 1830.00, 1050, 'validated'),

-- Target Bills
('TGT_HQ_MPLS', 'electric', 'Xcel Energy', 'TGT-HQ-001', '2024-06-17', '2024-05-17', '2024-06-16', 1025000, 92250.00, 'kWh', 'Large General Service', 38400.00, 41000.00, 10250.00, 2600.00, 3200, 'validated'),
('TGT_HQ_MPLS', 'gas', 'CenterPoint Energy', 'TGT-HQ-GAS', '2024-06-17', '2024-05-17', '2024-06-16', 8500, 12750.00, 'therms', 'Commercial', 0, 10625.00, 1487.50, 637.50, NULL, 'validated'),
('TGT_STORE_001', 'electric', 'Xcel Energy', 'TGT-1001-001', '2024-06-19', '2024-05-19', '2024-06-18', 152000, 13680.00, 'kWh', 'Small General Service', 4640.00, 7600.00, 1216.00, 224.00, 580, 'validated');

-- Insert Energy Alerts (Recent monitoring alerts)
INSERT INTO energy_alerts (meter_id, building_id, alert_type, severity, title, description, detected_value, expected_value, threshold_value, confidence_score, detection_timestamp, estimated_cost_impact, status) VALUES

-- High Priority Alerts
('MSFT_QN1_002', 'MSFT_DATACENTER_QN1', 'demand_spike', 'critical', 'UPS System Demand Spike', 'UPS system showing 25% higher than normal power draw, possible cooling failure', 2500.0, 2000.0, 2200.0, 0.95, '2024-07-14 08:35:00', 5000.00, 'open'),
('WMT_1234_002', 'WMT_SUPER_001', 'equipment_fault', 'high', 'Refrigeration Compressor Fault', 'Refrigeration system showing erratic power consumption patterns', 145.0, 112.0, 125.0, 0.88, '2024-07-14 10:22:00', 2500.00, 'acknowledged'),
('GM_WTC_003', 'GM_WARREN_TECH', 'anomaly', 'high', 'Paint Shop Energy Anomaly', 'Paint booth ventilation system consuming 40% more energy than baseline', 1190.0, 850.0, 1000.0, 0.92, '2024-07-14 06:45:00', 3200.00, 'investigating'),

-- Medium Priority Alerts
('JPM_NYC_003', 'JPM_TOWER_NYC', 'high_usage', 'medium', 'Chiller Plant High Usage', 'Chiller plant consumption 15% above seasonal average', 1890.0, 1750.0, 1850.0, 0.78, '2024-07-14 11:15:00', 1200.00, 'open'),
('AMZN_DFW8_001', 'AMZN_FULFILLMENT_TX', 'anomaly', 'medium', 'Weekend Usage Anomaly', 'Higher than expected weekend energy consumption detected', 485.0, 320.0, 400.0, 0.72, '2024-07-13 14:30:00', 800.00, 'open'),
('TGT_HQ_001', 'TGT_HQ_MPLS', 'offline', 'medium', 'Meter Communication Lost', 'Main electric meter has not reported data for 2 hours', NULL, NULL, NULL, 1.00, '2024-07-14 09:20:00', 0.00, 'acknowledged'),

-- Low Priority Alerts
('AAPL_PARK_001', 'AAPL_PARK_MAIN', 'high_usage', 'low', 'Slightly Elevated Consumption', 'Building consumption 8% above predicted value', 2280.0, 2100.0, 2200.0, 0.65, '2024-07-14 07:00:00', 300.00, 'open'),
('MSFT_MAIN_003', 'MSFT_MAIN_CAMPUS', 'anomaly', 'low', 'Chiller Efficiency Drift', 'Chiller efficiency slowly declining over past week', 945.0, 900.0, 930.0, 0.68, '2024-07-13 16:45:00', 150.00, 'open');

-- Insert Maintenance Records (Equipment maintenance history)
INSERT INTO maintenance_records (equipment_id, building_id, maintenance_type, work_order_number, scheduled_date, actual_date, technician_name, contractor_company, description, work_performed, labor_hours, labor_cost, parts_cost, total_cost, equipment_condition, efficiency_impact, completion_status) VALUES

-- Recent Maintenance
((SELECT equipment_id FROM equipment WHERE equipment_name = 'Chiller Plant #1' AND building_id = 'MSFT_MAIN_CAMPUS'), 'MSFT_MAIN_CAMPUS', 'preventive', 'WO-2024-001234', '2024-06-15', '2024-06-15', 'John Smith', 'Carrier Service', 'Semi-annual chiller maintenance', 'Cleaned condenser tubes, checked refrigerant levels, calibrated controls', 8.0, 800.00, 450.00, 1250.00, 'good', 2.5, 'completed'),

((SELECT equipment_id FROM equipment WHERE equipment_name = 'Refrigeration Rack #1' AND building_id = 'WMT_SUPER_001'), 'WMT_SUPER_001', 'corrective', 'WO-2024-002456', '2024-07-10', '2024-07-12', 'Mike Johnson', 'Hussmann Service', 'Compressor overheating repair', 'Replaced faulty condenser fan motor, cleaned coils', 6.0, 720.00, 285.00, 1005.00, 'good', 8.0, 'completed'),

((SELECT equipment_id FROM equipment WHERE equipment_name = 'UPS System A' AND building_id = 'MSFT_DATACENTER_QN1'), 'MSFT_DATACENTER_QN1', 'preventive', 'WO-2024-003678', '2024-05-20', '2024-05-20', 'Sarah Davis', 'Schneider Service', 'Quarterly UPS maintenance', 'Battery test, firmware update, thermal imaging inspection', 4.0, 600.00, 0.00, 600.00, 'excellent', 0.0, 'completed'),

((SELECT equipment_id FROM equipment WHERE equipment_name = 'Central Chiller Plant' AND building_id = 'JPM_TOWER_NYC'), 'JPM_TOWER_NYC', 'preventive', 'WO-2024-004890', '2024-04-25', '2024-04-28', 'Robert Chen', 'York Service', 'Annual chiller overhaul', 'Complete chiller inspection, oil change, bearing replacement', 16.0, 2400.00, 1850.00, 4250.00, 'excellent', 5.0, 'completed'),

((SELECT equipment_id FROM equipment WHERE equipment_name = 'Paint Booth Ventilation' AND building_id = 'GM_WARREN_TECH'), 'GM_WARREN_TECH', 'preventive', 'WO-2024-005123', '2024-07-01', '2024-07-03', 'Lisa Rodriguez', 'Eisenmann Service', 'Quarterly ventilation maintenance', 'Filter replacement, fan balance, heat exchanger cleaning', 12.0, 1440.00, 680.00, 2120.00, 'good', 3.0, 'completed');

-- Insert Weather Data (Sample weather data for energy correlation)
DO $$
DECLARE
    building_record RECORD;
    current_date DATE := CURRENT_DATE - INTERVAL '7 days';
    end_date DATE := CURRENT_DATE;
    hour_counter INTEGER;
    base_temp DECIMAL;
    daily_temp_variation DECIMAL;
    hourly_temp DECIMAL;
    humidity DECIMAL;
    solar DECIMAL;
BEGIN
    -- Insert weather data for major building locations
    FOR building_record IN 
        SELECT DISTINCT b.building_id, b.city, b.state, b.latitude, b.longitude
        FROM buildings b
        WHERE b.building_id IN ('MSFT_MAIN_CAMPUS', 'WMT_SUPER_001', 'JPM_TOWER_NYC', 'GM_WARREN_TECH', 'AMZN_HQ2_VAR1', 'AAPL_PARK_MAIN', 'TGT_HQ_MPLS')
    LOOP
        current_date := CURRENT_DATE - INTERVAL '7 days';
        WHILE current_date <= end_date LOOP
            hour_counter := 0;
            WHILE hour_counter < 24 LOOP
                -- Calculate base temperature by location and season
                base_temp := CASE 
                    WHEN building_record.state IN ('WA', 'CA') THEN 68 + 20 * sin(2 * pi() * (EXTRACT(doy FROM current_date) - 100) / 365.0)
                    WHEN building_record.state IN ('TX', 'AR') THEN 75 + 25 * sin(2 * pi() * (EXTRACT(doy FROM current_date) - 100) / 365.0)
                    WHEN building_record.state IN ('NY', 'MI', 'MN') THEN 58 + 30 * sin(2 * pi() * (EXTRACT(doy FROM current_date) - 100) / 365.0)
                    WHEN building_record.state = 'VA' THEN 65 + 25 * sin(2 * pi() * (EXTRACT(doy FROM current_date) - 100) / 365.0)
                    ELSE 65 + 25 * sin(2 * pi() * (EXTRACT(doy FROM current_date) - 100) / 365.0)
                END;
                
                -- Daily temperature variation
                daily_temp_variation := 15 * sin(2 * pi() * hour_counter / 24.0 - pi()/2);
                hourly_temp := base_temp + daily_temp_variation + (random() - 0.5) * 8;
                
                -- Humidity calculation (higher in summer, varies by region)
                humidity := 45 + 30 * sin(2 * pi() * (EXTRACT(doy FROM current_date) - 100) / 365.0) + (random() - 0.5) * 20;
                humidity := GREATEST(20, LEAST(95, humidity));
                
                -- Solar irradiance (peak at noon, zero at night)
                IF hour_counter BETWEEN 6 AND 18 THEN
                    solar := 1000 * sin(pi() * (hour_counter - 6) / 12.0) * (0.7 + random() * 0.3);
                ELSE
                    solar := 0;
                END IF;
                
                INSERT INTO weather_data (
                    building_id, reading_date, temperature_f, humidity_percent, 
                    solar_irradiance, wind_speed_mph, cloud_cover_percent,
                    heating_degree_days, cooling_degree_days
                ) VALUES (
                    building_record.building_id,
                    current_date + (hour_counter * INTERVAL '1 hour'),
                    hourly_temp,
                    humidity,
                    solar,
                    5 + random() * 15, -- wind speed
                    random() * 100, -- cloud cover
                    GREATEST(0, 65 - hourly_temp), -- HDD
                    GREATEST(0, hourly_temp - 65)  -- CDD
                );
                
                hour_counter := hour_counter + 1;
            END LOOP;
            current_date := current_date + INTERVAL '1 day';
        END LOOP;
    END LOOP;
END $$;

-- Insert Sample Sustainability Reports
INSERT INTO sustainability_reports (portfolio_id, report_type, reporting_period_start, reporting_period_end, total_energy_consumption_kwh, total_energy_cost, electricity_consumption_kwh, gas_consumption_therms, renewable_energy_kwh, renewable_energy_percent, total_carbon_emissions_tons, scope_1_emissions, scope_2_emissions, energy_intensity_kwh_per_sqft, energy_cost_per_sqft, energy_star_avg_score, projects_completed, total_savings_kwh, total_savings_cost, carbon_reduction_tons, executive_summary, key_findings, report_data) VALUES

-- Microsoft Q2 2024 Report
('MSFT_PORTFOLIO', 'executive', '2024-04-01', '2024-06-30', 45500000, 3640000, 42800000, 158000, 21400000, 50.0, 12580.5, 2840.2, 9740.3, 45.2, 3.64, 88, 3, 3930000, 393000, 1088.9, 
'Microsoft continues to exceed sustainability targets with 50% renewable energy achievement and significant energy efficiency improvements across the portfolio.',
'Key achievements include completion of three major energy projects, 15% reduction in energy intensity, and early achievement of renewable energy milestones.',
'{"projects": [{"name": "LED Retrofit", "savings": 450000}, {"name": "HVAC Controls", "savings": 680000}, {"name": "Free Cooling", "savings": 2800000}], "benchmarks": {"energy_star_improvement": "+8%", "carbon_intensity_reduction": "12%"}}'
),

-- Walmart Q2 2024 Report  
('WMT_PORTFOLIO', 'executive', '2024-04-01', '2024-06-30', 298500000, 23880000, 285600000, 780000, 89250000, 31.2, 82580.4, 14040.6, 68539.8, 68.5, 5.49, 78, 2, 3820000, 347000, 1057.1,
'Walmart achieved significant progress toward zero emissions goals with major renewable energy additions and continued efficiency improvements.',
'Completed solar installation at Dallas DC contributing 31% renewable energy portfolio-wide. Refrigeration upgrades delivered substantial efficiency gains.',
'{"renewable_projects": [{"location": "Dallas DC", "capacity_mw": 2.5, "annual_generation": 3500000}], "efficiency_programs": {"refrigeration_upgrades": 15, "led_retrofits": 28}}'
),

-- JPMorgan Q2 2024 Report
('JPM_PORTFOLIO', 'executive', '2024-04-01', '2024-06-30', 82500000, 9900000, 79200000, 195000, 15840000, 20.0, 22770.0, 3510.0, 19260.0, 48.6, 5.83, 90, 2, 3050000, 366000, 844.6,
'JPMorgan Chase demonstrates strong environmental leadership with continued energy efficiency gains and progress toward carbon neutrality.',
'Portfolio optimization projects delivered 12% reduction in energy intensity. Advanced building controls show promising results for continued savings.',
'{"carbon_neutral_progress": "45%", "energy_efficiency_improvement": "12%", "green_building_certification": {"leed_buildings": 18, "energy_star_score_avg": 90}}'
);

-- Create sample data summary
SELECT 'Database populated with comprehensive sample data:' as message
UNION ALL SELECT '- ' || COUNT(*) || ' Users' FROM users
UNION ALL SELECT '- ' || COUNT(*) || ' Portfolios' FROM portfolios  
UNION ALL SELECT '- ' || COUNT(*) || ' Buildings' FROM buildings
UNION ALL SELECT '- ' || COUNT(*) || ' Equipment records' FROM equipment
UNION ALL SELECT '- ' || COUNT(*) || ' Energy meters' FROM energy_meters
UNION ALL SELECT '- ' || COUNT(*) || ' Energy usage records' FROM energy_usage
UNION ALL SELECT '- ' || COUNT(*) || ' Energy alerts' FROM energy_alerts
UNION ALL SELECT '- ' || COUNT(*) || ' Utility bills' FROM utility_bills
UNION ALL SELECT '- ' || COUNT(*) || ' Market rates' FROM market_rates
UNION ALL SELECT '- ' || COUNT(*) || ' Energy projects' FROM energy_projects
UNION ALL SELECT '- ' || COUNT(*) || ' Project opportunities' FROM project_opportunities
UNION ALL SELECT '- ' || COUNT(*) || ' Maintenance records' FROM maintenance_records
UNION ALL SELECT '- ' || COUNT(*) || ' Weather data points' FROM weather_data
UNION ALL SELECT '- ' || COUNT(*) || ' Benchmark records' FROM benchmark_data
UNION ALL SELECT '- ' || COUNT(*) || ' Sustainability reports' FROM sustainability_reports;

-- Refresh materialized view with new data
REFRESH MATERIALIZED VIEW mv_daily_building_summary;