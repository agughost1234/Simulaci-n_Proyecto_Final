-- Initialization script for PostgreSQL
-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schema if needed
CREATE SCHEMA IF NOT EXISTS public;

-- Grant privileges
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;
