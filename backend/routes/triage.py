from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pathlib import Path
import json

from backend.models.schemas import TriageRequest, TriageResponse
from backend.services.triage_engine import generate_triage
from backend.services.multimodal_service import analyze_multimodal
from backend.services.medifusion_service import predict_triage
from backend.database.database import get_connection
from backend.services.security import verify_api_key
from backend.services.cloud_service import save_case_to_cloud
from backend.services.supabase_service import get_supabase


router = APIRouter(
    prefix="/api",
    tags=["Triage"]
)


# =========================================================
# UPLOAD DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "uploads"


# =========================================================
# CREATE TRIAGE CASE
# =========================================================

@router.post("/triage", response_model=TriageResponse)
def triage_patient(request: TriageRequest):

    # -----------------------------------------------------
    # Combine typed symptoms and voice transcript
    # -----------------------------------------------------

    combined_symptoms = request.symptoms.strip()

    if request.voice_transcript:
        combined_symptoms = (
            combined_symptoms
            + " "
            + request.voice_transcript.strip()
        ).strip()


    # -----------------------------------------------------
    # Build actual image path
    # -----------------------------------------------------

    image_path = None

    if request.image_stored_as:

        candidate_path = UPLOAD_DIR / Path(
            request.image_stored_as
        ).name

        if candidate_path.exists():
            image_path = str(candidate_path)


    # =====================================================
    # STRUCTURED MEDIFUSION INPUT
    # =====================================================

    structured_data = {

        # Vitals
        "temperature": request.temperature,
        "heart_rate": request.heart_rate,
        "spo2": request.spo2,
        "respiratory_rate": request.respiratory_rate,
        "systolic_bp": request.systolic_bp,
        "diastolic_bp": request.diastolic_bp,

        # Medical history
        "diabetes_history": request.diabetes_history,
        "hypertension_history": request.hypertension_history,
        "asthma_history": request.asthma_history,
        "heart_disease_history": request.heart_disease_history,
        "previous_hospitalization": request.previous_hospitalization,

        # Additional information
        "pain_level": request.pain_level,
        "symptom_duration_days": request.symptom_duration_days,
        "medication_count": request.medication_count,
    }


    # Remove fields that were not supplied
    structured_data = {
        key: value
        for key, value in structured_data.items()
        if value is not None
        and value != ""
    }


    # =====================================================
    # ANALYZE AVAILABLE MULTIMODAL INPUTS
    # =====================================================

    multimodal_result = analyze_multimodal(
        symptoms=request.symptoms,
        age=request.age,
        gender=request.gender,
        existing_conditions=request.existing_conditions,
        voice_transcript=request.voice_transcript,
        image_path=image_path,
        image_file_type=request.image_file_type
    )


    # -----------------------------------------------------
    # Extract image analysis result
    # -----------------------------------------------------

    image_analysis = multimodal_result.get(
        "image",
        {
            "available": False,
            "status": "no_image"
        }
    )


    # =====================================================
    # MEDIFUSION STRUCTURED AI ANALYSIS
    # =====================================================

    try:

        medifusion_result = predict_triage(
            age=request.age,
            gender=request.gender,
            symptoms=combined_symptoms,
            structured_data=structured_data
        )

    except Exception as exc:

        medifusion_result = {
            "model_used": False,
            "status": "model_error",
            "prediction": None,
            "confidence": None,
            "probabilities": {},
            "extracted_symptoms": {},
            "features_used": {},
            "missing_structured_fields": [],
            "data_sufficient": False,
            "model_status": "error",
            "human_review_required": True,
            "error": str(exc)
        }


    # =====================================================
    # UNIFIED MULTIMODAL SIGNALS
    # =====================================================

    multimodal_signals = {

        "text_available": bool(
            request.symptoms
        ),

        "voice_available": bool(
            request.voice_transcript
        ),

        "image_available": bool(
            image_analysis.get("available")
        ),

        "image_quality": image_analysis.get(
            "quality_status"
        ),

        "medifusion_available": medifusion_result.get(
            "model_used",
            False
        ),

        "medifusion_prediction": medifusion_result.get(
            "prediction"
        ),

        "medifusion_confidence": medifusion_result.get(
            "confidence"
        ),

        "structured_data_supplied": bool(
            structured_data
        ),

        "structured_data_sufficient": medifusion_result.get(
            "data_sufficient",
            False
        )
    }


    # =====================================================
    # HUMAN REVIEW SAFETY GATE
    # =====================================================

    multimodal_human_review_required = True

    if medifusion_result.get(
        "missing_structured_fields"
    ):
        multimodal_human_review_required = True

    if medifusion_result.get(
        "status"
    ) != "success":
        multimodal_human_review_required = True

    if image_analysis.get("available"):

        visual_analysis = image_analysis.get(
            "visual_analysis",
            {}
        )

        if visual_analysis.get(
            "human_review_required",
            True
        ):
            multimodal_human_review_required = True


    # =====================================================
    # UNIFIED MULTIMODAL ASSESSMENT
    # =====================================================

    unified_analysis = {

        "text": {
            "available": bool(
                request.symptoms
            ),
            "source": "patient_symptoms"
        },

        "voice": {
            "available": bool(
                request.voice_transcript
            ),
            "source": "voice_transcript"
        },

        "image": {
            "available": bool(
                image_analysis.get("available")
            ),

            "quality_status": image_analysis.get(
                "quality_status"
            ),

            "visual_analysis": image_analysis.get(
                "visual_analysis"
            )
        },

        "structured_inputs": {
            "available": bool(
                structured_data
            ),
            "data": structured_data
        },

        "medifusion": {

            "available": medifusion_result.get(
                "model_used",
                False
            ),

            "status": medifusion_result.get(
                "status"
            ),

            "prediction": medifusion_result.get(
                "prediction"
            ),

            "confidence": medifusion_result.get(
                "confidence"
            ),

            "probabilities": medifusion_result.get(
                "probabilities",
                {}
            ),

            "extracted_symptoms": medifusion_result.get(
                "extracted_symptoms",
                {}
            ),

            "features_used": medifusion_result.get(
                "features_used",
                {}
            ),

            "data_sufficient": medifusion_result.get(
                "data_sufficient",
                False
            ),

            "missing_fields": medifusion_result.get(
                "missing_structured_fields",
                []
            ),

            "model_status": medifusion_result.get(
                "model_status"
            )
        },

        "signals": multimodal_signals,

        "human_review_required": (
            multimodal_human_review_required
        ),

        "disclaimer": (
            "This is an AI-assisted triage prototype "
            "and not a medical diagnosis. Final decisions "
            "require appropriate healthcare professional "
            "review."
        )
    }


    # =====================================================
    # PRIMARY TRIAGE ENGINE
    # =====================================================

    result = generate_triage(
        combined_symptoms
    )


    # =====================================================
    # INITIAL RESULT STATE
    # =====================================================

    reasoning = result.get(
        "reasoning",
        ""
    )

    human_review_required = result.get(
        "human_review_required",
        False
    )

    detected_factors = list(
        result.get(
            "detected_factors",
            []
        )
    )


    # =====================================================
    # ADD MEDIFUSION INFORMATION
    # =====================================================

    if medifusion_result.get(
        "model_used"
    ):

        prediction = medifusion_result.get(
            "prediction"
        )

        confidence = medifusion_result.get(
            "confidence"
        )

        data_sufficient = medifusion_result.get(
            "data_sufficient",
            False
        )

        missing_fields = medifusion_result.get(
            "missing_structured_fields",
            []
        )


        # -------------------------------------------------
        # Add secondary AI signal
        # -------------------------------------------------

        if confidence is not None:

            detected_factors.append(
                f"MediFusion AI prediction: "
                f"{prediction} "
                f"({confidence:.2f} confidence)"
            )

        else:

            detected_factors.append(
                f"MediFusion AI prediction: "
                f"{prediction}"
            )


        # -------------------------------------------------
        # Explain structured input status
        # -------------------------------------------------

        if data_sufficient:

            reasoning += (
                " MediFusion AI analysis was performed "
                "using the available structured clinical "
                "inputs. This is an AI-assisted secondary "
                "signal and requires human review; it is "
                "not a medical diagnosis."
            )

        else:

            reasoning += (
                " MediFusion AI analysis was performed, "
                "but some structured clinical information "
                "was not provided. Missing fields include: "
                f"{', '.join(missing_fields)}. "
                "Therefore, the MediFusion output should "
                "be treated only as a partial AI-assisted "
                "signal and requires human review. It is "
                "not a medical diagnosis."
            )


        # MediFusion always requires human review
        human_review_required = True

    else:

        status = medifusion_result.get(
            "status"
        )

        if status == "model_error":

            detected_factors.append(
                "MediFusion analysis unavailable"
            )

            reasoning += (
                " The additional MediFusion AI analysis "
                "was unavailable, so human review is required."
            )

        elif status != "success":

            detected_factors.append(
                "MediFusion structured analysis was incomplete"
            )

            reasoning += (
                " The MediFusion structured AI analysis "
                "could not provide a complete result. "
                "Human review is required."
            )

        human_review_required = True


    # =====================================================
    # ANALYZE UPLOADED IMAGE QUALITY
    # =====================================================

    if image_analysis.get(
        "available"
    ):

        quality_status = image_analysis.get(
            "quality_status"
        )

        if quality_status == "acceptable":

            detected_factors.append(
                "Uploaded image passed basic quality checks"
            )

        elif quality_status == "low_quality":

            detected_factors.append(
                "Uploaded image may be low quality "
                "and requires human review"
            )

            human_review_required = True

        elif quality_status:

            detected_factors.append(
                f"Image quality status: "
                f"{quality_status}"
            )

            human_review_required = True


    # =====================================================
    # HANDLE VISUAL MODEL RESULT
    # =====================================================

    if image_analysis.get(
        "available"
    ):

        visual_analysis = image_analysis.get(
            "visual_analysis",
            {}
        )

        visual_status = visual_analysis.get(
            "status"
        )


        if visual_status == "model_not_loaded":

            detected_factors.append(
                "Visual model is not currently loaded"
            )

            reasoning += (
                " The uploaded image passed the basic "
                "technical quality checks, but no trained "
                "visual model is currently available. "
                "Therefore, visual interpretation was not "
                "performed and human review is required."
            )

            human_review_required = True


        elif visual_status == "model_adapter_not_configured":

            detected_factors.append(
                "Visual model adapter requires configuration"
            )

            reasoning += (
                " The uploaded image passed the basic "
                "technical quality checks, but the visual "
                "model input configuration is incomplete. "
                "Human review is required."
            )

            human_review_required = True


        elif visual_status == "blocked_low_quality":

            detected_factors.append(
                "Visual analysis blocked because of "
                "low image quality"
            )

            human_review_required = True


        elif visual_status == "prediction_error":

            detected_factors.append(
                "Visual analysis could not be completed"
            )

            reasoning += (
                " Visual analysis could not be completed. "
                "Human review is required."
            )

            human_review_required = True


    # =====================================================
    # ADD IMAGE INFORMATION TO REASONING
    # =====================================================

    if image_analysis.get(
        "available"
    ):

        if image_analysis.get(
            "quality_status"
        ) == "acceptable":

            reasoning += (
                " The uploaded image passed the basic "
                "technical quality checks. This does not "
                "indicate or rule out any medical condition."
            )

        elif image_analysis.get(
            "quality_status"
        ) == "low_quality":

            reasoning += (
                " The uploaded image may have insufficient "
                "technical quality for reliable downstream "
                "analysis. Human review is required."
            )

            human_review_required = True


    # =====================================================
    # FINAL HUMAN REVIEW DECISION
    # =====================================================

    human_review_required = (
        human_review_required
        or multimodal_human_review_required
    )


    # =====================================================
    # UPDATE FINAL RESULT
    # =====================================================

    result["reasoning"] = reasoning

    result["human_review_required"] = (
        human_review_required
    )

    result["detected_factors"] = (
        detected_factors
    )

    result["image_analysis"] = (
        image_analysis
    )

    result["multimodal_analysis"] = (
        unified_analysis
    )


    # =====================================================
    # SAVE CASE TO LOCAL SQLITE
    # =====================================================

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO cases (
            case_id,
            patient_name,
            age,
            gender,
            existing_conditions,
            symptoms,
            voice_transcript,
            image_filename,
            image_stored_as,
            image_file_type,
            report_analysis,
            triage_level,
            confidence,
            summary,
            reasoning,
            human_review_required,
            detected_factors,
            status
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            result["case_id"],
            request.patient_name,
            request.age,
            request.gender,
            request.existing_conditions,
            request.symptoms,
            request.voice_transcript,
            request.image_filename,
            request.image_stored_as,
            request.image_file_type,

            (
                json.dumps(
                    request.report_analysis
                )
                if request.report_analysis
                else None
            ),

            result["triage_level"],
            result["confidence"],
            result["summary"],
            result["reasoning"],

            int(
                result["human_review_required"]
            ),

            json.dumps(
                result["detected_factors"]
            ),

            "WAITING"
        )
    )

    connection.commit()
    connection.close()


    # =====================================================
    # SAVE CASE TO CLOUD
    # =====================================================

    cloud_case = {

        "case_id": result["case_id"],

        "patient_name": request.patient_name,
        "age": request.age,
        "gender": request.gender,
        "existing_conditions": request.existing_conditions,

        "symptoms": request.symptoms,
        "voice_transcript": request.voice_transcript,

        "triage_level": result["triage_level"],
        "confidence": result["confidence"],

        "summary": result["summary"],
        "reasoning": result["reasoning"],

        "human_review_required": bool(
            result["human_review_required"]
        ),

        "final_decision": None,
        "status": "WAITING",

        "image_filename": request.image_filename,
        "image_stored_as": request.image_stored_as,
        "image_file_type": request.image_file_type,

        "report_analysis": request.report_analysis,

        "detected_factors": result[
            "detected_factors"
        ]
    }


    cloud_result = save_case_to_cloud(
        cloud_case
    )


    if cloud_result:

        print(
            f"[Cloud Sync] Case "
            f"{result['case_id']} "
            "saved successfully."
        )

    else:

        print(
            f"[Cloud Sync] Case "
            f"{result['case_id']} "
            "could not be saved to cloud."
        )


    # =====================================================
    # RETURN TRIAGE RESULT
    # =====================================================

    return result

