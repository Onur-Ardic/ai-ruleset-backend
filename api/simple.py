from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Minimal FastAPI app for testing
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
    return {"test": "successful", "environment": "vercel"}

# Vercel handler
handler = app
