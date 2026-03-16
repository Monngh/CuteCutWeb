from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1_router import router as api_v1_router

app = FastAPI(title="AutoCut Web Backend")

# Allow only the actual Vercel frontend domain in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cute-cut-web.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
