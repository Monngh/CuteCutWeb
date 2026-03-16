from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1_router import router as api_v1_router

app = FastAPI(title="AutoCut Web Backend")

# Allow only the actual Vercel frontend domain in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cute-cut-web.vercel.app", 
        "https://cute-cut-gzv4n3bfu-gaelhernandezmonroy-7379s-projects.vercel.app", 
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/debug-redis")
def debug_redis():
    import traceback
    import os
    try:
        from app.worker.celery_app import celery_app
        url = os.environ.get("REDIS_URL", "not-set")
        # Try pushing a dummy task to see exact failure
        return {
            "status": "Redis ping attempt",
            "url_configured": url,
            "broker_url": celery_app.conf.broker_url
        }
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}
