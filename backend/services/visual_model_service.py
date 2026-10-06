from pathlib import Path
import os

try:
    import joblib
except ImportError:
    joblib = None


# Default location for the future trained visual model
BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = BASE_DIR / "models" / "skin_wound_model.pkl"

MODEL_PATH = Path(
    os.getenv(
        "VISUAL_MODEL_PATH",
        str(DEFAULT_MODEL_PATH)
    )
)

_model = None
_model_load_attempted = False


def load_visual_model():
    """
    Load the trained visual model if it is available.

    The application continues safely when no model is present.
    """

    global _model
    global _model_load_attempted

    if _model_load_attempted:
        return _model

    _model_load_attempted = True

    if joblib is None:
        return None

    if not MODEL_PATH.exists():
        return None

    try:
        _model = joblib.load(MODEL_PATH)
        return _model

    except Exception:
        _model = None
        return None


def predict_visual(image_path: str):
    """
    Run visual prediction on an uploaded image.

    IMPORTANT:
    This function is an adapter layer. It does not claim that
    the model can diagnose a medical condition.

    The actual preprocessing and prediction logic will be added
    once the trained visual model is available.
    """

    model = load_visual_model()

    if model is None:
        return {
            "available": False,
            "status": "model_not_loaded",
            "prediction": None,
            "confidence": None,
            "human_review_required": True,
            "message": (
                "No trained visual model is currently available. "
                "Visual analysis was not performed."
            )
        }

    try:
        # The exact preprocessing required by the trained model
        # will be added after the model architecture is confirmed.
        #
        # We intentionally do NOT send a raw image directly into
        # an unknown model.

        return {
            "available": False,
            "status": "model_adapter_not_configured",
            "prediction": None,
            "confidence": None,
            "human_review_required": True,
            "message": (
                "The visual model was loaded, but its expected "
                "input preprocessing has not yet been configured."
            )
        }

    except Exception as exc:
        return {
            "available": False,
            "status": "prediction_error",
            "prediction": None,
            "confidence": None,
            "human_review_required": True,
            "error": str(exc),
            "message": (
                "Visual analysis could not be completed."
            )
        }