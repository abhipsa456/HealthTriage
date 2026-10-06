import os

from fastapi import Header, HTTPException


# =========================================================
# API KEY CONFIGURATION
# =========================================================

API_KEY = os.getenv(
    "HEALTHTRIAGE_API_KEY",
    "demo-healthtriage-key"
)


# =========================================================
# VERIFY API KEY
# =========================================================

def verify_api_key(
    x_api_key: str | None = Header(default=None)
):
    """
    Basic API-key protection for the prototype.

    In production, this should be replaced with
    proper authentication and role-based authorization.
    """

    if x_api_key != API_KEY:

        raise HTTPException(
            status_code=401,
            detail="Unauthorized request."
        )

    return True