#!/bin/bash
# RaidScanner Startup Script

echo "========================================"
echo "  RaidScanner - Choose Mode"
echo "========================================"
echo ""
echo "1. Web Interface (GUI)"
echo "2. CLI Mode (Terminal)"
echo ""
read -p "Select mode [1-2]: " mode

case $mode in
    1)
        echo "Starting Web Interface..."
        python3 app.py
        ;;
    2)
        echo "Starting CLI Mode..."
        python3 main.py
        ;;
    *)
        echo "Invalid selection. Starting CLI Mode..."
        python3 main.py
        ;;
esac
