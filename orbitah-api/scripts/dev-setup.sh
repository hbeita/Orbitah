#!/bin/bash

# Development setup script for Orbitah API

echo "🚀 Orbitah Development Setup"
echo "=============================="

# Function to start development environment
start_dev() {
    echo "📊 Starting development environment with orbitahdb_dev..."
    export SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://orbitah:orbitahpassword@localhost:5433/orbitahdb_dev"
    echo "✅ Database URL set to: $SQLALCHEMY_DATABASE_URL"
    echo "🔧 Starting API server..."
    python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8001
}

# Function to start test environment
start_test() {
    echo "🧪 Starting test environment with orbitahdb_test..."
    export SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://orbitah:orbitahpassword@localhost:5433/orbitahdb_test"
    echo "✅ Database URL set to: $SQLALCHEMY_DATABASE_URL"
    echo "🔧 Starting API server..."
    python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8001
}

# Function to start production environment
start_prod() {
    echo "🏭 Starting production environment with orbitahdb..."
    export SQLALCHEMY_DATABASE_URL="postgresql+psycopg2://orbitah:orbitahpassword@localhost:5433/orbitahdb"
    echo "✅ Database URL set to: $SQLALCHEMY_DATABASE_URL"
    echo "🔧 Starting API server..."
    python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8001
}

# Function to reset development database
reset_dev_db() {
    echo "🗑️  Resetting development database..."
    docker exec orbitah-api-db-1 psql -U orbitah -d orbitahdb_dev -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
    echo "✅ Development database reset complete!"
}

# Function to reset test database
reset_test_db() {
    echo "🗑️  Resetting test database..."
    docker exec orbitah-api-db-1 psql -U orbitah -d orbitahdb_test -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
    echo "✅ Test database reset complete!"
}

# Function to show database status
show_status() {
    echo "📊 Database Status:"
    echo "=================="
    docker exec orbitah-api-db-1 psql -U orbitah -d orbitahdb -c "\l" | grep orbitah
}

# Main script logic
case "$1" in
    "dev")
        start_dev
        ;;
    "test")
        start_test
        ;;
    "prod")
        start_prod
        ;;
    "reset-dev")
        reset_dev_db
        ;;
    "reset-test")
        reset_test_db
        ;;
    "status")
        show_status
        ;;
    *)
        echo "Usage: $0 {dev|test|prod|reset-dev|reset-test|status}"
        echo ""
        echo "Commands:"
        echo "  dev        - Start API with development database (orbitahdb_dev)"
        echo "  test       - Start API with test database (orbitahdb_test)"
        echo "  prod       - Start API with production database (orbitahdb)"
        echo "  reset-dev  - Reset development database (clear all data)"
        echo "  reset-test - Reset test database (clear all data)"
        echo "  status     - Show database status"
        echo ""
        echo "Examples:"
        echo "  $0 dev        # Start development environment"
        echo "  $0 reset-dev  # Reset development database"
        ;;
esac
