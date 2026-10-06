from pathlib import Path

import pytesseract
from PIL import Image
from pypdf import PdfReader
import fitz


# =========================================================
# CONFIGURATION
# =========================================================

SUPPORTED_REPORT_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp"
}


TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_pdf_text(file_path: Path):
    """
    Try normal machine-readable PDF text extraction.
    """

    try:

        reader = PdfReader(str(file_path))

        extracted_pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            try:

                page_text = (
                    page.extract_text() or ""
                )

            except Exception as error:

                print(
                    f"Could not extract PDF page "
                    f"{page_number}: {error}"
                )

                page_text = ""

            extracted_pages.append({
                "page": page_number,
                "text": page_text.strip()
            })

        full_text = "\n\n".join(
            page["text"]
            for page in extracted_pages
            if page["text"]
        ).strip()

        return {
            "text": full_text,
            "pages": extracted_pages,
            "page_count": len(reader.pages)
        }

    except Exception as error:

        print(
            "PDF text extraction error:",
            error
        )

        return {
            "text": "",
            "pages": [],
            "page_count": 0
        }


# =========================================================
# OCR IMAGE
# =========================================================

def extract_image_text(
    image_path: Path
):
    """
    Extract visible text from an image using Tesseract OCR.

    This is text extraction only.
    It does not interpret or diagnose medical information.
    """

    try:

        image = Image.open(
            image_path
        )

        image = image.convert("RGB")

        text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        return text.strip()

    except Exception as error:

        print(
            "Image OCR error:",
            error
        )

        return ""


# =========================================================
# OCR SCANNED PDF
# =========================================================

def extract_scanned_pdf_text(
    file_path: Path
):
    """
    Render scanned PDF pages as images and run OCR.

    PyMuPDF is used for rendering.
    Tesseract performs OCR.
    """

    extracted_pages = []

    try:

        document = fitz.open(
            str(file_path)
        )

        for page_number, page in enumerate(
            document,
            start=1
        ):

            try:

                pixmap = page.get_pixmap(
                    matrix=fitz.Matrix(
                        2,
                        2
                    )
                )

                image = Image.frombytes(
                    "RGB",
                    [
                        pixmap.width,
                        pixmap.height
                    ],
                    pixmap.samples
                )

                page_text = pytesseract.image_to_string(
                    image,
                    lang="eng"
                ).strip()

                extracted_pages.append({
                    "page": page_number,
                    "text": page_text
                })

            except Exception as error:

                print(
                    f"OCR failed for PDF page "
                    f"{page_number}: {error}"
                )

                extracted_pages.append({
                    "page": page_number,
                    "text": ""
                })

        document.close()

        full_text = "\n\n".join(
            page["text"]
            for page in extracted_pages
            if page["text"]
        ).strip()

        return {
            "text": full_text,
            "pages": extracted_pages,
            "page_count": len(extracted_pages)
        }

    except Exception as error:

        print(
            "Scanned PDF OCR error:",
            error
        )

        return {
            "text": "",
            "pages": [],
            "page_count": 0
        }


# =========================================================
# MAIN REPORT ANALYSIS
# =========================================================

def analyze_report(
    file_path: str | None,
    file_type: str | None = None
):
    """
    Extract text from uploaded reports or prescription images.

    Supported:
        - Text-based PDF
        - Scanned PDF
        - JPG
        - PNG
        - WEBP

    This service performs extraction only.

    It does NOT:
        - diagnose conditions
        - interpret laboratory results
        - recommend treatment
        - determine medication safety

    Extracted information must be verified against
    the original document by healthcare staff.
    """

    # -----------------------------------------------------
    # No file
    # -----------------------------------------------------

    if not file_path:

        return {
            "available": False,
            "status": "no_report"
        }


    path = Path(
        file_path
    )


    # -----------------------------------------------------
    # File existence
    # -----------------------------------------------------

    if not path.exists():

        return {
            "available": False,
            "status": "file_not_found"
        }


    # -----------------------------------------------------
    # File type
    # -----------------------------------------------------

    if file_type not in SUPPORTED_REPORT_TYPES:

        return {
            "available": False,
            "status": "unsupported_report_type",
            "supported_types": list(
                SUPPORTED_REPORT_TYPES
            )
        }


    # =====================================================
    # PDF
    # =====================================================

    if file_type == "application/pdf":

        # -------------------------------------------------
        # First try normal PDF text extraction
        # -------------------------------------------------

        pdf_result = extract_pdf_text(
            path
        )

        extracted_text = pdf_result["text"]


        if extracted_text:

            return {
                "available": True,
                "status": "text_extracted",
                "method": "pdf_text_extraction",
                "filename": path.name,
                "page_count": pdf_result["page_count"],
                "text": extracted_text,
                "pages": pdf_result["pages"],
                "human_verification_required": True,
                "disclaimer": (
                    "Extracted text may contain errors. "
                    "Please verify it against the original "
                    "document before using it for triage."
                )
            }


        # -------------------------------------------------
        # No machine-readable text
        # Try OCR
        # -------------------------------------------------

        ocr_result = extract_scanned_pdf_text(
            path
        )


        if ocr_result["text"]:

            return {
                "available": True,
                "status": "ocr_text_extracted",
                "method": "tesseract_ocr",
                "filename": path.name,
                "page_count": ocr_result["page_count"],
                "text": ocr_result["text"],
                "pages": ocr_result["pages"],
                "human_verification_required": True,
                "disclaimer": (
                    "OCR-extracted text may contain errors, "
                    "especially in scanned or handwritten documents. "
                    "Verify all extracted information against "
                    "the original document."
                )
            }


        # -------------------------------------------------
        # Nothing could be extracted
        # -------------------------------------------------

        return {
            "available": True,
            "status": "no_extractable_text",
            "filename": path.name,
            "page_count": pdf_result["page_count"],
            "text": "",
            "pages": [],
            "human_verification_required": True,
            "message": (
                "No machine-readable text could be extracted "
                "from this document. OCR also did not detect "
                "usable text."
            )
        }


    # =====================================================
    # IMAGE
    # =====================================================

    if file_type in {
        "image/jpeg",
        "image/png",
        "image/webp"
    }:

        extracted_text = extract_image_text(
            path
        )


        if extracted_text:

            return {
                "available": True,
                "status": "ocr_text_extracted",
                "method": "tesseract_ocr",
                "filename": path.name,
                "page_count": 1,
                "text": extracted_text,
                "pages": [
                    {
                        "page": 1,
                        "text": extracted_text
                    }
                ],
                "human_verification_required": True,
                "disclaimer": (
                    "OCR-extracted text may contain errors. "
                    "Handwritten prescriptions may be especially "
                    "difficult to recognize. Verify all extracted "
                    "information against the original document."
                )
            }


        return {
            "available": True,
            "status": "no_extractable_text",
            "filename": path.name,
            "page_count": 1,
            "text": "",
            "pages": [
                {
                    "page": 1,
                    "text": ""
                }
            ],
            "human_verification_required": True,
            "message": (
                "No readable text was detected in the image."
            )
        }


    # -----------------------------------------------------
    # Fallback
    # -----------------------------------------------------

    return {
        "available": False,
        "status": "unsupported_report_type"
    }