@echo off
REM RaidScanner Docker Run Script for Windows
REM This script builds and runs the RaidScanner container

echo Building RaidScanner Docker image...
docker-compose build

if %errorlevel% neq 0 (
    echo Failed to build Docker image.
    pause
    exit /b %errorlevel%
)

echo.
echo Starting RaidScanner container...
docker-compose run --rm raidscanner

echo.
echo Scan complete! Check the .\output and .\reports directories for results.
pause
