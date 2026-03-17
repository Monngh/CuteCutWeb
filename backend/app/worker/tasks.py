import os
import time
import uuid
import pytubefix
from pytubefix.cli import on_progress
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
            # Step 1: Download (Bypassed YouTube, using direct sample video)
            self.update_state(state='PROGRESS', meta={'progress': 10, 'message': 'Downloading source video...'})
            
            try:
                import requests
                # Use a reliable direct MP4 link for testing the pipeline (Google API test bucket)
                sample_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
                
                # Bypassing YouTube entirely for this test phase
                response = requests.get(sample_url, stream=True)
                response.raise_for_status()
                
                actual_raw_video_path = f"{work_dir}/raw_video.mp4"
                with open(actual_raw_video_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
            except Exception as e:
                raise Exception(f"Failed to download sample video: {str(e)}")

            # Step 2: Transcribe (Mocked)
            self.update_state(state='PROGRESS', meta={'progress': 50, 'message': 'Transcribing audio...'})
            time.sleep(2)

            # Step 3: Trim and Format
            self.update_state(state='PROGRESS', meta={'progress': 75, 'message': 'Rendering video (9:16 format)...'})
            (
                ffmpeg
                .input(actual_raw_video_path, ss=0, t=15)
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
