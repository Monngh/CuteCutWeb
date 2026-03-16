from fastapi import APIRouter
from pydantic import BaseModel
from app.worker.tasks import process_video_task
from celery.result import AsyncResult
from app.worker.celery_app import celery_app

router = APIRouter()

class VideoRequest(BaseModel):
    youtube_url: str

class VideoResponse(BaseModel):
    job_id: str
    status: str

@router.post("/process", response_model=VideoResponse)
def process_video(request: VideoRequest):
    # Trigger Celery task asynchronously
    task = process_video_task.delay(request.youtube_url)
    return {"job_id": task.id, "status": "queued"}

@router.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    task_result = AsyncResult(job_id, app=celery_app)
    
    response = {
        "job_id": job_id,
        "status": task_result.state.lower(),
        "progress": 0,
        "message": "Initializing...",
        "result_url": None
    }

    if task_result.state == 'PENDING':
        # Job not active yet
        pass
    elif task_result.state == 'PROGRESS':
        info = task_result.info or {}
        response['progress'] = info.get('progress', 0) if isinstance(info, dict) else 0
        response['message'] = info.get('message', 'Processing...') if isinstance(info, dict) else 'Processing...'
    elif task_result.state == 'SUCCESS':
        info = task_result.info or {}
        if 'error' in info:
            response['status'] = 'failed'
            response['message'] = info['error']
        else:
            response['progress'] = 100
            response['message'] = "Completed!"
            response['result_url'] = info.get('result_url') if isinstance(info, dict) else None
    elif task_result.state == 'FAILURE':
        response['status'] = 'failed'
        response['message'] = str(task_result.info) if task_result.info else "Unknown Error"

    return response
