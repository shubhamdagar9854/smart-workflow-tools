#!/bin/bash

# Smart Workflow Tools - All Services Launcher
# This script starts all services and opens the unified dashboard

echo "🚀 Starting Smart Workflow Tools - All Services..."
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to start service in background
start_service() {
    local service_name=$1
    local service_path=$2
    local service_command=$3
    local port=$4
    
    echo -e "${BLUE}Starting $service_name...${NC}"
    
    if check_port $port; then
        echo -e "${YELLOW}⚠️  Port $port is already in use. Please stop the service first.${NC}"
        return 1
    fi
    
    cd "$service_path"
    nohup $service_command > "$service_name.log" 2>&1 &
    local pid=$!
    
    sleep 2
    
    if check_port $port; then
        echo -e "${GREEN}✅ $service_name started successfully (PID: $pid, Port: $port)${NC}"
        echo $pid > "$service_name.pid"
        return 0
    else
        echo -e "${RED}❌ Failed to start $service_name${NC}"
        return 1
    fi
}

# Main execution
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js first.${NC}"
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python is not installed. Please install Python first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Get the current directory
CURRENT_DIR=$(pwd)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${YELLOW}📂 Project Root: $PROJECT_ROOT${NC}"

# Start all services
echo -e "${YELLOW}🚀 Starting all services...${NC}"

# 1. Login Service
start_service "Login-Service" "$PROJECT_ROOT/login/new-project" "node app.js" 3000

# 2. Unified Dashboard
start_service "Unified-Dashboard" "$PROJECT_ROOT/unified-dashboard" "node app.js" 3010

# 3. Resume Scanner
start_service "Resume-Scanner" "$PROJECT_ROOT/Smart-Workflow-Tools-v2/resume" "python simple_app.py" 5000

# 4. Email Marketing
start_service "Email-Marketing" "$PROJECT_ROOT/COLD-EMAIL" "npm start" 3001

# 5. Gmail Automation
start_service "Gmail-Automation" "$PROJECT_ROOT/gmail-to-sheets" "python src/main.py" 8000

# 6. Developer Tools
start_service "Developer-Tools" "$PROJECT_ROOT/practice" "node app.js" 4000

echo -e "${YELLOW}⏳ Waiting for services to fully start...${NC}"
sleep 5

# Check service status
echo -e "${YELLOW}📊 Service Status:${NC}"

services=(
    "Login-Service:3000"
    "Unified-Dashboard:3010"
    "Resume-Scanner:5000"
    "Email-Marketing:3001"
    "Gmail-Automation:8000"
    "Developer-Tools:4000"
)

for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    
    if check_port $port; then
        echo -e "${GREEN}✅ $name - Running on port $port${NC}"
    else
        echo -e "${RED}❌ $name - Not running on port $port${NC}"
    fi
done

# Open the unified dashboard
echo -e "${YELLOW}🌐 Opening Unified Dashboard...${NC}"

# Try to open in browser (works on macOS, Linux, and Windows)
if command -v open &> /dev/null; then
    open http://localhost:3010
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3010
elif command -v start &> /dev/null; then
    start http://localhost:3010
else
    echo -e "${YELLOW}📱 Please open http://localhost:3010 in your browser${NC}"
fi

echo -e "${GREEN}🎉 Smart Workflow Tools is now running!${NC}"
echo -e "${GREEN}📊 Unified Dashboard: http://localhost:3010${NC}"
echo -e "${GREEN}📋 All services are accessible from the dashboard${NC}"
echo -e "${YELLOW}💡 Press Ctrl+C to stop all services${NC}"

# Function to cleanup on exit
cleanup() {
    echo -e "${YELLOW}🛑 Stopping all services...${NC}"
    
    # Kill all background processes
    pkill -f "node app.js"
    pkill -f "python simple_app.py"
    pkill -f "npm start"
    pkill -f "python src/main.py"
    
    echo -e "${GREEN}✅ All services stopped${NC}"
    exit 0
}

# Set up signal handler for cleanup
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
