from fastapi import APIRouter
from app.api.endpoints_video import router as video_router
from app.api.endpoints_oauth import router as oauth_router

router = APIRouter()

router.include_router(video_router, prefix="/video", tags=["video"])
router.include_router(oauth_router, prefix="/oauth", tags=["oauth"])
