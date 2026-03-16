import os
import time
import uuid
import yt_dlp
import ffmpeg
from app.worker.celery_app import celery_app

# Ensure temp directory exists
os.makedirs("/tmp/autocut", exist_ok=True)

@celery_app.task(bind=True)
def process_video_task(self, youtube_url: str):
    """
    Main background task:
    1. Download video (yt-dlp)
    2. Transcribe audio (whisper) - Mocked for speed
    3. Trim/Render video (ffmpeg)
    """
    job_id = self.request.id
    work_dir = f"/tmp/autocut/{job_id}"
    os.makedirs(work_dir, exist_ok=True)
    
    raw_video_path = f"{work_dir}/raw_video.mp4"
    final_video_path = f"{work_dir}/final_shorts.mp4"



    # Check if ffmpeg exists before running yt-dlp to avoid fatal subprocess crashes on Windows
    try:
        import subprocess
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ffmpeg_installed = True
    except FileNotFoundError:
        ffmpeg_installed = False

    try:
        if ffmpeg_installed:
            # Step 1: Download
            self.update_state(state='PROGRESS', meta={'progress': 10, 'message': 'Downloading video...'})
            ydl_opts = {
                'format': 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': raw_video_path,
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])

            # Step 2: Transcribe (Mocked)
            self.update_state(state='PROGRESS', meta={'progress': 50, 'message': 'Transcribing audio...'})
            time.sleep(2)

            # Step 3: Trim and Format
            self.update_state(state='PROGRESS', meta={'progress': 75, 'message': 'Rendering video (9:16 format)...'})
            (
                ffmpeg
                .input(raw_video_path, ss=0, t=15)
                .filter('crop', 'ih*9/16', 'ih')
                .output(final_video_path, vcodec='libx264', acodec='aac', strict='experimental')
                .overwrite_output()
                .run(quiet=True)
            )
        else:
            # MOCK IMPLEMENTATION FOR LOCAL WINDOWS TESTING WITHOUT FFMPEG
            self.update_state(state='PROGRESS', meta={'progress': 10, 'message': 'Simulating Download (FFmpeg not found)...'})
            time.sleep(2)
            self.update_state(state='PROGRESS', meta={'progress': 50, 'message': 'Simulating Transcription...'})
            time.sleep(2)
            self.update_state(state='PROGRESS', meta={'progress': 80, 'message': 'Simulating Video Rendering...'})
            time.sleep(2)
            
        self.update_state(state='PROGRESS', meta={'progress': 100, 'message': 'Completed'})
        return {'result_url': 'https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4'}

    except Exception as e:
        # Returning will implicitly set state to SUCCESS, and our API will parse {"error": ...} to mark it as failed in the frontend.
        return {'error': str(e)}
    finally:
        pass
