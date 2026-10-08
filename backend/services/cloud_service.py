from typing import Optional

from backend.services.supabase_service import get_supabase


def save_case_to_cloud(case_data: dict) -> Optional[dict]:
    """
    Save a completed triage case to Supabase.

    Returns the inserted cloud record.
    Returns None if cloud saving fails.
    """

    try:
        supabase = get_supabase()

        response = (
            supabase
            .table("cases")
            .upsert(
                case_data,
                on_conflict="case_id"
            )
            .execute()
        )

        if response.data:
            return response.data[0]

        return None

    except Exception as error:
        print(f"[Cloud Sync] Failed to save case: {error}")
        return None