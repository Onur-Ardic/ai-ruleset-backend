from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Add project root to path for imports
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

@app.route('/')
def home():
    return jsonify({
        "message": "AI Ruleset Generator API is working!", 
        "status": "ok",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "version": "1.0.0"
    })

@app.route('/test')
def test():
    return jsonify({
        "test": "successful",
        "environment": "vercel", 
        "python_version": sys.version,
        "current_dir": os.getcwd(),
        "project_root": project_root
    })

@app.route('/generate-ruleset', methods=['POST'])
def generate_ruleset():
    try:
        # Try to import AI services
        from app.services.ai_service import AIService
        from app.core.config import settings
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        # Initialize AI service
        ai_service = AIService()
        
        # Generate ruleset
        result = ai_service.generate_simple_ruleset(
            project_type=data.get('project_type', 'web'),
            language=data.get('language', 'javascript'),
            description=data.get('description', '')
        )
        
        return jsonify({"ruleset": result})
        
    except ImportError as e:
        return jsonify({
            "error": "Could not import AI services", 
            "details": str(e),
            "fallback": "Basic ruleset generation not available yet"
        }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/modules-test')
def test_modules():
    try:
        from app.core.config import settings
        return jsonify({
            "status": "Config loaded successfully",
            "ai_provider": getattr(settings, 'AI_PROVIDER', 'not found')
        })
    except ImportError as e:
        return jsonify({
            "status": "Import error",
            "error": str(e),
            "path": sys.path[:5]
        })

# Vercel handler
if __name__ == "__main__":
    app.run()
