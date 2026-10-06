from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.triage import router as triage_router
from backend.routes.patient import router as patient_router
from backend.routes.speech import router as speech_router
from backend.database.database import initialize_database

app = FastAPI(
    title="HealthTriage API",
    description="AI-assisted healthcare triage backend",
    version="1.0.0"
)


# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the triage routes
app.include_router(triage_router)
app.include_router(patient_router)
app.include_router(speech_router)

initialize_database()

@app.get("/")
def root():
    return {
        "message": "HealthTriage API is running",
        "status": "success"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "HealthTriage Backend"
    }