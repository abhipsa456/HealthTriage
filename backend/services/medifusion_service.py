from pathlib import Path
from typing import Optional
import sys

import joblib
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "MediFusion-AI"
    / "model"
    / "structured_triage_model.pkl"
)

MEDIFUSION_SRC = (
    PROJECT_ROOT
    / "MediFusion-AI"
    / "src"
)


# ============================================================
# MODEL
# ============================================================

MODEL = None


def load_model():
    """
    Load the MediFusion structured triage model once.
    """

    global MODEL

    if MODEL is not None:
        return MODEL

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"MediFusion model not found at: {MODEL_PATH}"
        )

    try:
        MODEL = joblib.load(MODEL_PATH)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to load MediFusion model: {exc}"
        ) from exc

    return MODEL


# ============================================================
# SYMPTOM EXTRACTOR
# ============================================================


# ============================================================
# SAFE VALUE HELPERS
# ============================================================

def safe_number(value, default=0):
    """
    Convert a value to a numeric value.

    Missing or invalid values are represented as 0 only for
    model execution. Missing clinical information is tracked
    separately and is never presented as a real measurement.
    """

    if value is None:
        return default

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_binary(value, default=0):
    """
    Convert common boolean-like values to 0/1.
    """

    if value is None:
        return default

    if isinstance(value, bool):
        return int(value)

    if isinstance(value, (int, float)):
        return int(bool(value))

    value = str(value).strip().lower()

    if value in {
        "yes",
        "true",
        "1",
        "present",
        "positive"
    }:
        return 1

    if value in {
        "no",
        "false",
        "0",
        "absent",
        "negative"
    }:
        return 0

    return default

def load_symptom_extractor():
    """
    Load the symptom extractor from the MediFusion source folder.
    """

    if not MEDIFUSION_SRC.exists():
        raise FileNotFoundError(
            f"MediFusion source folder not found at: "
            f"{MEDIFUSION_SRC}"
        )

    src_path = str(MEDIFUSION_SRC)

    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    try:
        from symptom_extractor import extract_symptoms  # type: ignore
    except Exception as exc:
        raise RuntimeError(
            f"Could not import MediFusion symptom extractor: {exc}"
        ) from exc

    return extract_symptoms

# ============================================================
# MAIN MEDIFUSION PREDICTION
# ============================================================

