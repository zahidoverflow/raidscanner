#!/bin/bash

# RaidScanner Docker Run Script
# This script builds and runs the RaidScanner container

echo "🚀 Building RaidScanner Docker image..."
docker-compose build

echo ""
echo "🔍 Starting RaidScanner container..."
docker-compose run --rm raidscanner

echo ""
echo "✅ Scan complete! Check the ./output and ./reports directories for results."
