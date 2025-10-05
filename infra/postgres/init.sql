-- Initial database setup
-- This runs once when the container first starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Verify database is ready
SELECT 'Database initialized successfully' AS status;