def predict_triage(
    age: Optional[int],
    gender: Optional[str],
    symptoms: str,
    structured_data: Optional[dict] = None
):
    """
    Run the MediFusion structured triage model.

    Important:
    - This is an AI-assisted prototype integration.
    - It is NOT a medical diagnosis.
    - Missing clinical information is explicitly tracked.
    - Missing measurements are not presented as actual measurements.
    - Human review remains required for clinical use.
    """

    # --------------------------------------------------------
    # Load resources
    # --------------------------------------------------------

    model = load_model()
    extract_symptoms = load_symptom_extractor()

    structured_data = structured_data or {}

    symptoms = (symptoms or "").strip()

    # --------------------------------------------------------
    # Extract symptoms
    # --------------------------------------------------------

    try:
        extracted = extract_symptoms(symptoms)
    except Exception as exc:
        return {
            "model_used": False,
            "status": "symptom_extraction_error",
            "prediction": None,
            "confidence": None,
            "probabilities": {},
            "extracted_symptoms": {},
            "features_used": {},
            "missing_structured_fields": [],
            "data_sufficient": False,
            "model_status": "error",
            "error": str(exc),
            "human_review_required": True
        }

    # --------------------------------------------------------
    # Make sure extracted symptom keys exist
    # --------------------------------------------------------

    symptom_fields = [
        "fever",
        "cough",
        "headache",
        "vomiting",
        "diarrhea",
        "fatigue",
        "abdominal_pain",
        "dizziness",
        "chest_pain",
        "breathing_difficulty"
    ]

    for field in symptom_fields:
        extracted.setdefault(field, 0)

    # --------------------------------------------------------
    # Gender mapping
    # --------------------------------------------------------

    sex_map = {
        "male": 0,
        "female": 1,
        "other": 2,
        "prefer_not": 2,
        "prefer not": 2
    }

    gender_key = (gender or "").strip().lower()

    sex = sex_map.get(
        gender_key,
        2
    )

    # --------------------------------------------------------
    # Structured fields
    # --------------------------------------------------------

    clinical_fields = [
        "temperature",
        "heart_rate",
        "spo2",
        "respiratory_rate",
        "systolic_bp",
        "diastolic_bp"
    ]

    history_fields = [
        "diabetes_history",
        "hypertension_history",
        "asthma_history",
        "heart_disease_history",
        "previous_hospitalization"
    ]

    other_fields = [
        "pain_level",
        "symptom_duration_days",
        "medication_count"
    ]

    all_structured_fields = (
        clinical_fields
        + history_fields
        + other_fields
    )

    missing_structured_fields = [
        field
        for field in all_structured_fields
        if (
            field not in structured_data
            or structured_data[field] is None
            or structured_data[field] == ""
        )
    ]

    # --------------------------------------------------------
    # Build patient feature dictionary
    # --------------------------------------------------------

    patient = {
        "age": safe_number(
            age,
            default=0
        ),

        "sex": sex,

        # Clinical measurements
        "temperature": safe_number(
            structured_data.get("temperature")
        ),

        "heart_rate": safe_number(
            structured_data.get("heart_rate")
        ),

        "spo2": safe_number(
            structured_data.get("spo2")
        ),

        "respiratory_rate": safe_number(
            structured_data.get("respiratory_rate")
        ),

        "systolic_bp": safe_number(
            structured_data.get("systolic_bp")
        ),

        "diastolic_bp": safe_number(
            structured_data.get("diastolic_bp")
        ),

        # Symptoms
        "fever": safe_binary(
            extracted.get("fever")
        ),

        "cough": safe_binary(
            extracted.get("cough")
        ),

        "headache": safe_binary(
            extracted.get("headache")
        ),

        "vomiting": safe_binary(
            extracted.get("vomiting")
        ),

        "diarrhea": safe_binary(
            extracted.get("diarrhea")
        ),

        "fatigue": safe_binary(
            extracted.get("fatigue")
        ),

        "abdominal_pain": safe_binary(
            extracted.get("abdominal_pain")
        ),

        "dizziness": safe_binary(
            extracted.get("dizziness")
        ),

        "chest_pain": safe_binary(
            extracted.get("chest_pain")
        ),

        "breathing_difficulty": safe_binary(
            extracted.get("breathing_difficulty")
        ),

        # Medical history
        "diabetes_history": safe_binary(
            structured_data.get("diabetes_history")
        ),

        "hypertension_history": safe_binary(
            structured_data.get("hypertension_history")
        ),

        "asthma_history": safe_binary(
            structured_data.get("asthma_history")
        ),

        "heart_disease_history": safe_binary(
            structured_data.get("heart_disease_history")
        ),

        "previous_hospitalization": safe_binary(
            structured_data.get(
                "previous_hospitalization"
            )
        ),

        # Other information
        "pain_level": safe_number(
            structured_data.get("pain_level")
        ),

        "symptom_duration_days": safe_number(
            structured_data.get(
                "symptom_duration_days"
            )
        ),

        "medication_count": safe_number(
            structured_data.get(
                "medication_count"
            )
        )
    }

    # --------------------------------------------------------
    # Verify model features
    # --------------------------------------------------------

    try:
        feature_order = list(
            model.feature_names_in_
        )
    except AttributeError:
        return {
            "model_used": False,
            "status": "model_feature_names_unavailable",
            "prediction": None,
            "confidence": None,
            "probabilities": {},
            "extracted_symptoms": extracted,
            "features_used": patient,
            "missing_structured_fields":
                missing_structured_fields,
            "data_sufficient": False,
            "model_status": "invalid_model",
            "human_review_required": True,
            "error": (
                "The MediFusion model does not expose "
                "feature_names_in_."
            )
        }

    # --------------------------------------------------------
    # Check missing model features
    # --------------------------------------------------------

    missing_model_features = [
        feature
        for feature in feature_order
        if feature not in patient
    ]

    if missing_model_features:
        return {
            "model_used": False,
            "status": "feature_mismatch",
            "prediction": None,
            "confidence": None,
            "probabilities": {},
            "extracted_symptoms": extracted,
            "features_used": patient,
            "missing_structured_fields":
                missing_structured_fields,
            "missing_model_features":
                missing_model_features,
            "data_sufficient": False,
            "model_status": "feature_mismatch",
            "human_review_required": True,
            "error": (
                "The MediFusion model expects features "
                "that are not available in the integration."
            )
        }

    # --------------------------------------------------------
    # Create DataFrame in exact training order
    # --------------------------------------------------------

    patient_df = pd.DataFrame(
        [patient],
        columns=feature_order
    )

    # --------------------------------------------------------
    # Run prediction
    # --------------------------------------------------------

    try:
        prediction = model.predict(
            patient_df
        )[0]

        probabilities = model.predict_proba(
            patient_df
        )[0]

    except Exception as exc:
        return {
            "model_used": False,
            "status": "prediction_error",
            "prediction": None,
            "confidence": None,
            "probabilities": {},
            "extracted_symptoms": extracted,
            "features_used": patient,
            "missing_structured_fields":
                missing_structured_fields,
            "data_sufficient": False,
            "model_status": "prediction_error",
            "human_review_required": True,
            "error": str(exc)
        }

    # --------------------------------------------------------
    # Probability mapping
    # --------------------------------------------------------

    probability_dict = {
        str(label): float(probability)
        for label, probability in zip(
            model.classes_,
            probabilities
        )
    }

    confidence = max(
        probability_dict.values()
    )

    # --------------------------------------------------------
    # Structured-data completeness
    # --------------------------------------------------------

    data_sufficient = (
        len(missing_structured_fields) == 0
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {
        "model_used": True,

        "status": "success",

        "prediction": str(
            prediction
        ),

        "confidence": float(
            confidence
        ),

        "probabilities": probability_dict,

        "extracted_symptoms": extracted,

        "features_used": patient,

        "missing_structured_fields":
            missing_structured_fields,

        "data_sufficient":
            data_sufficient,

        "model_status": (
            "complete_structured_input"
            if data_sufficient
            else "partial_structured_input"
        ),

        # Important for healthcare prototype
        "human_review_required": True,

        "disclaimer": (
            "MediFusion provides an AI-assisted "
            "prototype signal only. It is not a "
            "medical diagnosis and requires qualified "
            "healthcare professional review."
        )
    }