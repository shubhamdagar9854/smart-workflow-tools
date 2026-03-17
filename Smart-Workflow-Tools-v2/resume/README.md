# 🤖 Resume Scanner Service

A microservice for AI-powered resume analysis and job matching using Google Gemini AI with RAG (Retrieval-Augmented Generation). This service provides intelligent resume processing, candidate evaluation, and job matching capabilities.

## 🏗️ Microservice Architecture

### Service Overview
- **Service Name**: `resume-scanner-service`
- **Port**: 5000 (configurable)
- **Protocol**: HTTP/HTTPS
- **Format**: JSON
- **Authentication**: JWT-based (configurable)

### API Endpoints

#### Resume Processing
```
POST   /api/resumes/upload       - Upload and process resume
GET    /api/resumes/:id          - Get resume details
GET    /api/resumes              - List all resumes
DELETE /api/resumes/:id          - Delete resume
POST   /api/resumes/batch        - Batch process resumes
```

#### AI Analysis
```
POST   /api/analysis/summarize   - Generate AI summary
POST   /api/analysis/skills      - Extract skills
POST   /api/analysis/experience  - Analyze experience
POST   /api/analysis/match       - Match with job description
```

#### Job Matching
```
POST   /api/jobs/create          - Create job description
GET    /api/jobs/:id/matches     - Get matching resumes
POST   /api/jobs/:id/shortlist   - Shortlist candidates
GET    /api/jobs/:id/analytics   - Job matching analytics
```

#### RAG Learning
```
POST   /api/feedback/submit       - Submit admin feedback
GET    /api/feedback/history     - Get feedback history
POST   /api/feedback/improve     - Improve AI model
GET    /api/learning/status       - Get learning status
```

#### Admin Dashboard
```
GET    /api/admin/dashboard       - Admin dashboard data
GET    /api/admin/analytics       - System analytics
POST   /api/admin/config          - Update configuration
GET    /api/admin/logs            - System logs
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Gemini API key
- PostgreSQL (for production)
- Redis (for caching)

### Installation

```bash
# Clone the service
git clone <repository-url>
cd resume

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python database.py

# Start the service
python app.py

# For development
python app.py --debug
```

### Environment Variables

```bash
# Service Configuration
PORT=5000
ENVIRONMENT=development
DEBUG=true

# Google AI Configuration
GOOGLE_API_KEY=your-gemini-api-key
GOOGLE_MODEL=gemini-2.0-flash

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost:5432/resume_scanner
# or for SQLite
# DATABASE_URL=sqlite:///resumes.db

# Redis Configuration
REDIS_URL=redis://localhost:6379
REDIS_DB=0

# Security
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRY_HOURS=24

# File Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
ALLOWED_EXTENSIONS=pdf,docx

# RAG Configuration
RAG_ENABLED=true
VECTOR_DB_PATH=./vector_db
FEEDBACK_LEARNING_RATE=0.01

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/service.log

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 🏛️ Service Architecture

### Core Components

#### 1. **API Gateway Layer**
- Flask application with Blueprint routing
- Request validation and authentication
- Rate limiting and security middleware
- API versioning support

#### 2. **Resume Processing Service**
- File upload and validation
- PDF/DOCX parsing using pdfplumber and python-docx
- Text extraction and cleaning
- Metadata extraction

#### 3. **AI Analysis Engine**
- Google Gemini AI integration
- RAG system for continuous learning
- Skill extraction and classification
- Experience analysis and summarization

#### 4. **Job Matching Service**
- Semantic matching algorithms
- Experience level compatibility
- Skills gap analysis
- Match scoring and ranking

#### 5. **RAG Learning System**
- Feedback collection and processing
- Vector database management
- Model fine-tuning
- Performance tracking

### Database Schema

#### Resumes Table
```sql
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    file_size INTEGER NOT NULL,
    extracted_text TEXT,
    ai_summary TEXT,
    skills JSONB,
    experience JSONB,
    education JSONB,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Jobs Table
```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT,
    experience_level VARCHAR(50),
    skills_required JSONB,
    company VARCHAR(255),
    location VARCHAR(255),
    salary_range VARCHAR(100),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Matches Table
```sql
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id),
    job_id INTEGER REFERENCES jobs(id),
    match_score DECIMAL(5,2) NOT NULL,
    skills_match DECIMAL(5,2),
    experience_match DECIMAL(5,2),
    education_match DECIMAL(5,2),
    shortlisted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Feedback Table
```sql
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id),
    job_id INTEGER REFERENCES jobs(id),
    feedback_type VARCHAR(50) NOT NULL, -- correction, improvement, validation
    original_analysis JSONB,
    corrected_analysis JSONB,
    admin_notes TEXT,
    applied BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Configuration

