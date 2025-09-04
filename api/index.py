from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os
from typing import Dict, Any
from pydantic import BaseModel

app = FastAPI(
    title="AI Ruleset Generator API",
    description="API for generating project rulesets using AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class RulesetRequest(BaseModel):
    project_type: str = "web"
    language: str = "javascript"
    description: str = ""

@app.get("/")
async def home():
    return {
        "message": "AI Ruleset Generator API is working!", 
        "status": "ok",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "version": "1.0.0"
    }

@app.get("/test")
async def test():
    return {
        "test": "successful",
        "environment": "vercel", 
        "python_version": sys.version,
        "current_dir": os.getcwd()
    }

@app.post("/generate-ruleset")
async def generate_ruleset(request_data: RulesetRequest):
    try:
        project_type = request_data.project_type
        language = request_data.language
        description = request_data.description
        
        # Try to use AI service if available
        try:
            # Add project root to path for imports
            project_root = os.path.join(os.path.dirname(__file__), '..')
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            
            from app.services.ai_service import AIService
            
            ai_service = AIService()
            result = ai_service.generate_simple_ruleset(
                project_type=project_type,
                language=language,
                description=description
            )
            
            return {"ruleset": result, "source": "AI Generated"}
            
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
            
            return {"ruleset": basic_ruleset, "source": "Fallback Template"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

# Vercel handler - Bu çok önemli!
handler = app
