import os
import shutil
import subprocess
import tempfile

import onnx_asr

from fastapi import APIRouter, UploadFile, File, HTTPException


router = APIRouter(
    prefix="/api/speech",
    tags=["Speech"]
)


MODEL_NAME = "OpenVoiceOS/ai4bharat-indicconformer-or-onnx"

_model = None


def get_odia_model():
    global _model

    if _model is None:
        print("Loading local Odia speech model...")

        _model = onnx_asr.load_model(
            MODEL_NAME
        )

        print("Odia speech model loaded successfully.")

    return _model


def find_ffmpeg():
    """
    Find FFmpeg on the system.
    """

    ffmpeg = shutil.which("ffmpeg")

    if ffmpeg:
        return ffmpeg

    possible_paths = [
        os.path.expandvars(
            r"%LOCALAPPDATA%\Microsoft\WinGet\Packages"
        )
    ]

    for base_path in possible_paths:
        if not os.path.exists(base_path):
            continue

        for root, dirs, files in os.walk(base_path):
            if "ffmpeg.exe" in files:
                return os.path.join(
                    root,
                    "ffmpeg.exe"
                )

    return None


@router.post("/transcribe")
async def transcribe_speech(
    audio: UploadFile = File(...)
):
    temp_input = None
    temp_wav = None

    try:
        if not audio:
            raise HTTPException(
                status_code=400,
                detail="No audio received."
            )

        audio_content = await audio.read()

        if not audio_content:
            raise HTTPException(
                status_code=400,
                detail="Audio file is empty."
            )

        # --------------------------------------------------
        # Save uploaded browser audio temporarily
        # --------------------------------------------------

        input_suffix = (
            os.path.splitext(
                audio.filename or ""
            )[1]
            or ".webm"
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=input_suffix
        ) as input_file:

            input_file.write(audio_content)

            temp_input = input_file.name

        # --------------------------------------------------
        # Find FFmpeg
        # --------------------------------------------------

        ffmpeg = find_ffmpeg()

        if not ffmpeg:
            raise HTTPException(
                status_code=500,
                detail="FFmpeg was not found on the system."
            )

        # --------------------------------------------------
        # Convert browser audio -> 16 kHz mono WAV
        # --------------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as wav_file:

            temp_wav = wav_file.name

        command = [
            ffmpeg,
            "-y",
            "-i",
            temp_input,
            "-ar",
            "16000",
            "-ac",
            "1",
            "-sample_fmt",
            "s16",
            temp_wav
        ]

        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode != 0:
            print(
                "FFmpeg error:",
                process.stderr
            )

            raise HTTPException(
                status_code=400,
                detail="Could not process the audio file."
            )

        # --------------------------------------------------
        # Load local Odia model
        # --------------------------------------------------

        model = get_odia_model()

        # --------------------------------------------------
        # Transcribe
        # --------------------------------------------------

        transcript = model.recognize(
            temp_wav
        )

        transcript = (
            transcript or ""
        ).strip()

        if not transcript:
            raise HTTPException(
                status_code=422,
                detail="Could not recognize speech."
            )

        return {
            "success": True,
            "language": "or-IN",
            "transcript": transcript
        }

    except HTTPException:
        raise

    except Exception as error:
        print(
            "Local Odia speech transcription error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Speech transcription failed."
        )

    finally:
        # --------------------------------------------------
        # Delete temporary audio files
        # --------------------------------------------------

        for path in [
            temp_input,
            temp_wav
        ]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as cleanup_error:
                    print(
                        "Could not remove temporary file:",
                        cleanup_error
                    )