### Service Configuration
```python
# config/settings.py
import os
from typing import Optional

class Settings:
    # Service
    PORT: int = int(os.getenv("PORT", 5000))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Google AI
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    GOOGLE_MODEL: str = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///resumes.db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-jwt-secret")
    JWT_EXPIRY_HOURS: int = int(os.getenv("JWT_EXPIRY_HOURS", 24))
    
    # File Upload
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH", 16777216))
    ALLOWED_EXTENSIONS: set = {"pdf", "docx"}
    
    # RAG
    RAG_ENABLED: bool = os.getenv("RAG_ENABLED", "true").lower() == "true"
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "./vector_db")
    FEEDBACK_LEARNING_RATE: float = float(os.getenv("FEEDBACK_LEARNING_RATE", 0.01))

settings = Settings()
```

### AI Configuration
```python
# services/ai_service.py
import google.generativeai as genai
from typing import Dict, List, Any

class AIService:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.rag_system = RAGSystem()
    
    async def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume using AI"""
        # Get relevant feedback from RAG
        relevant_feedback = await self.rag_system.get_relevant_feedback(resume_text)
        
        # Generate analysis with context
        prompt = self._build_analysis_prompt(resume_text, relevant_feedback)
        response = self.model.generate_content(prompt)
        
        return self._parse_analysis_response(response.text)
    
    async def match_job(self, resume_data: Dict, job_description: str) -> Dict[str, Any]:
        """Match resume with job description"""
        prompt = self._build_matching_prompt(resume_data, job_description)
        response = self.model.generate_content(prompt)
        
        return self._parse_matching_response(response.text)
```

## 📊 Monitoring & Logging

### Health Check Endpoint
```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "uptime": 3600,
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "redis": "connected",
    "google_ai": "authenticated",
    "vector_db": "available"
  },
  "metrics": {
    "resumes_processed": 1000,
    "jobs_created": 50,
    "matches_generated": 5000,
    "feedback_collected": 100
  }
}
```

### Metrics Endpoint
```
GET /metrics
```

Response:
```json
{
  "requests_total": 5000,
  "requests_success": 4850,
  "requests_error": 150,
  "resumes_uploaded": 1000,
  "ai_analyses": 1000,
  "job_matches": 5000,
  "average_response_time": 2500,
  "rag_improvements": 50
}
```

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads logs vector_db

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  resume-scanner-service:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/resume_scanner
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./uploads:/app/uploads
      - ./vector_db:/app/vector_db
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: resume_scanner
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - run: pip install -r requirements.txt
    - run: python -m pytest tests/
    - run: python -m flake8 src/
    - run: python -m black --check src/

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run security scan
      run: |
        pip install safety bandit
        safety check -r requirements.txt
        bandit -r app.py

  deploy:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to production
      run: |
        docker build -t resume-scanner-service .
        docker push ${{ secrets.DOCKER_REGISTRY }}/resume-scanner-service
```

## 🧪 Testing

### Unit Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/test_ai_service.py
```

### Integration Tests
```bash
# Run integration tests
python -m pytest tests/integration/

# Run API tests
python -m pytest tests/api/
```

### Load Testing
```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load_test.py --host=http://localhost:5000
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Stateless API design
- Load balancer configuration
- Database connection pooling
- Redis clustering for caching

### Performance Optimization
- AI response caching
- Vector database optimization
- Batch processing for resumes
- Asynchronous job processing

## 🔒 Security

### Authentication
- JWT token-based authentication
- API key management
- OAuth 2.0 integration
- Role-based access control

### Security Best Practices
- File upload validation
- SQL injection prevention
- XSS protection
- CORS configuration
- Rate limiting
- Audit logging

## 📝 API Documentation

### OpenAPI/Swagger
```bash
# Generate API documentation
python app.py --docs

# Access documentation
http://localhost:5000/docs
```

### Postman Collection
Import the provided Postman collection for API testing:
- `postman/resume-scanner-service.postman_collection.json`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/shubhamdagar9854/smart-workflow-tools/issues)
- **Email**: shubhamdagar9854@gmail.com
- **Documentation**: [Wiki](https://github.com/shubhamdagar9854/smart-workflow-tools/wiki)

---

**Service Version**: 1.0.0  
**Last Updated**: 2024-01-01  
**Maintainer**: Shubham Dagar
