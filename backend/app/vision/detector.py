import cv2
import uuid
from ultralytics import YOLO
import os

model = YOLO("yolov8n.pt")

def process_video(video_path: str, video_id: str):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frame_interval = max(1, int(fps / 5))
    events = []
    frame_index = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % frame_interval == 0:
            results = model(frame, conf=0.45, classes=[0], verbose=False)
            detections = results[0].boxes

            if detections is not None and len(detections) > 0:
                snap_path = f"frames/{video_id}_frame_{frame_index}.jpg"
                os.makedirs("frames", exist_ok=True)
                cv2.imwrite(snap_path, frame)

                event = {
                    "event_id": f"EVT_{video_id}_{frame_index}",
                    "video_id": video_id,
                    "event_type": "person_detected",
                    "severity": "L1",
                    "frame_index": frame_index,
                    "frame_snapshot_path": snap_path,
                    "person_count": len(detections),
                    "threat_score": 0.1,
                }
                events.append(event)
                print(f"Frame {frame_index}: {len(detections)} person(s) detected")

        frame_index += 1

    cap.release()
    return events