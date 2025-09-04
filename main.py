"""
AI Ruleset Generator - Flask Main Application for Render
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime

# Flask uygulaması oluştur
app = Flask(__name__)

# CORS yapılandırması
CORS(app, 
     origins=["*"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

@app.route("/", methods=['GET'])
def root():
    """Ana sayfa"""
    return jsonify({
        "message": "AI Ruleset Generator API",
        "version": "1.0.0",
        "status": "active",
        "platform": "Render",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/health", methods=['GET'])
def health_check():
    """Sağlık kontrolü"""
    return jsonify({
        "status": "healthy",
        "platform": "Render",
        "version": "1.0.0",
        "message": "All systems operational"
    })

@app.route("/project-categories", methods=['GET'])
def get_project_categories():
    """Proje kategorilerini döndür"""
    return jsonify({
        "categories": [
            {"id": "web", "name": "Web Application", "description": "Frontend and full-stack web applications"},
            {"id": "api", "name": "REST API", "description": "Backend APIs and microservices"},
            {"id": "mobile", "name": "Mobile App", "description": "iOS, Android, and cross-platform mobile apps"},
            {"id": "desktop", "name": "Desktop Application", "description": "Native desktop applications"},
            {"id": "cli", "name": "Command Line Tool", "description": "Command line interfaces and scripts"},
            {"id": "library", "name": "Library/Package", "description": "Reusable libraries and packages"},
            {"id": "microservice", "name": "Microservice", "description": "Containerized microservices"},
            {"id": "data", "name": "Data Science/ML", "description": "Data analysis and machine learning projects"}
        ]
    })

@app.route("/project-types", methods=['GET'])
def get_project_types():
    """Desteklenen proje tiplerini döndür"""
    return jsonify({
        "project_types": [
            {"value": "web", "label": "Web Application"},
            {"value": "api", "label": "REST API"},
            {"value": "mobile", "label": "Mobile App"},
            {"value": "desktop", "label": "Desktop Application"},
            {"value": "cli", "label": "Command Line Tool"},
            {"value": "library", "label": "Library/Package"},
            {"value": "microservice", "label": "Microservice"},
            {"value": "data", "label": "Data Science/ML"}
        ]
    })

@app.route("/frameworks", methods=['GET'])
def get_frameworks():
    """Language'a göre framework'leri döndür"""
    language = request.args.get('language', 'javascript')
    
    frameworks_map = {
        'javascript': ['React', 'Vue', 'Angular', 'Express', 'Next.js', 'Svelte'],
        'typescript': ['React', 'Vue', 'Angular', 'Express', 'Next.js', 'NestJS'],
        'python': ['Django', 'Flask', 'FastAPI', 'Streamlit', 'Jupyter'],
        'java': ['Spring Boot', 'Spring MVC', 'Maven', 'Gradle'],
        'csharp': ['.NET Core', 'ASP.NET', 'Blazor', 'Unity'],
        'php': ['Laravel', 'Symfony', 'CodeIgniter', 'WordPress']
    }
@app.route("/generate-ruleset", methods=['POST', 'OPTIONS'])
def generate_ruleset():
    """Ruleset oluştur"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        project_type = data.get('project_type', 'web')
        language = data.get('language', 'javascript')
        framework = data.get('framework', 'vanilla')
        description = data.get('description', '')
        
        # Generate basic ruleset
        basic_ruleset = generate_basic_ruleset(project_type, language, framework)
        
        return jsonify({
            "success": True,
            "ruleset": basic_ruleset,
            "project_info": {
                "project_type": project_type,
                "language": language,
                "framework": framework,
                "description": description
            },
            "generated_at": datetime.now().isoformat(),
            "platform": "Render"
        })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_basic_ruleset(project_type: str, language: str, framework: str) -> dict:
    """Temel ruleset şablonu oluştur"""
    tools_map = {
        'javascript': ['ESLint', 'Prettier', 'Jest', 'Webpack'],
        'typescript': ['TSLint', 'Prettier', 'Jest', 'TypeScript Compiler'],
        'python': ['Black', 'Flake8', 'pytest', 'mypy'],
        'java': ['Checkstyle', 'PMD', 'JUnit', 'Maven/Gradle'],
        'react': ['ESLint', 'Prettier', 'Jest', 'React Testing Library'],
        'vue': ['ESLint', 'Prettier', 'Vue Test Utils', 'Vite'],
        'angular': ['TSLint', 'Prettier', 'Jasmine', 'Angular CLI']
    }
    
    return {
        "project_type": project_type,
        "language": language,
        "framework": framework,
        "rules": [
            f"Use {language} best practices",
            "Implement consistent code formatting",
            "Write meaningful variable and function names",
            "Add comprehensive error handling",
            "Include unit tests for all functions",
            "Document your code with comments",
            "Follow security best practices",
            "Optimize for performance",
            "Use version control effectively",
            "Implement proper logging"
        ],
        "tools": tools_map.get(language.lower(), ['ESLint', 'Prettier', 'Jest']),
        "structure": {
            "src/": "Source code directory",
            "tests/": "Test files", 
            "docs/": "Documentation",
            "config/": "Configuration files"
        }
    }

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
