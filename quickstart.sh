#!/bin/bash

# LazyMail Quick Start Script
# This script helps you quickly set up and run LazyMail

set -e  # Exit on error

echo "=========================================="
echo "  LazyMail - Quick Start Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Docker is installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file${NC}"
        echo -e "${YELLOW}⚠ Please edit .env and update passwords before production use!${NC}"
    else
        echo -e "${RED}Error: .env.example not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

echo ""
echo "Starting Docker services..."
echo "This may take a few minutes on first run..."
echo ""

# Start Docker Compose services
docker-compose up -d

echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Check service health
echo ""
echo "Checking service status..."

# Check if postgres is ready
if docker-compose ps | grep -q "postgres.*Up"; then
    echo -e "${GREEN}✓ PostgreSQL is running${NC}"
else
    echo -e "${RED}✗ PostgreSQL is not running${NC}"
fi

# Check if redis is ready
if docker-compose ps | grep -q "redis.*Up"; then
    echo -e "${GREEN}✓ Redis is running${NC}"
else
    echo -e "${RED}✗ Redis is not running${NC}"
fi

# Check if rspamd is ready
if docker-compose ps | grep -q "rspamd.*Up"; then
    echo -e "${GREEN}✓ Rspamd is running${NC}"
else
    echo -e "${RED}✗ Rspamd is not running${NC}"
fi

echo ""
echo "=========================================="
echo "  Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Services are now running:"
echo ""
echo "  PostgreSQL:  localhost:5432"
echo "  Redis:       localhost:6379"
echo "  Rspamd:      localhost:11334"
echo ""
echo "Next steps:"
echo ""
echo "  1. Run database migrations:"
echo "     cd services/api"
echo "     alembic upgrade head"
echo ""
echo "  2. Start the API server:"
echo "     cd services/api"
echo "     uvicorn app.main:app --reload"
echo ""
echo "  3. Access the API documentation:"
echo "     http://localhost:8000/docs"
echo ""
echo "  4. Check service health:"
echo "     curl http://localhost:8000/api/v1/health/all"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "=========================================="