@router.get("/debug/supabase")
def debug_supabase():
    import os

    return {
        "supabase_url_configured": bool(os.getenv("SUPABASE_URL")),
        "supabase_service_key_configured": bool(
            os.getenv("SUPABASE_SERVICE_KEY")
        )
    }

# =========================================================
# GET ALL CASES
# =========================================================

@router.get("/cases")
def get_cases():

    """
    Return triage cases for the healthcare staff dashboard.

    Cloud-first:
    1. Try Supabase
    2. Fall back to local SQLite if cloud retrieval fails.

    This endpoint is read-only.
    """

    # =====================================================
    # TRY CLOUD FIRST
    # =====================================================

    try:

        supabase = get_supabase()

        response = (
            supabase
            .table("cases")
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        if response.data is not None:

            return response.data


    except Exception as error:

        print(
            "[Cloud Cases] "
            f"Failed to retrieve cloud cases: {error}"
        )


    # =====================================================
    # FALL BACK TO LOCAL SQLITE
    # =====================================================

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM cases
            ORDER BY
                CASE
                    WHEN COALESCE(
                        final_decision,
                        triage_level
                    ) = 'red'
                        THEN 1

                    WHEN COALESCE(
                        final_decision,
                        triage_level
                    ) = 'yellow'
                        THEN 2

                    WHEN COALESCE(
                        final_decision,
                        triage_level
                    ) = 'green'
                        THEN 3

                    ELSE 4
                END,

                created_at DESC
            """
        )

        cases = cursor.fetchall()

        connection.close()

        return [
            dict(case)
            for case in cases
        ]


    except Exception as error:

        print(
            "[Local Cases] "
            f"Failed to retrieve cases: {error}"
        )

        return []


# =========================================================
# GET SINGLE CASE
# =========================================================

@router.get("/cases/{case_id}")
def get_case(
    case_id: str,
    authorized: bool = Depends(verify_api_key)
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM cases
        WHERE case_id = ?
        """,
        (case_id,)
    )

    case = cursor.fetchone()

    connection.close()


    # -----------------------------------------------------
    # Case not found
    # -----------------------------------------------------

    if case is None:

        return {
            "error": "Case not found"
        }


    # -----------------------------------------------------
    # Convert database row to dictionary
    # -----------------------------------------------------

    case_data = dict(case)


    # -----------------------------------------------------
    # Convert detected factors from JSON to list
    # -----------------------------------------------------

    try:

        case_data["detected_factors"] = json.loads(
            case_data.get(
                "detected_factors"
            ) or "[]"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):

        case_data["detected_factors"] = []


    # -----------------------------------------------------
    # Convert report analysis from JSON to object
    # -----------------------------------------------------

    try:

        case_data["report_analysis"] = json.loads(
            case_data.get(
                "report_analysis"
            ) or "null"
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):

        case_data["report_analysis"] = None


    # -----------------------------------------------------
    # Re-run MediFusion for Case Details
    # -----------------------------------------------------

    try:

        medifusion_result = predict_triage(

            age=case_data.get(
                "age"
            ),

            gender=case_data.get(
                "gender"
            ),

            symptoms=case_data.get(
                "symptoms",
                ""
            ),

            structured_data={}
        )


        case_data["multimodal_analysis"] = {

            "medifusion": {

                "available":
                    medifusion_result.get(
                        "model_used",
                        False
                    ),

                "status":
                    medifusion_result.get(
                        "status"
                    ),

                "prediction":
                    medifusion_result.get(
                        "prediction"
                    ),

                "confidence":
                    medifusion_result.get(
                        "confidence"
                    ),

                "probabilities":
                    medifusion_result.get(
                        "probabilities",
                        {}
                    ),

                "extracted_symptoms":
                    medifusion_result.get(
                        "extracted_symptoms",
                        {}
                    ),

                "features_used":
                    medifusion_result.get(
                        "features_used",
                        {}
                    ),

                "data_sufficient":
                    medifusion_result.get(
                        "data_sufficient",
                        False
                    ),

                "missing_fields":
                    medifusion_result.get(
                        "missing_structured_fields",
                        []
                    ),

                "model_status":
                    medifusion_result.get(
                        "model_status"
                    )
            },


            "signals": {

                "medifusion_available":
                    medifusion_result.get(
                        "model_used",
                        False
                    ),

                "medifusion_prediction":
                    medifusion_result.get(
                        "prediction"
                    ),

                "medifusion_confidence":
                    medifusion_result.get(
                        "confidence"
                    )
            },


            "human_review_required": True,

            "disclaimer": (
                "This is an AI-assisted triage prototype "
                "and not a medical diagnosis. Final decisions "
                "require appropriate healthcare professional "
                "review."
            )
        }


    except Exception as error:

        print(
            "MediFusion case-detail analysis error:",
            error
        )


        case_data["multimodal_analysis"] = {

            "medifusion": {

                "available": False,

                "status": "model_error",

                "prediction": None,

                "confidence": None,

                "probabilities": {},

                "extracted_symptoms": {},

                "features_used": {},

                "data_sufficient": False,

                "missing_fields": [],

                "model_status": "error"
            },


            "signals": {

                "medifusion_available": False,

                "medifusion_prediction": None,

                "medifusion_confidence": None
            },


            "human_review_required": True,

            "disclaimer": (
                "This is an AI-assisted triage prototype "
                "and not a medical diagnosis. Final decisions "
                "require appropriate healthcare professional "
                "review."
            )
        }


    return case_data


