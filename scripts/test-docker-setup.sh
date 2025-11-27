#!/bin/bash

# Docker Setup Test Script
# Verifies that Docker environment is ready for RaidScanner

echo "🔍 Testing RaidScanner Docker Setup"
echo "===================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Test 1: Check if Docker is installed
echo -n "1. Checking Docker installation... "
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ PASSED${NC}"
    DOCKER_VERSION=$(docker --version)
    echo "   $DOCKER_VERSION"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "   Docker is not installed. Please install Docker first."
    ((FAILED++))
fi

# Test 2: Check if Docker daemon is running
echo -n "2. Checking Docker daemon... "
if docker info &> /dev/null; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "   Docker daemon is not running. Please start Docker."
    ((FAILED++))
fi

# Test 3: Check if docker-compose is installed
echo -n "3. Checking docker-compose... "
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓ PASSED${NC}"
    COMPOSE_VERSION=$(docker-compose --version)
    echo "   $COMPOSE_VERSION"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "   docker-compose is not installed."
    ((FAILED++))
fi

# Test 4: Check if Dockerfile exists
echo -n "4. Checking Dockerfile... "
if [ -f "Dockerfile" ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "   Dockerfile not found in current directory."
    ((FAILED++))
fi

# Test 5: Check if docker-compose.yml exists
echo -n "5. Checking docker-compose.yml... "
if [ -f "docker-compose.yml" ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "   docker-compose.yml not found."
    ((FAILED++))
fi

# Test 6: Check if required files exist
echo -n "6. Checking required files... "
if [ -f "main.py" ] && [ -f "requirements.txt" ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "   main.py or requirements.txt not found."
    ((FAILED++))
fi

# Test 7: Check if payloads directory exists
echo -n "7. Checking payloads directory... "
if [ -d "payloads" ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    PAYLOAD_COUNT=$(find payloads -type f | wc -l)
    echo "   Found $PAYLOAD_COUNT payload files"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "   payloads directory not found."
    ((FAILED++))
fi

# Test 8: Check if scripts are executable
echo -n "8. Checking script permissions... "
if [ -x "docker-run.sh" ] && [ -x "docker-commands.sh" ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC}"
    echo "   Scripts are not executable. Run: chmod +x docker-run.sh docker-commands.sh"
    ((PASSED++))
fi

# Test 9: Validate docker-compose.yml syntax
echo -n "9. Validating docker-compose.yml... "
if docker-compose config &> /dev/null; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "   docker-compose.yml has syntax errors."
    ((FAILED++))
fi

# Test 10: Check available disk space
echo -n "10. Checking disk space... "
AVAILABLE_SPACE=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$AVAILABLE_SPACE" -gt 5 ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    echo "    Available: ${AVAILABLE_SPACE}GB"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARNING${NC}"
    echo "    Available: ${AVAILABLE_SPACE}GB (Recommended: >5GB)"
    ((PASSED++))
fi

# Summary
echo ""
echo "===================================="
echo "Test Results:"
echo "  Passed: ${GREEN}$PASSED${NC}"
echo "  Failed: ${RED}$FAILED${NC}"
echo "===================================="
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed! Your Docker setup is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Build the image: docker-compose build"
    echo "  2. Run the scanner: docker-compose run --rm raidscanner"
    echo "  or simply run: ./docker-run.sh"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Please fix the issues above.${NC}"
    exit 1
fi
