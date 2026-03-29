@echo off
title Smart Workflow Tools - All Services Launcher
color 0A

echo.
echo ========================================
echo   Smart Workflow Tools - All Services
echo ========================================
echo.

echo [1/6] Checking prerequisites...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python first.
    pause
    exit /b 1
)

echo [SUCCESS] Prerequisites check passed
echo.

echo [2/6] Starting Login Service...
cd /d "%~dp0login\new-project"
start "Login Service" cmd /k "node app.js"
timeout /t 3 /nobreak >nul

echo [3/6] Starting Unified Dashboard...
cd /d "%~dp0unified-dashboard"
start "Unified Dashboard" cmd /k "node app.js"
timeout /t 3 /nobreak >nul

echo [4/6] Starting Resume Scanner...
cd /d "%~dp0Smart-Workflow-Tools-v2\resume"
start "Resume Scanner" cmd /k "python simple_app.py"
timeout /t 3 /nobreak >nul

echo [5/6] Starting Email Marketing...
cd /d "%~dp0COLD-EMAIL"
start "Email Marketing" cmd /k "npm start"
timeout /t 3 /nobreak >nul

echo [6/6] Starting Gmail Automation...
cd /d "%~dp0gmail-to-sheets"
start "Gmail Automation" cmd /k "python src/main.py"
timeout /t 3 /nobreak >nul

echo [7/7] Starting Developer Tools...
cd /d "%~dp0practice"
start "Developer Tools" cmd /k "node app.js"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   Services Status Check
echo ========================================
echo.

echo Checking services...
timeout /t 5 /nobreak >nul

netstat -an | findstr :3000 >nul && echo [SUCCESS] Login Service - Running on port 3000 || echo [ERROR] Login Service - Not running
netstat -an | findstr :3010 >nul && echo [SUCCESS] Unified Dashboard - Running on port 3010 || echo [ERROR] Unified Dashboard - Not running
netstat -an | findstr :5000 >nul && echo [SUCCESS] Resume Scanner - Running on port 5000 || echo [ERROR] Resume Scanner - Not running
netstat -an | findstr :3001 >nul && echo [SUCCESS] Email Marketing - Running on port 3001 || echo [ERROR] Email Marketing - Not running
netstat -an | findstr :8000 >nul && echo [SUCCESS] Gmail Automation - Running on port 8000 || echo [ERROR] Gmail Automation - Not running
netstat -an | findstr :4000 >nul && echo [SUCCESS] Developer Tools - Running on port 4000 || echo [ERROR] Developer Tools - Not running

echo.
echo ========================================
echo   Launching Dashboard
echo ========================================
echo.

echo Opening Unified Dashboard in your default browser...
start http://localhost:3010

echo.
echo [SUCCESS] Smart Workflow Tools is now running!
echo [INFO] Unified Dashboard: http://localhost:3010
echo [INFO] All services are accessible from the dashboard
echo [INFO] Close this window to stop all services
echo.

pause
