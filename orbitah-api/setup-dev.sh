#!/bin/bash

echo "🚀 Setting up Orbitah Development Environment"
echo "============================================="

# Set the development database URL
export SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://orbitah:orbitahpassword@localhost:5433/orbitahdb_dev"

echo "📊 Using database: orbitahdb_dev"
echo "🔗 Database URL: $SQLALCHEMY_DATABASE_URL"

# Create tables in development database
echo "🔧 Creating database tables..."
cd /Users/hectorgarciabeita/Hec-Projects/Orbitah/orbitah-api
python -c "from api.database import Base, engine; Base.metadata.create_all(bind=engine); print('✅ Tables created successfully')"

# Start the API server
echo "🚀 Starting API server..."
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8001
