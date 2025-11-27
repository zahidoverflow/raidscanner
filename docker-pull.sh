#!/bin/bash

# Quick Pull and Run Script for RaidScanner from Docker Hub
# No build required!

echo "🐳 Pulling RaidScanner from Docker Hub..."
docker pull zahidoverflow/raidscanner:latest

echo ""
echo "🔍 Starting RaidScanner..."
docker run -it --rm \
  -v "$(pwd)/output:/app/output" \
  -v "$(pwd)/reports:/app/reports" \
  --shm-size=2g \
  zahidoverflow/raidscanner:latest

echo ""
echo "✅ Scan complete! Check ./output and ./reports for results."
