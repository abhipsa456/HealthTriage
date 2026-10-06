from typing import Optional


def analyze_text(
    symptoms: Optional[str],
    age: Optional[int] = None,
    gender: Optional[str] = None,
    structured_data: Optional[dict] = None
):
    """
    Analyze patient text using the MediFusion model.

    This is an AI-assisted prototype.
    It does not provide a medical diagnosis.
    """

    if not symptoms or not symptoms.strip():
        return {
            "text": "",
            "keywords": [],
            "model_used": False,
            "status": "no_input"
        }

    text = symptoms.strip()

    try:
        from backend.services.medifusion_service import predict_triage

        result = predict_triage(
            age=age,
            gender=gender,
            symptoms=text,
            structured_data=structured_data
        )

        return {
            "text": text,

            "keywords": [
                key
                for key, value
                in result["extracted_symptoms"].items()
                if value == 1
            ],

            "model_used": True,
            "status": "success",

            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "probabilities": result["probabilities"],

            "extracted_symptoms":
                result["extracted_symptoms"],

            "features_used":
                result["features_used"],

            # Transparency about missing inputs
            "missing_structured_fields":
                result["missing_structured_fields"],

            "data_sufficient":
                result["data_sufficient"],

            "model_status":
                result["model_status"]
        }

    except Exception as error:

        print(
            f"MediFusion NLP integration error: {error}"
        )

        return {
            "text": text,
            "keywords": [],
            "model_used": False,
            "status": "model_error",
            "error": str(error)
        }