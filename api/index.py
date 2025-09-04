from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
        "current_dir": os.getcwd()
    })

@app.route('/generate-ruleset', methods=['POST'])
def generate_ruleset():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Simple ruleset generation without AI for now
        project_type = data.get('project_type', 'web')
        language = data.get('language', 'javascript')
        description = data.get('description', '')
        
        # Basic ruleset template
        basic_ruleset = {
            "project_type": project_type,
            "language": language,
            "description": description,
            "rules": [
                "Use consistent code formatting",
                "Write meaningful variable names",
                "Add proper error handling",
                "Include unit tests",
                "Document your code"
            ],
            "tools": ["ESLint", "Prettier", "Jest"],
            "note": "This is a basic ruleset. AI generation coming soon!"
        }
        
        return jsonify({"ruleset": basic_ruleset})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel handler
if __name__ == "__main__":
    app.run()
