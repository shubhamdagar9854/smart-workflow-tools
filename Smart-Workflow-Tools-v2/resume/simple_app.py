import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
import sqlite3
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'smart_workflow_tools_resume_scanner_2024'

# Configuration
UPLOAD_FOLDER = 'uploads'
DB_NAME = 'resumes.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

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
            skills TEXT,
            experience TEXT,
            education TEXT,
            summary TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Extract basic info from form
            name = request.form.get('name', 'Unknown')
            email = request.form.get('email', 'unknown@example.com')
            skills = request.form.get('skills', '')
            experience = request.form.get('experience', '')
            education = request.form.get('education', '')
            summary = request.form.get('summary', '')
            
            # Save to database
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO resumes (name, email, filename, skills, experience, education, summary) VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (name, email, filename, skills, experience, education, summary))
            conn.commit()
            conn.close()
            
            flash('Resume uploaded successfully!')
            return redirect(url_for('list_resumes'))
        else:
            flash('Invalid file type. Please upload PDF, DOC, or DOCX files.')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/resumes')
def list_resumes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resumes ORDER BY uploaded_at DESC')
    resumes = cursor.fetchall()
    conn.close()
    return render_template('resumes.html', resumes=resumes)

@app.route('/resume/<int:resume_id>')
def view_resume(resume_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
    resume = cursor.fetchone()
    conn.close()
    
    if resume:
        return render_template('resume_detail.html', resume=resume)
    else:
        flash('Resume not found')
        return redirect(url_for('list_resumes'))

@app.route('/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    init_db()
    print("🚀 Resume Scanner Service Starting...")
    print("📊 Port: 5000")
    print("🔗 URL: http://localhost:5000")
    print("📁 Upload Folder:", UPLOAD_FOLDER)
    print("💾 Database:", DB_NAME)
    # Disable Flask's automatic dotenv loading to avoid Python 3.13 issues
    app.cli.load_dotenv = lambda *args, **kwargs: None
    app.run(host='0.0.0.0', port=5000, debug=True)
