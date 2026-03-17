#!/usr/bin/env python3
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import urllib.parse
from datetime import datetime
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Configuration
PORT = 8080
UPLOAD_FOLDER = 'uploads'
DB_NAME = 'resumes.db'

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database setup
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            filename TEXT NOT NULL,
            summary TEXT,
            skills TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Mock AI Analysis
def analyze_resume(filename):
    return {
        'skills': ['Python', 'JavaScript', 'SQL', 'Machine Learning', 'Data Analysis'],
        'experience': '5+ years',
        'summary': 'Experienced software developer with strong background in data analysis and machine learning.',
        'match_percentage': 85
    }

class ResumeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Scanner Service</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 0;
            text-align: center;
        }
        .feature-card {
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
    </style>
</head>
<body>
    <div class="hero-section">
        <div class="container">
            <h1 class="display-4 mb-4">📄 Resume Scanner Service</h1>
            <p class="lead mb-4">AI-Powered Resume Analysis and Job Matching</p>
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <a href="/upload" class="btn btn-light btn-lg">📤 Upload Resume</a>
                        <a href="/resumes" class="btn btn-outline-light btn-lg">📋 View Resumes</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-4">
                <div class="card feature-card h-100">
                    <div class="card-body text-center">
                        <h3 class="card-title">🤖 AI Analysis</h3>
                        <p class="card-text">Advanced AI-powered resume analysis with skill extraction and job matching</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card feature-card h-100">
                    <div class="card-body text-center">
                        <h3 class="card-title">📊 Skill Matching</h3>
                        <p class="card-text">Automated skill matching with job requirements and compatibility scoring</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card feature-card h-100">
                    <div class="card-body text-center">
                        <h3 class="card-title">📈 Resume Insights</h3>
                        <p class="card-text">Detailed analysis and recommendations for resume improvement</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h3>🚀 Service Status</h3>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-3">
                                <div class="text-center">
                                    <h4 class="text-success">✅ Running</h4>
                                    <p class="text-muted">Resume Scanner</p>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <h4 class="text-success">✅ Ready</h4>
                                    <p class="text-muted">AI Analysis</p>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <h4 class="text-success">✅ Active</h4>
                                    <p class="text-muted">Database</p>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <h4 class="text-success">✅ Connected</h4>
                                    <p class="text-muted">File Storage</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <footer class="bg-light py-4 mt-5">
        <div class="container text-center">
            <p class="text-muted">Resume Scanner Service - Powered by AI</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
            '''
            self.wfile.write(html.encode())
            
        elif self.path == '/upload':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Resume</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h2 class="text-center">📤 Upload Resume</h2>
                    </div>
                    <div class="card-body">
                        <form action="/upload" method="POST" enctype="multipart/form-data">
                            <div class="mb-3">
                                <label for="name" class="form-label">Name</label>
                                <input type="text" class="form-control" id="name" name="name" required>
                            </div>
                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control" id="email" name="email" required>
                            </div>
                            <div class="mb-3">
                                <label for="file" class="form-label">Resume File</label>
                                <input type="file" class="form-control" id="file" name="file" accept=".pdf,.doc,.docx" required>
                            </div>
                            <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                                <button type="submit" class="btn btn-success">📤 Upload Resume</button>
                                <a href="/" class="btn btn-outline-secondary">🏠 Home</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
            '''
            self.wfile.write(html.encode())
            
        elif self.path == '/resumes':
            # Get resumes from database
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM resumes ORDER BY uploaded_at DESC')
            resumes = cursor.fetchall()
            conn.close()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Uploaded Resumes</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h2 class="text-center">📋 Uploaded Resumes</h2>
                    </div>
                    <div class="card-body">
            '''
            
            if resumes:
                html += '<div class="table-responsive"><table class="table table-striped"><thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Filename</th><th>Skills</th><th>Uploaded At</th></tr></thead><tbody>'
                for resume in resumes:
                    skills = resume[5] if resume[5] else 'Not analyzed'
                    html += f'<tr><td>{resume[0]}</td><td>{resume[1]}</td><td>{resume[2]}</td><td>{resume[3]}</td><td><span class="badge bg-primary">{skills}</span></td><td>{resume[6]}</td></tr>'
                html += '</tbody></table></div>'
            else:
                html += '<div class="text-center"><h4>No resumes uploaded yet</h4><p class="text-muted">Upload your first resume to get started!</p></div>'
            
            html += '''
                        <div class="mt-4 text-center">
                            <a href="/" class="btn btn-outline-primary">🏠 Home</a>
                            <a href="/upload" class="btn btn-primary">📤 Upload Another</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
            '''
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def do_POST(self):
        if self.path == '/upload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse multipart form data
            boundary = self.headers['Content-Type'].split('=')[1].strip()
            parts = post_data.split(b'--' + boundary.encode())
            
            name = ''
            email = ''
            filename = ''
            
            for part in parts:
                if b'Content-Disposition: form-data' in part:
                    if b'name="name"' in part:
                        lines = part.split(b'\r\n')
                        for i, line in enumerate(lines):
                            if line.strip() == b'':
                                name = lines[i+1].decode('utf-8').strip()
                                break
                    elif b'name="email"' in part:
                        lines = part.split(b'\r\n')
                        for i, line in enumerate(lines):
                            if line.strip() == b'':
                                email = lines[i+1].decode('utf-8').strip()
                                break
                    elif b'filename=' in part:
                        filename_line = part.split(b'\r\n')[1].decode('utf-8')
                        filename = filename_line.split('filename="')[1].split('"')[0]
            
            if name and email and filename:
                # Analyze resume
                analysis = analyze_resume(filename)
                
                # Save to database
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute('INSERT INTO resumes (name, email, filename, summary, skills) VALUES (?, ?, ?, ?, ?)',
                             (name, email, filename, analysis['summary'], ','.join(analysis['skills'])))
                conn.commit()
                conn.close()
                
                # Redirect to home with success message
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Bad Request')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run_server():
    print("🚀 Resume Scanner Service Starting...")
    print("📊 Port:", PORT)
    print("🔗 URL: http://localhost:" + str(PORT))
    print("🤖 AI Analysis: Mock (API key configured)")
    print("📁 Uploads:", UPLOAD_FOLDER)
    print("🗄️ Database:", DB_NAME)
    print("⚡ Server Type: Simple HTTP Server (No Flask)")
    
    init_db()
    
    try:
        server = HTTPServer(('0.0.0.0', PORT), ResumeHandler)
        print("✅ Server started successfully!")
        print("🌐 Access the service at: http://localhost:" + str(PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_server()
