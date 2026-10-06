from pathlib import Path


SUPPORTED_REPORT_TYPES = {
    "application/pdf"
}


def analyze_report(
    file_path: str | None,
    file_type: str | None = None
):
    """
    Placeholder medical-report processing service.

    The actual document/NLP model can be connected later.

    This service does not interpret or diagnose medical conditions.
    """

    if not file_path:
        return {
            "available": False,
            "status": "no_report"
        }

    path = Path(file_path)

    if not path.exists():
        return {
            "available": False,
            "status": "file_not_found"
        }

    if file_type not in SUPPORTED_REPORT_TYPES:
        return {
            "available": False,
            "status": "unsupported_report_type"
        }

    return {
        "available": True,
        "status": "placeholder",
        "filename": path.name
    }