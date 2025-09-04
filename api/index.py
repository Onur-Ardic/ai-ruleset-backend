from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os

# Proje kök dizinini path'e ekle
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

try:
    # App modüllerini import et
    from app.core.config import settings
    from app.routers.main import router
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback imports
    settings = None
    router = None

app = FastAPI(
    title="AI Ruleset Generator",
    description="AI-powered development ruleset generator",
    version="1.0.0"
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vercel için tüm originlere izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "ok", "message": "AI Ruleset Generator API is running"}

# Router'ları dahil et (eğer başarıyla import edildiyse)
if router:
    app.include_router(router)
else:
    @app.get("/fallback")
    async def fallback():
        return {"error": "Router could not be loaded"}

# Vercel için handler function
handler = app
