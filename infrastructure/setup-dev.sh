#!/bin/bash

# Development Environment Setup Script
# This script sets up the Docker development environment for the Multi-Agent MCP Orchestration System

set -e

echo "🚀 Setting up Multi-Agent MCP Orchestration System Development Environment"
echo "=================================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p ../logs ../data ../tests/files

# Copy environment file if it doesn't exist
if [ ! -f ../.env ]; then
    echo "📝 Creating .env file from template..."
    cp ../.env.example ../.env
    echo "⚠️  Please update ../.env with your API keys and configuration"
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose -f docker-compose.dev.yml build

echo "🚀 Starting development services..."
docker-compose -f docker-compose.dev.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
docker-compose -f docker-compose.dev.yml ps

# Show logs
echo "📋 Recent logs:"
docker-compose -f docker-compose.dev.yml logs --tail=20

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "🌐 Services available at:"
echo "   - Orchestration: http://localhost:8080"
echo "   - Energy Agent: http://localhost:5052"
echo "   - Database Agent: http://localhost:5053"
echo "   - Textract Agent: http://localhost:5054"
echo "   - Summarize Agent: http://localhost:5055"
echo "   - Time Agent: http://localhost:5051"
echo "   - PostgreSQL: localhost:5432"
echo "   - Redis: localhost:6379"
echo "   - Prometheus: http://localhost:9090"
echo "   - Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "📝 Useful commands:"
echo "   - View logs: docker-compose -f docker-compose.dev.yml logs -f [service]"
echo "   - Stop services: docker-compose -f docker-compose.dev.yml down"
echo "   - Restart services: docker-compose -f docker-compose.dev.yml restart"
echo "   - Rebuild: docker-compose -f docker-compose.dev.yml up --build"
echo ""
echo "🔧 Next steps:"
echo "   1. Update ../.env with your API keys"
echo "   2. Run database setup: ./scripts/setup_database.sh"
echo "   3. Test the system: python tests/run_tests.py" 