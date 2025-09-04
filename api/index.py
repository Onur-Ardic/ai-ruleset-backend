from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Minimal FastAPI app for Vercel
app = FastAPI(
    title="AI Ruleset Generator",
    description="AI-powered development ruleset generator",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Ruleset Generator API is working!", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/test")
async def test():
    import sys
    return {
        "test": "successful", 
        "environment": "vercel",
        "python_version": sys.version,
        "path": sys.path[:3]  # Show first 3 paths
    }

# Now try to import app modules safely
import sys
import os

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

@app.get("/modules")
async def test_modules():
    try:
        from app.core.config import settings
        from app.routers.main import router
        app.include_router(router)
        return {"status": "modules loaded successfully", "router_included": True}
    except ImportError as e:
        return {"status": "import error", "error": str(e), "path": sys.path[:5]}

# Vercel handler
handler = app
