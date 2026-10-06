from pathlib import Path

from pypdf import PdfReader


SUPPORTED_REPORT_TYPES = {
    "application/pdf"
}


def analyze_report(
    file_path: str | None,
    file_type: str | None = None
):
    """
    Extract text from an uploaded medical PDF.

    This service performs document text extraction only.
    It does not diagnose medical conditions or interpret
    medical findings.

    Extracted information must be verified by healthcare staff.
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
            "status": "unsupported_report_type",
            "supported_types": list(
                SUPPORTED_REPORT_TYPES
            )
        }

    try:
        reader = PdfReader(str(path))

        extracted_pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):
            try:
                page_text = page.extract_text() or ""
            except Exception as error:
                page_text = ""

                print(
                    f"Could not extract page "
                    f"{page_number}: {error}"
                )

            extracted_pages.append({
                "page": page_number,
                "text": page_text.strip()
            })

        full_text = "\n\n".join(
            page["text"]
            for page in extracted_pages
            if page["text"]
        ).strip()

        if not full_text:
            return {
                "available": True,
                "status": "no_extractable_text",
                "filename": path.name,
                "page_count": len(reader.pages),
                "text": "",
                "pages": extracted_pages,
                "human_verification_required": True,
                "message": (
                    "No machine-readable text was found. "
                    "The document may be scanned or handwritten. "
                    "Image-based OCR is required for further extraction."
                )
            }

        return {
            "available": True,
            "status": "text_extracted",
            "filename": path.name,
            "page_count": len(reader.pages),
            "text": full_text,
            "pages": extracted_pages,
            "human_verification_required": True,
            "disclaimer": (
                "Extracted text may contain errors. "
                "Please verify it against the original document "
                "before using it for triage."
            )
        }

    except Exception as error:
        print(
            "Report extraction error:",
            error
        )

        return {
            "available": False,
            "status": "processing_error",
            "filename": path.name,
            "error": str(error),
            "human_verification_required": True
        }