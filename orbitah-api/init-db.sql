-- Create development database
CREATE DATABASE orbitahdb_dev;

-- Create test database
CREATE DATABASE orbitahdb_test;

-- Grant permissions to the orbitah user
GRANT ALL PRIVILEGES ON DATABASE orbitahdb_dev TO orbitah;
GRANT ALL PRIVILEGES ON DATABASE orbitahdb_test TO orbitah;
