from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
from fastapi.responses import FileResponse


router = APIRouter(
    prefix="/api/patient",
    tags=["Patient"]
)


# =========================================================
# UPLOAD CONFIGURATION
# =========================================================

UPLOAD_DIR = Path("backend/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}


ALLOWED_REPORT_TYPES = {
    "application/pdf"
}


# =========================================================
# FILE UPLOAD
# =========================================================

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    # -----------------------------------------------------
    # Check filename
    # -----------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )


    # -----------------------------------------------------
    # Check file type
    # -----------------------------------------------------

    allowed_types = (
        ALLOWED_IMAGE_TYPES |
        ALLOWED_REPORT_TYPES
    )


    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Allowed files are JPG, PNG, WEBP and PDF."
            )
        )


    # -----------------------------------------------------
    # Read file
    # -----------------------------------------------------

    file_content = await file.read()


    # -----------------------------------------------------
    # Check file size
    # -----------------------------------------------------

    if len(file_content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=400,
            detail="File size must be less than 10 MB."
        )


    # -----------------------------------------------------
    # Generate safe server-side filename
    # -----------------------------------------------------

    original_extension = (
        Path(file.filename)
        .suffix
        .lower()
    )


    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".pdf"
    }


    if original_extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail="Unsupported file extension."
        )


    new_filename = (
        f"{uuid.uuid4().hex}"
        f"{original_extension}"
    )


    file_path = (
        UPLOAD_DIR /
        new_filename
    )


    # -----------------------------------------------------
    # Save file
    # -----------------------------------------------------

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(
                file_content
            )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail="Unable to save uploaded file."
        ) from error


    # -----------------------------------------------------
    # Return upload information
    # -----------------------------------------------------

    return {
        "message": "File uploaded successfully",

        "filename": file.filename,

        "stored_as": new_filename,

        "file_type": file.content_type,

        "size": len(file_content)
    }


# =========================================================
# SERVE UPLOADED FILE
# =========================================================

@router.get("/file/{filename}")
def get_uploaded_file(
    filename: str
):

    # -----------------------------------------------------
    # Prevent path traversal
    # -----------------------------------------------------

    safe_filename = Path(
        filename
    ).name


    file_path = (
        UPLOAD_DIR /
        safe_filename
    )


    # -----------------------------------------------------
    # Check file exists
    # -----------------------------------------------------

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="File not found."
        )


    # -----------------------------------------------------
    # Return file
    # -----------------------------------------------------

    return FileResponse(
        file_path
    )