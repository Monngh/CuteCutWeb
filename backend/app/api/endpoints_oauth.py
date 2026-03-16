from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PublishRequest(BaseModel):
    job_id: str
    platform: str
    auth_token: str

@router.get("/{platform}/login")
def social_login(platform: str):
    """
    Redirects to the OAuth provider (TikTok or Instagram)
    """
    return {"message": f"Redirecting to {platform} OAuth Login"}

@router.get("/{platform}/callback")
def social_callback(platform: str, code: str):
    """
    Handles OAuth callback to exchange code for token
    """
    return {"token": "dummy_oauth_token"}

@router.post("/publish")
def publish_video(request: PublishRequest):
    """
    Publishes the generated video using the platform API
    """
    return {"success": True, "post_url": f"https://{request.platform}.com/dummy"}
