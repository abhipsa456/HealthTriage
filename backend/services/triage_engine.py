import uuid

CONFIDENCE_THRESHOLD = 0.70


# ---------------------------------------------------------
# SAFETY GATE
# ---------------------------------------------------------

def apply_safety_gate(
    triage_level: str,
    confidence: float,
    human_review_required: bool = False
):
    """
    Safety gate for the demo triage system.

    Low-confidence results are always sent for human review.
    """

    if confidence < CONFIDENCE_THRESHOLD:
        human_review_required = True

    return {
        "triage_level": triage_level,
        "confidence": confidence,
        "human_review_required": human_review_required
    }


# ---------------------------------------------------------
# KEYWORD HELPERS
# ---------------------------------------------------------

def contains_any(text: str, keywords: list[str]) -> list[str]:
    """
    Returns all keywords/phrases found in the submitted text.
    """

    return [
        keyword
        for keyword in keywords
        if keyword in text
    ]


EMERGENCY_KEYWORDS = [
    "unconscious",
    "severe bleeding",
    "difficulty breathing",
    "breathing difficulty",
    "shortness of breath",
    "trouble breathing",
    "chest pain",
    "seizure",
    "loss of consciousness"
]


NEGATION_WORDS = [
    "no",
    "not",
    "without",
    "denies",
    "denied",
    "never"
]


def is_negated(text: str, keyword: str) -> bool:
    """
    Checks whether a keyword is explicitly negated.

    Handles examples such as:
    'no breathing difficulty'
    'no chest pain or severe pain'
    'without vomiting'
    'denies chest pain'
    """

    text = text.lower()
    keyword = keyword.lower()

    index = text.find(keyword)

    if index == -1:
        return False

    # Look back far enough to capture coordinated phrases such as:
    # "No breathing difficulty, chest pain, vomiting, or severe pain."
    before_keyword = text[max(0, index - 100):index]

    # Direct negation immediately before the keyword
    for word in NEGATION_WORDS:
        if f" {word} " in f" {before_keyword} ":
            return True

    # Handle coordinated negative lists:
    # "no A, B, or C"
    negative_list_patterns = [
        "no ",
        "not ",
        "without ",
        "denies ",
        "denied ",
        "never "
    ]

    for pattern in negative_list_patterns:
        if pattern in before_keyword:
            return True

    return False


def find_active_emergency_keywords(text: str) -> list[str]:
    """
    Returns emergency keywords that are present
    and are not explicitly negated.
    """

    text = text.lower()

    active_keywords = []

    for keyword in EMERGENCY_KEYWORDS:
        if keyword in text and not is_negated(text, keyword):
            active_keywords.append(keyword)

    return active_keywords


# ---------------------------------------------------------
# MAIN TRIAGE ENGINE
# ---------------------------------------------------------

def generate_triage(symptoms: str):
    """
    Temporary demo triage engine.

    IMPORTANT:
    This is NOT a medically validated model.
    It is intended only for prototype demonstration.

    The current rules are only for demonstration and
    should not be used for real medical decision-making.
    """

    text = (symptoms or "").lower().strip()

    # ---------------------------------------------------------
    # URGENT PATTERNS
    # ---------------------------------------------------------

    urgent_keywords = [
        "high fever",
        "persistent vomiting",
        "severe pain",
        "swelling",
        "infection",
        "persistent pain",
        "continuous vomiting"
    ]

    # Only non-negated emergency keywords are considered.
    emergency_matches = find_active_emergency_keywords(text)

    urgent_matches = [
    keyword
    for keyword in urgent_keywords
    if keyword in text and not is_negated(text, keyword)
]

    detected_factors = []

    # ---------------------------------------------------------
    # RED: EMERGENCY
    # ---------------------------------------------------------

    if emergency_matches:

        triage_level = "red"
        confidence = 0.90

        summary = (
            "The submitted information contains "
            "a high-priority symptom that may require "
            "immediate medical assessment."
        )

        reasoning = (
            "The demo rule engine detected one or more "
            "high-priority symptom patterns in the submitted information. "
            "Human clinical assessment is required."
        )

        human_review = True

        for keyword in emergency_matches:
            detected_factors.append(
                f"High-priority symptom detected: {keyword}"
            )

        detected_factors.append(
            "Emergency-level human review recommended by demo rules"
        )

    # ---------------------------------------------------------
    # YELLOW: URGENT
    # ---------------------------------------------------------

    elif urgent_matches:

        triage_level = "yellow"
        confidence = 0.82

        summary = (
            "The submitted information contains "
            "symptoms that may require timely medical assessment."
        )

        reasoning = (
            "The demo rule engine detected one or more "
            "symptom patterns that may require prompt clinical review."
        )

        human_review = True

        for keyword in urgent_matches:
            detected_factors.append(
                f"Urgent symptom detected: {keyword}"
            )

        detected_factors.append(
            "Prompt clinical review recommended by demo rules"
        )

    # ---------------------------------------------------------
    # GREEN: NO HIGH-PRIORITY MATCH
    # ---------------------------------------------------------

    else:

        triage_level = "green"
        confidence = 0.75

        summary = (
            "No high-priority symptom was detected "
            "by the current demo rules."
        )

        reasoning = (
            "The submitted information did not match "
            "the demo system's high-priority symptom patterns."
        )

        human_review = False

        detected_factors.append(
            "No high-priority symptom matched the demo rules"
        )

    # ---------------------------------------------------------
    # SAFETY GATE
    # ---------------------------------------------------------

    safety_result = apply_safety_gate(
        triage_level,
        confidence,
        human_review
    )

    # ---------------------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------------------

    return {
        "case_id": f"HT-{str(uuid.uuid4())[:8].upper()}",
        "triage_level": safety_result["triage_level"],
        "confidence": safety_result["confidence"],
        "summary": summary,
        "reasoning": reasoning,
        "human_review_required": safety_result["human_review_required"],
        "detected_factors": detected_factors
    }