# =========================================================
# FINALIZE / MANUAL CLINICAL DECISION
# =========================================================

class FinalizeRequest(BaseModel):

    final_decision: str


@router.put("/cases/{case_id}/finalize")
def finalize_case(
    case_id: str,
    request: FinalizeRequest,
    authorized: bool = Depends(verify_api_key)
):

    allowed_decisions = [
        "red",
        "yellow",
        "green"
    ]

    decision = (
        request.final_decision
        .lower()
        .strip()
    )


    # -----------------------------------------------------
    # Validate decision
    # -----------------------------------------------------

    if decision not in allowed_decisions:

        return {
            "error": (
                "Invalid final decision. "
                "Use red, yellow, or green."
            )
        }


    # -----------------------------------------------------
    # Find case
    # -----------------------------------------------------

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM cases
        WHERE case_id = ?
        """,
        (case_id,)
    )

    case = cursor.fetchone()


    if case is None:

        connection.close()

        return {
            "error": "Case not found"
        }


    # -----------------------------------------------------
    # Previous decision
    # -----------------------------------------------------

    previous_decision = (
        case["final_decision"]
    )


    # -----------------------------------------------------
    # Update final decision + status
    # -----------------------------------------------------

    cursor.execute(
        """
        UPDATE cases
        SET
            final_decision = ?,
            status = ?
        WHERE case_id = ?
        """,
        (
            decision,
            "COMPLETED",
            case_id
        )
    )


    # -----------------------------------------------------
    # Record audit event
    # -----------------------------------------------------

    cursor.execute(
        """
        INSERT INTO case_audit_log (
            case_id,
            action,
            previous_decision,
            new_decision
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            case_id,
            "MANUAL_OVERRIDE",
            previous_decision,
            decision
        )
    )


    connection.commit()
    connection.close()


    return {
        "message": "Case finalized successfully",
        "case_id": case_id,
        "final_decision": decision,
        "status": "COMPLETED"
    }


# =========================================================
# GET CASE AUDIT HISTORY
# =========================================================

@router.get("/cases/{case_id}/audit")
def get_case_audit(
    case_id: str,
    authorized: bool = Depends(verify_api_key)
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            case_id,
            action,
            previous_decision,
            new_decision,
            created_at
        FROM case_audit_log
        WHERE case_id = ?
        ORDER BY created_at DESC
        """,
        (case_id,)
    )

    audit_entries = cursor.fetchall()

    connection.close()


    return [
        dict(entry)
        for entry in audit_entries
    ]