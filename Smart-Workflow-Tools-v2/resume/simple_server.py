import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
import sqlite3
from werkzeug.utils import secure_filename

# Set environment variables directly
os.environ['FLASK_ENV'] = 'development'
os.environ['PORT'] = '8080'
os.environ['GEMINI_API_KEY'] = 'AIzaSyDEhwbpB4a_5_1FJKCoNMUsJ-D5zFlvd04'

app = Flask(__name__)
app.secret_key = 'b6401568e15cca1ff8d7d6e67151797ef178c394ce72e4eaa82b944fecbe1168'

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
            summary TEXT,
            skills TEXT,
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
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Save to database
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO resumes (name, email, filename) VALUES (?, ?, ?)',
                         (request.form.get('name', 'Unknown'), 
                          request.form.get('email', 'unknown@example.com'), 
                          filename))
            conn.commit()
            conn.close()
            
            flash('Resume uploaded successfully!')
            return redirect(url_for('index'))
    
    return render_template('upload.html')

@app.route('/resumes')
def list_resumes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resumes ORDER BY uploaded_at DESC')
    resumes = cursor.fetchall()
    conn.close()
    return render_template('resumes.html', resumes=resumes)

if __name__ == '__main__':
    init_db()
    print("🚀 Resume Scanner Service Starting...")
    print("📊 Port: 8080")
    print("🔗 URL: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
