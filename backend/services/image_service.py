from pathlib import Path

from PIL import Image, UnidentifiedImageError

from backend.services.visual_model_service import predict_visual

SUPPORTED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}

MIN_WIDTH = 224
MIN_HEIGHT = 224


def analyze_image(
    file_path: str | None,
    file_type: str | None = None
):
    """
    Image validation, quality analysis and visual-analysis routing.

    Current capabilities:
    - file existence validation
    - supported image-type validation
    - image integrity validation
    - resolution/quality check
    - skin/wound visual-analysis routing

    IMPORTANT:
    The current implementation does not diagnose a medical
    condition. The visual model remains a separate component.
    """

    # -----------------------------------------------------
    # No image supplied
    # -----------------------------------------------------

    if not file_path:
        return {
            "available": False,
            "status": "no_image"
        }

    # -----------------------------------------------------
    # Check file existence
    # -----------------------------------------------------

    path = Path(file_path)

    if not path.exists():
        return {
            "available": False,
            "status": "file_not_found",
            "human_review_required": True
        }

    # -----------------------------------------------------
    # Check supported file type
    # -----------------------------------------------------

    if file_type not in SUPPORTED_IMAGE_TYPES:
        return {
            "available": False,
            "status": "unsupported_image_type",
            "human_review_required": True
        }

    # -----------------------------------------------------
    # Open image
    # -----------------------------------------------------

    try:

        with Image.open(path) as image:

            width, height = image.size
            image_format = image.format

            quality_issues = []

            # -------------------------------------------------
            # Resolution check
            # -------------------------------------------------

            if width < MIN_WIDTH:
                quality_issues.append(
                    f"Image width is below {MIN_WIDTH}px."
                )

            if height < MIN_HEIGHT:
                quality_issues.append(
                    f"Image height is below {MIN_HEIGHT}px."
                )

            # -------------------------------------------------
            # Quality status
            # -------------------------------------------------

            if quality_issues:
                quality_status = "low_quality"
            else:
                quality_status = "acceptable"

            # -------------------------------------------------
            # Image category
            #
            # For the current prototype, uploaded medical
            # photographs are routed to the skin/wound
            # analysis pipeline.
            #
            # This is a ROUTING category, not a diagnosis.
            # -------------------------------------------------

            image_category = "skin_wound"

            # -------------------------------------------------
            # Visual analysis
            #
            # The actual trained visual model will be connected
            # here in the next step.
            # -------------------------------------------------

            visual_analysis = predict_visual(
                image_path=str(path)
            )

            visual_analysis["image_category"] = image_category

            if quality_status == "low_quality":
                visual_analysis["status"] = (
                "blocked_low_quality"
             )
            visual_analysis["message"] = (
        "Visual analysis was not performed because "
        "the uploaded image did not pass the basic "
        "quality requirements."
    )
            # -------------------------------------------------
            # If image quality is poor, do not allow the
            # downstream visual model to treat it as reliable.
            # -------------------------------------------------

            if quality_status == "low_quality":

                visual_analysis["status"] = (
                    "blocked_low_quality"
                )

                visual_analysis["message"] = (
                    "Visual analysis was not performed because "
                    "the uploaded image did not pass the basic "
                    "quality requirements."
                )

            # -------------------------------------------------
            # Final response
            # -------------------------------------------------

            return {
                "available": True,
                "status": "success",
                "filename": path.name,
                "width": width,
                "height": height,
                "format": image_format,
                "quality_status": quality_status,
                "quality_issues": quality_issues,
                "image_category": image_category,
                "visual_analysis": visual_analysis
            }

    # ---------------------------------------------------------
    # Invalid image
    # ---------------------------------------------------------

    except UnidentifiedImageError:

        return {
            "available": False,
            "status": "invalid_image",
            "quality_issues": [
                (
                    "The uploaded file could not be "
                    "recognized as a valid image."
                )
            ],
            "human_review_required": True
        }

    # ---------------------------------------------------------
    # Unexpected processing error
    # ---------------------------------------------------------

    except Exception as exc:

        return {
            "available": False,
            "status": "image_processing_error",
            "error": str(exc),
            "human_review_required": True
        }