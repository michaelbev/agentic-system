-- Drop all tables for Energy as a Service Platform (in dependency-safe order)

-- Drop views first
DROP VIEW IF EXISTS opportunity_pipeline;
DROP VIEW IF EXISTS building_energy_performance;
DROP VIEW IF EXISTS portfolio_summary;

-- Drop tables in dependency-safe order
DROP TABLE IF EXISTS sustainability_reports CASCADE;
DROP TABLE IF EXISTS benchmark_data CASCADE;
DROP TABLE IF EXISTS project_opportunities CASCADE;
DROP TABLE IF EXISTS energy_projects CASCADE;
DROP TABLE IF EXISTS energy_usage CASCADE;
DROP TABLE IF EXISTS energy_meters CASCADE;
DROP TABLE IF EXISTS buildings CASCADE;
DROP TABLE IF EXISTS portfolios CASCADE;

-- Drop extensions if needed
-- DROP EXTENSION IF EXISTS "uuid-ossp"; 