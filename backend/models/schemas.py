from pydantic import BaseModel, Field
from typing import Optional, List


class TriageRequest(BaseModel):

    # -----------------------------
    # Basic Patient Information
    # -----------------------------

    patient_name: Optional[str] = None

    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=120
    )

    gender: Optional[str] = None

    existing_conditions: Optional[str] = None


    # -----------------------------
    # Symptoms
    # -----------------------------

    symptoms: str = Field(
        min_length=1,
        max_length=5000
    )

    voice_transcript: Optional[str] = None


    # -----------------------------
    # Vitals
    # Enter only if measured
    # -----------------------------

    temperature: Optional[float] = Field(
        default=None,
        ge=25,
        le=45
    )

    heart_rate: Optional[float] = Field(
        default=None,
        ge=20,
        le=250
    )

    spo2: Optional[float] = Field(
        default=None,
        ge=50,
        le=100
    )

    respiratory_rate: Optional[float] = Field(
        default=None,
        ge=5,
        le=80
    )

    systolic_bp: Optional[float] = Field(
        default=None,
        ge=50,
        le=250
    )

    diastolic_bp: Optional[float] = Field(
        default=None,
        ge=20,
        le=150
    )


    # -----------------------------
    # Medical History
    # -----------------------------

    diabetes_history: Optional[str] = None

    hypertension_history: Optional[str] = None

    asthma_history: Optional[str] = None

    heart_disease_history: Optional[str] = None

    previous_hospitalization: Optional[str] = None


    # -----------------------------
    # Additional Information
    # -----------------------------

    pain_level: Optional[float] = Field(
        default=None,
        ge=0,
        le=10
    )

    symptom_duration_days: Optional[float] = Field(
        default=None,
        ge=0,
        le=3650
    )

    medication_count: Optional[int] = Field(
        default=None,
        ge=0,
        le=100
    )

    report_analysis: Optional[dict] = None


    # -----------------------------
    # Uploaded Files
    # -----------------------------

    image_filename: Optional[str] = None

    image_stored_as: Optional[str] = None

    image_file_type: Optional[str] = None

class TriageResponse(BaseModel):
    case_id: str
    triage_level: str
    confidence: float
    summary: str
    reasoning: str
    human_review_required: bool
    detected_factors: List[str] = []
    image_analysis: Optional[dict] = None
    multimodal_analysis: Optional[dict] = None