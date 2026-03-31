const { spawn } = require('child_process');
const express = require('express');
const path = require('path');
const axios = require('axios');
const app = express();
const PORT = 3010;

// Service configuration
const SERVICES = {
    login: {
        name: 'Login Service',
        port: 3000,
        command: 'node',
        args: ['app.js'],
        path: './login/new-project',
        url: 'https://localhost:3000',
        icon: 'fa-lock'
    },
    resume: {
        name: 'Resume Scanner',
        port: 5000,
        command: 'python',
        args: ['simple_app.py'],
        path: './Smart-Workflow-Tools-v2/resume',
        url: 'http://localhost:5000',
        icon: 'fa-file-alt'
    },
    email: {
        name: 'Email Marketing',
        port: 3001,
        command: 'npm',
        args: ['start'],
        path: './COLD-EMAIL',
        url: 'http://localhost:3001',
        icon: 'fa-envelope'
    },
    gmail: {
        name: 'Gmail Automation',
        port: 8000,
        command: 'python',
        args: ['src/main.py'],
        path: './gmail-to-sheets',
        url: 'http://localhost:8000',
        icon: 'fa-google'
    },
    devtools: {
        name: 'Developer Tools',
        port: 4000,
        command: 'node',
        args: ['app.js'],
        path: './practice',
        url: 'http://localhost:4000',
        icon: 'fa-code'
    }
};

// Running services tracking
const runningServices = new Map();

// Start a service
function startService(serviceKey) {
    const service = SERVICES[serviceKey];
    if (runningServices.has(serviceKey)) {
        console.log(`⚠️  ${service.name} is already running`);
        return;
    }

    console.log(`🚀 Starting ${service.name}...`);
    
    const child = spawn(service.command, service.args, {
        cwd: path.resolve(service.path),
        stdio: ['pipe', 'pipe', 'pipe'],
        shell: true
    });

    runningServices.set(serviceKey, child);

    child.stdout.on('data', (data) => {
        console.log(`[${service.name}] ${data.toString().trim()}`);
    });

    child.stderr.on('data', (data) => {
        console.log(`[${service.name} ERROR] ${data.toString().trim()}`);
    });

    child.on('close', (code) => {
        console.log(`${service.name} stopped with code ${code}`);
        runningServices.delete(serviceKey);
    });

    // Wait a moment and check if service is responding
    setTimeout(() => {
        checkServiceHealth(serviceKey);
    }, 3000);
}

// Check service health
async function checkServiceHealth(serviceKey) {
    const service = SERVICES[serviceKey];
    try {
        const response = await axios.get(service.url, { 
            timeout: 2000,
            httpsAgent: new (require('https').Agent)({ rejectUnauthorized: false })
        });
        console.log(`✅ ${service.name} is healthy and running`);
        return true;
    } catch (error) {
        console.log(`❌ ${service.name} health check failed: ${error.message}`);
        return false;
    }
}

// Stop a service
function stopService(serviceKey) {
    const service = SERVICES[serviceKey];
    const child = runningServices.get(serviceKey);
    
    if (child) {
        child.kill('SIGTERM');
        runningServices.delete(serviceKey);
        console.log(`🛑 Stopped ${service.name}`);
    } else {
        console.log(`⚠️  ${service.name} is not running`);
    }
}

// Stop all services
function stopAllServices() {
    console.log('🛑 Stopping all services...');
    runningServices.forEach((child, serviceKey) => {
        stopService(serviceKey);
    });
}

// Express middleware
app.use(express.json());
app.use(express.static('public'));

