const express = require('express');
const path = require('path');
const axios = require('axios');
const app = express();
const PORT = 3010;

// Middleware
app.use(express.static('public'));
app.use(express.json());

// Service Configuration
const SERVICES = {
    login: {
        url: 'https://localhost:3000',
        name: 'Login Service',
        icon: 'fa-lock',
        description: 'Authentication & Dashboard',
        status: 'active'
    },
    resume: {
        url: 'http://localhost:5000',
        name: 'Resume Scanner',
        icon: 'fa-file-alt',
        description: 'AI-powered resume analysis',
        status: 'active'
    },
    email: {
        url: 'http://localhost:3001',
        name: 'Email Marketing',
        icon: 'fa-envelope',
        description: 'Campaign management',
        status: 'active'
    },
    gmail: {
        url: 'http://localhost:8000',
        name: 'Gmail Automation',
        icon: 'fa-google',
        description: 'Email synchronization',
        status: 'active'
    },
    devtools: {
        url: 'http://localhost:4000',
        name: 'Developer Tools',
        icon: 'fa-code',
        description: 'Development utilities',
        status: 'active'
    }
};

// Service Health Check
async function checkServiceHealth(service) {
    try {
        const response = await axios.get(service.url, { timeout: 3000 });
        return {
            ...service,
            status: 'active',
            responseTime: response.headers['x-response-time'] || 'N/A'
        };
    } catch (error) {
        return {
            ...service,
            status: 'inactive',
            error: error.message
        };
    }
}

// Routes
app.get('/', async (req, res) => {
    try {
        // Check health of all services
        const servicePromises = Object.values(SERVICES).map(service => 
            checkServiceHealth(service)
        );
        const serviceStatuses = await Promise.all(servicePromises);
        
        res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Workflow Tools - Unified Dashboard</title>
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
            padding: 25px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
        }
        .service-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        .service-icon {
            font-size: 3rem;
            margin-bottom: 15px;
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
        .status-active {
            background: #10b981;
            color: white;
        }
        .status-inactive {
            background: #ef4444;
            color: white;
        }
        .launch-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            transition: all 0.3s ease;
        }
        .launch-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        .stats-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .refresh-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(45deg, #10b981, #059669);
            border: none;
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            font-size: 1.5rem;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .refresh-btn:hover {
            transform: scale(1.1);
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
                    <p class="text-white-50 mb-0">Unified Service Dashboard</p>
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
        <!-- Statistics Section -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="stats-card text-center text-white">
                    <h3 class="mb-1">${serviceStatuses.filter(s => s.status === 'active').length}</h3>
                    <p class="mb-0">Active Services</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card text-center text-white">
                    <h3 class="mb-1">${serviceStatuses.filter(s => s.status === 'inactive').length}</h3>
                    <p class="mb-0">Inactive Services</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card text-center text-white">
                    <h3 class="mb-1">${Object.keys(SERVICES).length}</h3>
                    <p class="mb-0">Total Services</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card text-center text-white">
                    <h3 class="mb-1">99.9%</h3>
                    <p class="mb-0">Uptime</p>
                </div>
            </div>
        </div>

        <!-- Services Grid -->
        <div class="row">
            ${serviceStatuses.map(service => `
                <div class="col-md-6 col-lg-4">
                    <div class="service-card">
                        <div class="status-badge status-${service.status}">
                            ${service.status === 'active' ? 'ACTIVE' : 'INACTIVE'}
                        </div>
                        <div class="text-center">
                            <div class="service-icon">
                                <i class="fas ${service.icon}"></i>
                            </div>
                            <h4>${service.name}</h4>
                            <p class="text-muted">${service.description}</p>
                            <div class="mb-3">
                                <small class="text-muted">
                                    <i class="fas fa-server me-1"></i>
                                    ${service.url}
                                </small>
                            </div>
                            ${service.status === 'active' ? `
                                <button class="btn launch-btn" onclick="launchService('${service.url}')">
                                    <i class="fas fa-external-link-alt me-2"></i>
                                    Launch Service
                                </button>
                            ` : `
                                <button class="btn btn-secondary" disabled>
                                    <i class="fas fa-exclamation-triangle me-2"></i>
                                    Service Unavailable
                                </button>
                            `}
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    </div>

    <!-- Refresh Button -->
    <button class="refresh-btn" onclick="location.reload()" title="Refresh Status">
        <i class="fas fa-sync-alt"></i>
    </button>

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

        // Launch service
        function launchService(url) {
            window.open(url, '_blank');
        }

        // Auto-refresh every 30 seconds
        setInterval(() => {
            location.reload();
        }, 30000);
    </script>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        `);
    } catch (error) {
        res.status(500).send('Error loading dashboard');
    }
});

// API endpoint for service status
app.get('/api/services', async (req, res) => {
    try {
        const servicePromises = Object.values(SERVICES).map(service => 
            checkServiceHealth(service)
        );
        const serviceStatuses = await Promise.all(servicePromises);
        res.json(serviceStatuses);
    } catch (error) {
        res.status(500).json({ error: 'Error checking service status' });
    }
});

// Service proxy endpoints
Object.keys(SERVICES).forEach(serviceKey => {
    const service = SERVICES[serviceKey];
    app.all(`/proxy/${serviceKey}/*`, async (req, res) => {
        try {
            const targetUrl = service.url + req.path.replace(`/proxy/${serviceKey}`, '');
            const response = await axios({
                method: req.method,
                url: targetUrl,
                data: req.body,
                headers: req.headers,
                timeout: 10000
            });
            res.send(response.data);
        } catch (error) {
            res.status(500).send('Service proxy error');
        }
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Unified Dashboard Server Started!`);
    console.log(`📊 Dashboard: http://localhost:${PORT}`);
    console.log(`🔗 Services: ${Object.keys(SERVICES).length} services connected`);
    console.log(`⏰ Started at: ${new Date().toLocaleString()}`);
});
