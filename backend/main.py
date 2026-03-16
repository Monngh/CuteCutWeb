from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1_router import router as api_v1_router

app = FastAPI(title="AutoCut Web Backend")

# Optional: Configuration for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tighten in production (e.g. Vercel domain)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
