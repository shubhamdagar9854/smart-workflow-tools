import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
import sqlite3
from werkzeug.utils import secure_filename
import warnings

# Suppress all warnings
warnings.filterwarnings('ignore')

# Set environment variables directly (no dotenv)
os.environ['FLASK_ENV'] = 'development'
os.environ['PORT'] = '8080'
os.environ['GEMINI_API_KEY'] = 'AIzaSyDEhwbpB4a_5_1FJKCoNMUsJ-D5zFlvd04'
os.environ['SECRET_KEY'] = 'b6401568e15cca1ff8d7d6e67151797ef178c394ce72e4eaa82b944fecbe1168'

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

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

# Mock AI Analysis Function
def analyze_resume(filename):
    """Mock resume analysis"""
    return {
        'skills': ['Python', 'JavaScript', 'SQL', 'Machine Learning', 'Data Analysis'],
        'experience': '5+ years',
        'summary': 'Experienced software developer with strong background in data analysis and machine learning.',
        'match_percentage': 85
    }

# Routes
@app.route('/')
def index():
    return render_template('simple_index.html')

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
            
            # Analyze resume
            analysis = analyze_resume(filename)
            
            # Save to database
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO resumes (name, email, filename, summary, skills) VALUES (?, ?, ?, ?, ?)',
                         (request.form.get('name', 'Unknown'), 
                          request.form.get('email', 'unknown@example.com'), 
                          filename,
                          analysis['summary'],
                          ','.join(analysis['skills'])))
            conn.commit()
            conn.close()
            
            flash(f'Resume uploaded successfully! Match Score: {analysis["match_percentage"]}%')
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

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for resume analysis"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save temporarily
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Analyze
    analysis = analyze_resume(filename)
    
    return jsonify({
        'success': True,
        'analysis': analysis
    })

if __name__ == '__main__':
    print("🚀 Resume Scanner Service Starting...")
    print("📊 Port:", os.environ.get('PORT', 8080))
    print("🔗 URL: http://localhost:" + os.environ.get('PORT', '8080'))
    print("🤖 AI Analysis: Mock (API key configured)")
    print("📁 Uploads:", UPLOAD_FOLDER)
    print("🗄️ Database:", DB_NAME)
    
    init_db()
    
    try:
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
