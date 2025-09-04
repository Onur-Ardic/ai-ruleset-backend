from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Create Flask application
application = Flask(__name__)

# Configure CORS with specific settings
CORS(application, 
     origins=["*"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     supports_credentials=True)

# Add CORS headers manually as well
@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@application.route('/')
def home():
    return jsonify({
        "message": "AI Ruleset Generator API is working!", 
        "status": "ok",
        "version": "1.0.0"
    })

@application.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "version": "1.0.0"
    })

@application.route('/test')
def test():
    return jsonify({
        "test": "successful",
        "environment": "vercel", 
        "python_version": sys.version,
        "current_dir": os.getcwd()
    })

@application.route('/generate-ruleset', methods=['POST', 'OPTIONS'])
def generate_ruleset():
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
        description = data.get('description', '')
        
        # Try to use AI service if available
        try:
            # Add project root to path for imports
            project_root = os.path.join(os.path.dirname(__file__), '..')
            sys.path.insert(0, project_root)
            
            from app.services.ai_service import AIService
            
            ai_service = AIService()
            result = ai_service.generate_simple_ruleset(
                project_type=project_type,
                language=language,
                description=description
            )
            
            return jsonify({"ruleset": result, "source": "AI Generated"})
            
        except Exception as ai_error:
            # Fallback to basic ruleset if AI fails
            basic_ruleset = {
                "project_type": project_type,
                "language": language,
                "description": description,
                "rules": [
                    f"Use {language} best practices",
                    "Implement consistent code formatting",
                    "Write meaningful variable and function names",
                    "Add comprehensive error handling",
                    "Include unit tests for all functions",
                    "Document your code with comments",
                    "Follow security best practices",
                    "Optimize for performance"
                ],
                "tools": _get_tools_for_language(language),
                "note": f"Basic ruleset for {project_type} project. AI service unavailable: {str(ai_error)}"
            }
            
            return jsonify({"ruleset": basic_ruleset, "source": "Fallback Template"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def _get_tools_for_language(language):
    """Get recommended tools based on programming language"""
    tools_map = {
        'javascript': ['ESLint', 'Prettier', 'Jest', 'Webpack'],
        'typescript': ['TSLint', 'Prettier', 'Jest', 'TypeScript Compiler'],
        'python': ['Black', 'Flake8', 'pytest', 'mypy'],
        'java': ['Checkstyle', 'PMD', 'JUnit', 'Maven/Gradle'],
        'react': ['ESLint', 'Prettier', 'Jest', 'React Testing Library'],
        'vue': ['ESLint', 'Prettier', 'Vue Test Utils', 'Vite'],
        'angular': ['TSLint', 'Prettier', 'Jasmine', 'Angular CLI']
    }
    return tools_map.get(language.lower(), ['ESLint', 'Prettier', 'Jest'])

# Vercel handler - export the app
app = application
handler = application

# For local development
if __name__ == "__main__":
    application.run(debug=True)
