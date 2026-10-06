from backend.services.image_service import analyze_image
from backend.services.nlp_service import analyze_text


def analyze_multimodal(
    symptoms: str,
    age: int | None = None,
    gender: str | None = None,
    existing_conditions: str | None = None,
    voice_transcript: str | None = None,
    image_path: str | None = None,
    image_file_type: str | None = None
):
    """
    Combines available text, voice and image inputs.

    This is an AI-assisted prototype workflow.
    It does not make a medical diagnosis.
    """

    # ---------------------------------------------------------
    # 1. Combine text + voice
    # ---------------------------------------------------------

    text_parts = []

    if symptoms:
        text_parts.append(symptoms.strip())

    if voice_transcript:
        text_parts.append(
            f"Voice transcript: {voice_transcript.strip()}"
        )

    combined_text = "\n".join(text_parts).strip()

    # ---------------------------------------------------------
    # 2. NLP / MediFusion analysis
    # ---------------------------------------------------------

    nlp_result = analyze_text(
        combined_text,
        age=age,
        gender=gender
    )

    # ---------------------------------------------------------
    # 3. Image analysis
    # ---------------------------------------------------------

    image_result = analyze_image(
        file_path=image_path,
        file_type=image_file_type
    )

    # ---------------------------------------------------------
    # 4. Return multimodal result
    # ---------------------------------------------------------

    return {
        "text": {
            "available": bool(symptoms),
            "content": symptoms
        },

        "voice": {
            "available": bool(voice_transcript),
            "content": voice_transcript
        },

        "image": image_result,

        "nlp": nlp_result,

        "multimodal_status": "success",

        "human_review_required": True
    }