# SentinelAI Architecture

## Flow
VIDEO INPUT -> Frame Extractor -> YOLOv8 Detection -> Threat Scoring -> GenAI Summary -> FastAPI -> React Dashboard

## Databases
- PostgreSQL: Events log
- MongoDB: Person cards  
- Redis: Cache

## Tech Stack
- Vision: YOLOv8 + OpenCV
- GenAI: Groq + LLaMA 3.3 70B
- Backend: FastAPI + Python 3.14
- Frontend: React + TypeScript
