from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from .database import engine, Base
from .vision.detector import process_video
from .reports.generator import generate_incident_report
import uuid, os, shutil

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Surveillance Intelligence Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("frames", exist_ok=True)
os.makedirs("data/videos", exist_ok=True)

results_store = {}

def run_processing(video_id: str, video_path: str):
    print(f"Starting processing for {video_id}...")
    events = process_video(video_path, video_id)
    results_store[video_id] = {
        "status": "done",
        "total_events": len(events),
        "events": events
    }
    print(f"Done! Found {len(events)} events.")

@app.get("/")
def root():
    return {"message": "Surveillance Platform API is running!"}

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}

@app.post("/api/v1/videos/upload")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    video_id = f"V{uuid.uuid4().hex[:6].upper()}"
    save_path = f"data/videos/{video_id}_{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    results_store[video_id] = {"status": "processing"}
    background_tasks.add_task(run_processing, video_id, save_path)
    return {"video_id": video_id, "filename": file.filename, "status": "processing", "message": "Video uploaded! Processing started."}

@app.get("/api/v1/videos/{video_id}/status")
def get_status(video_id: str):
    result = results_store.get(video_id)
    if not result:
        return {"error": "Video not found"}
    return result

@app.get("/api/v1/events")
def get_events():
    all_events = []
    for video_data in results_store.values():
        if "events" in video_data:
            all_events.extend(video_data["events"])
    return {"events": all_events, "total": len(all_events)}

@app.get("/api/v1/reports/incident/{video_id}")
def download_report(video_id: str):
    video_data = results_store.get(video_id)
    if not video_data or "events" not in video_data:
        return {"error": "No events found for this video"}
    path = generate_incident_report(video_data["events"], video_id)
    return FileResponse(path, filename=f"incident_{video_id}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