// Main dashboard route
app.get('/', async (req, res) => {
    const serviceStatuses = [];
    
    for (const [serviceKey, service] of Object.entries(SERVICES)) {
        const isRunning = runningServices.has(serviceKey);
        let status = 'stopped';
        
        if (isRunning) {
            try {
                await checkServiceHealth(serviceKey);
                status = 'running';
            } catch (error) {
                status = 'error';
            }
        }
        
        serviceStatuses.push({
            ...service,
            key: serviceKey,
            status: status,
            isRunning: isRunning
        });
    }

    res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Workflow Tools - Master Controller</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-header {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        .service-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            position: relative;
        }
        .service-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        .service-icon {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .status-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .status-running {
            background: #10b981;
            color: white;
        }
        .status-stopped {
            background: #6b7280;
            color: white;
        }
        .status-error {
            background: #ef4444;
            color: white;
        }
        .control-btn {
            padding: 8px 16px;
            border-radius: 20px;
            border: none;
            font-size: 0.9rem;
            margin: 2px;
            transition: all 0.3s ease;
        }
        .start-btn {
            background: #10b981;
            color: white;
        }
        .stop-btn {
            background: #ef4444;
            color: white;
        }
        .launch-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }
        .control-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }
        .master-controls {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>
    <header class="main-header py-3">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-6">
                    <h1 class="text-white mb-0">
                        <i class="fas fa-rocket me-2"></i>
                        Smart Workflow Tools
                    </h1>
                    <p class="text-white-50 mb-0">Master Service Controller</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <div class="text-white">
                        <i class="fas fa-clock me-2"></i>
                        <span id="current-time"></span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <div class="container py-5">
        <!-- Master Controls -->
        <div class="master-controls text-center text-white">
            <h3 class="mb-4">Master Controls</h3>
            <button class="control-btn start-btn me-2" onclick="startAllServices()">
                <i class="fas fa-play me-1"></i> Start All Services
            </button>
            <button class="control-btn stop-btn me-2" onclick="stopAllServices()">
                <i class="fas fa-stop me-1"></i> Stop All Services
            </button>
            <button class="control-btn launch-btn" onclick="refreshStatus()">
                <i class="fas fa-sync-alt me-1"></i> Refresh Status
            </button>
        </div>

        <!-- Services Grid -->
        <div class="row">
            ${serviceStatuses.map(service => `
                <div class="col-md-6 col-lg-4">
                    <div class="service-card">
                        <div class="status-badge status-${service.status}">
                            ${service.status.toUpperCase()}
                        </div>
                        <div class="text-center">
                            <div class="service-icon">
                                <i class="fas ${service.icon}"></i>
                            </div>
                            <h5>${service.name}</h5>
                            <p class="text-muted small">Port ${service.port}</p>
                            <div class="mb-3">
                                <button class="control-btn start-btn" onclick="startService('${service.key}')" 
                                        ${service.isRunning ? 'disabled' : ''}>
                                    <i class="fas fa-play me-1"></i> Start
                                </button>
                                <button class="control-btn stop-btn" onclick="stopService('${service.key}')" 
                                        ${!service.isRunning ? 'disabled' : ''}>
                                    <i class="fas fa-stop me-1"></i> Stop
                                </button>
                            </div>
                            ${service.status === 'running' ? `
                                <button class="control-btn launch-btn" onclick="launchService('${service.url}')">
                                    <i class="fas fa-external-link-alt me-1"></i> Launch
                                </button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    </div>

    <script>
        // Update current time
        function updateTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = 
                now.toLocaleString('en-US', { 
                    weekday: 'short', 
                    year: 'numeric', 
                    month: 'short', 
                    day: 'numeric', 
                    hour: '2-digit', 
                    minute: '2-digit' 
                });
        }
        updateTime();
        setInterval(updateTime, 1000);

        // Service control functions
        async function startService(serviceKey) {
            try {
                const response = await fetch('/api/start/' + serviceKey);
                const result = await response.json();
                if (result.success) {
                    setTimeout(() => location.reload(), 2000);
                }
            } catch (error) {
                console.error('Error starting service:', error);
            }
        }

        async function stopService(serviceKey) {
            try {
                const response = await fetch('/api/stop/' + serviceKey);
                const result = await response.json();
                if (result.success) {
                    setTimeout(() => location.reload(), 1000);
                }
            } catch (error) {
                console.error('Error stopping service:', error);
            }
        }

        async function startAllServices() {
            try {
                const response = await fetch('/api/start-all');
                const result = await response.json();
                if (result.success) {
                    setTimeout(() => location.reload(), 5000);
                }
            } catch (error) {
                console.error('Error starting all services:', error);
            }
        }

        async function stopAllServices() {
            try {
                const response = await fetch('/api/stop-all');
                const result = await response.json();
                if (result.success) {
                    setTimeout(() => location.reload(), 2000);
                }
            } catch (error) {
                console.error('Error stopping all services:', error);
            }
        }

        function launchService(url) {
            window.open(url, '_blank');
        }

        function refreshStatus() {
            location.reload();
        }

        // Auto-refresh every 10 seconds
        setInterval(() => {
            location.reload();
        }, 10000);
    </script>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    `);
});

// API routes for service control
app.post('/api/start/:serviceKey', (req, res) => {
    const serviceKey = req.params.serviceKey;
    startService(serviceKey);
    res.json({ success: true, message: `Starting ${SERVICES[serviceKey].name}` });
});

app.post('/api/stop/:serviceKey', (req, res) => {
    const serviceKey = req.params.serviceKey;
    stopService(serviceKey);
    res.json({ success: true, message: `Stopping ${SERVICES[serviceKey].name}` });
});

app.post('/api/start-all', (req, res) => {
    Object.keys(SERVICES).forEach(serviceKey => {
        setTimeout(() => startService(serviceKey), Object.keys(SERVICES).indexOf(serviceKey) * 1000);
    });
    res.json({ success: true, message: 'Starting all services' });
});

app.post('/api/stop-all', (req, res) => {
    stopAllServices();
    res.json({ success: true, message: 'Stopping all services' });
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down all services...');
    stopAllServices();
    setTimeout(() => {
        console.log('✅ All services stopped. Exiting...');
        process.exit(0);
    }, 2000);
});

// Start the master controller
app.listen(PORT, () => {
    console.log(`🚀 Master Service Controller Started!`);
    console.log(`📊 Control Panel: http://localhost:${PORT}`);
    console.log(`🎯 Features: Start/Stop all services from one place`);
    console.log(`⏰ Started at: ${new Date().toLocaleString()}`);
    console.log(`\n📋 Available Services:`);
    Object.entries(SERVICES).forEach(([key, service]) => {
        console.log(`   - ${service.name} (Port ${service.port})`);
    });
    console.log(`\n💡 Use the web interface at http://localhost:${PORT} to control services`);
});
