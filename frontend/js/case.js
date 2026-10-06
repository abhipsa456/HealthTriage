const API_URL = "http://127.0.0.1:8000";

const API_KEY = "demo-healthtriage-key";

function setText(id, value) {
    const element = document.getElementById(id);

    if (element) {
        element.textContent = value ?? "";
    }
}

async function loadCase() {

    const params =
        new URLSearchParams(
            window.location.search
        );

    const caseId =
        params.get("id");

    if (!caseId) {

        alert(
            "No case ID provided."
        );

        return;
    }

    try {

        const response =
            await fetch(
                `${API_URL}/api/cases/${encodeURIComponent(caseId)}`,
                {
                    headers: {
                        "X-API-Key": API_KEY
                    }
                }
            );

        if (!response.ok) {

            throw new Error(
                "Failed to load case."
            );
        }

        const caseData =
            await response.json();

        if (caseData.error) {

            alert(
                "Case not found."
            );

            return;
        }


        // =====================================================
        // BASIC CASE INFORMATION
        // =====================================================

        setText(
            "caseTitle",
            `Case ${caseData.case_id}`
        );

        setText(
            "caseId",
            caseData.case_id
        );

        setText(
            "patientName",
            caseData.patient_name ||
            "Not provided"
        );

        setText(
            "patientAge",
            caseData.age ??
            "Not provided"
        );

        setText(
            "patientGender",
            caseData.gender ||
            "Not provided"
        );

        setText(
            "existingConditions",
            caseData.existing_conditions ||
            "None provided"
        );

        setText(
            "symptoms",
            caseData.symptoms ||
            "No symptoms provided"
        );

        setText(
            "voiceTranscript",
            caseData.voice_transcript ||
            "No voice transcript available."
        );


        // =====================================================
        // DETERMINE TRIAGE LEVEL
        // =====================================================

        const level = (
            caseData.final_decision ||
            caseData.triage_level ||
            "green"
        ).toLowerCase();


        // =====================================================
        // UPDATE PRIORITY / URGENCY
        // =====================================================

        updatePriorityDisplay(
            level
        );


        // =====================================================
        // MEDIFUSION AI CONFIDENCE
        // =====================================================

        const medifusion =
            caseData
                .multimodal_analysis
                ?.medifusion || {};

        const medifusionConfidence =
            medifusion.confidence;

        let confidencePercent = null;

        if (
            medifusionConfidence !== null &&
            medifusionConfidence !== undefined
        ) {

            confidencePercent =
                (
                    Number(
                        medifusionConfidence
                    ) * 100
                ).toFixed(2);
        }


        // -----------------------------------------------------
        // Display MediFusion confidence
        // -----------------------------------------------------

        setText(
            "confidence",
            confidencePercent !== null
                ? `${confidencePercent}%`
                : "N/A"
        );


        // -----------------------------------------------------
        // Confidence bar
        // -----------------------------------------------------

        const confidenceFill =
            document.getElementById(
                "confidenceFill"
            );

        if (confidenceFill) {

            confidenceFill.style.width =
                confidencePercent !== null
                    ? `${confidencePercent}%`
                    : "0%";
        }


        // =====================================================
        // AI SUMMARY & REASONING
        // =====================================================

        setText(
            "summary",
            caseData.summary ||
            "No summary available."
        );

        setText(
            "reasoning",
            caseData.reasoning ||
            "No reasoning available."
        );


        // =====================================================
        // EXPLAINABILITY
        // =====================================================

        displayDetectedFactors(
            caseData.detected_factors
        );


        // =====================================================
        // HUMAN REVIEW
        // =====================================================

        updateHumanReviewStatus(
            caseData.human_review_required,
            medifusionConfidence
        );


        // =====================================================
        // FINAL DECISION
        // =====================================================

        setText(
            "finalDecision",
            caseData.final_decision
                ? caseData.final_decision.toUpperCase()
                : "Not finalized"
        );


        // =====================================================
        // SUPPORTING INFORMATION
        // =====================================================

        loadSupportingInformation(
            caseData
        );

        loadAuditHistory(
            caseId
        );

    } catch (error) {

        console.error(
            "Case loading error:",
            error
        );

        alert(
            "Unable to load case details.\n\n" +
            "Please make sure the backend is running."
        );
    }
}


// =========================================================
// UPDATE PRIORITY DISPLAY
// =========================================================

function updatePriorityDisplay(level) {

    const priorityBadge =
        document.getElementById(
            "priorityBadge"
        );

    const aiLevel =
        document.getElementById(
            "aiLevel"
        );

    const triageLevel =
        document.getElementById(
            "triageLevel"
        );


    let label;

    let className;


    if (level === "red") {

        label = "RED";

        className = "red";

    } else if (level === "yellow") {

        label = "YELLOW";

        className = "yellow";

    } else {

        label = "GREEN";

        className = "green";
    }


    // -----------------------------------------------------
    // Header priority badge
    // -----------------------------------------------------

    if (priorityBadge) {

        priorityBadge.textContent =
            label;

        priorityBadge.classList.remove(
            "priority-red",
            "priority-yellow",
            "priority-green"
        );

        priorityBadge.classList.add(
            `priority-${className}`
        );
    }


    // -----------------------------------------------------
    // Large AI urgency level
    // -----------------------------------------------------

    if (aiLevel) {

        aiLevel.textContent =
            label;

        aiLevel.classList.remove(
            "red-text",
            "yellow-text",
            "green-text"
        );

        aiLevel.classList.add(
            `${className}-text`
        );
    }


    // -----------------------------------------------------
    // Human-readable urgency
    // -----------------------------------------------------

    if (triageLevel) {

        if (level === "red") {

            triageLevel.textContent =
                "Emergency";

        } else if (level === "yellow") {

            triageLevel.textContent =
                "Urgent";

        } else {

            triageLevel.textContent =
                "Non-Urgent";
        }
    }
}


// =========================================================
// SUPPORTING INFORMATION
// =========================================================

function loadSupportingInformation(
    caseData
) {

    const imageContainer =
        document.getElementById(
            "imageSupport"
        );

    const reportContainer =
        document.getElementById(
            "reportSupport"
        );


    if (!caseData.image_stored_as) {

        if (imageContainer) {

            imageContainer.innerHTML =
                "<p>No image uploaded.</p>";
        }

        if (reportContainer) {

            reportContainer.innerHTML =
                "<p>No medical report uploaded.</p>";
        }

        return;
    }


    const fileUrl =
        `${API_URL}/api/patient/file/${encodeURIComponent(
            caseData.image_stored_as
        )}`;

    const fileType =
        caseData.image_file_type || "";


    // -----------------------------------------------------
    // IMAGE
    // -----------------------------------------------------

    if (
        fileType.startsWith("image/")
    ) {

        if (imageContainer) {

            imageContainer.innerHTML = `
                <img
                    src="${fileUrl}"
                    alt="Patient uploaded image"
                    style="
                        max-width: 300px;
                        max-height: 250px;
                        border-radius: 10px;
                        margin-top: 10px;
                    "
                >

                <p>
                    ${
                        caseData.image_filename ||
                        "Uploaded image"
                    }
                </p>
            `;
        }

        if (reportContainer) {

            reportContainer.innerHTML =
                "<p>No medical report uploaded.</p>";
        }

        return;
    }


    // -----------------------------------------------------
    // PDF MEDICAL REPORT
    // -----------------------------------------------------

    if (
        fileType ===
        "application/pdf"
    ) {

        if (reportContainer) {

            reportContainer.innerHTML = `
                <p>
                    ${
                        caseData.image_filename ||
                        "Medical report"
                    }
                </p>

                <a
                    href="${fileUrl}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="view-button"
                >
                    📄 View Report
                </a>
            `;
        }

        if (imageContainer) {

            imageContainer.innerHTML =
                "<p>No image uploaded.</p>";
        }

        return;
    }


    // -----------------------------------------------------
    // OTHER FILE
    // -----------------------------------------------------

    if (imageContainer) {

        imageContainer.innerHTML =
            "<p>No image uploaded.</p>";
    }

    if (reportContainer) {

        reportContainer.innerHTML = `
            <p>
                ${
                    caseData.image_filename ||
                    "Uploaded file"
                }
            </p>

            <a
                href="${fileUrl}"
                target="_blank"
                rel="noopener noreferrer"
                class="view-button"
            >
                📄 View File
            </a>
        `;
    }
}


// =========================================================
// EXPLAINABILITY
// =========================================================

function displayDetectedFactors(
    factors
) {

    const container =
        document.getElementById(
            "detectedFactors"
        );


    if (!container) {
        return;
    }


    if (
        !Array.isArray(factors) ||
        factors.length === 0
    ) {

        container.innerHTML = `
            <p>
                No specific factors were recorded
                for this case.
            </p>
        `;

        return;
    }


    container.innerHTML = `
        <ul class="detected-factors-list">

            ${factors.map(
                factor => `
                    <li>
                        ${escapeHtml(factor)}
                    </li>
                `
            ).join("")}

        </ul>
    `;
}


// =========================================================
// HUMAN REVIEW STATUS
// =========================================================

function updateHumanReviewStatus(
    humanReviewRequired,
    confidence
) {

    const container =
        document.getElementById(
            "humanReviewStatus"
        );


    if (!container) {
        return;
    }


    let confidenceText =
        "N/A";


    if (
        confidence !== null &&
        confidence !== undefined
    ) {

        confidenceText =
            (
                Number(confidence) *
                100
            ).toFixed(2) + "%";
    }


    if (humanReviewRequired) {

        container.innerHTML = `
            <div class="review-required">

                <strong>
                    ⚠ Human review required
                </strong>

                <p>
                    The AI assessment should be reviewed
                    by healthcare staff before a final
                    clinical decision is recorded.
                </p>

                <p>
                    MediFusion AI confidence:
                    <strong>
                        ${confidenceText}
                    </strong>
                </p>

            </div>
        `;

    } else {

        container.innerHTML = `
            <div class="review-not-required">

                <strong>
                    ✓ No automatic review flag
                </strong>

                <p>
                    The demo system did not trigger its
                    low-confidence review threshold.
                </p>

                <p>
                    MediFusion AI confidence:
                    <strong>
                        ${confidenceText}
                    </strong>
                </p>

            </div>
        `;
    }
}


// =========================================================
// FINALIZE CASE
// =========================================================

async function setDecision(
    decision
) {

    const params =
        new URLSearchParams(
            window.location.search
        );

    const caseId =
        params.get("id");


    if (!caseId) {

        alert(
            "No case ID provided."
        );

        return;
    }


    const confirmed =
        confirm(
            `Finalize this case as ${decision.toUpperCase()}?`
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/api/cases/${encodeURIComponent(
                    caseId
                )}/finalize`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "X-API-Key":
                            API_KEY
                    },

                    body: JSON.stringify({
                        final_decision:
                            decision.toLowerCase()
                    })
                }
            );


        const result =
            await response.json();


        if (
            !response.ok ||
            result.error
        ) {

            throw new Error(
                result.error ||
                "Failed to finalize case."
            );
        }


        alert(
            `Case finalized as ${decision.toUpperCase()}.`
        );


        loadCase();


    } catch (error) {

        console.error(
            "Finalization error:",
            error
        );

        alert(
            "Unable to finalize the case.\n\n" +
            "Please make sure the backend is running."
        );
    }
}


// =========================================================
// NAVIGATION
// =========================================================

function goBack() {

    window.location.href =
        "dashboard.html";
}


function logout() {

    window.location.href =
        "login.html";
}


// =========================================================
// AUDIT HISTORY
// =========================================================

async function loadAuditHistory(
    caseId
) {

    const container =
        document.getElementById(
            "auditHistory"
        );


    if (!container) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/api/cases/${encodeURIComponent(
                    caseId
                )}/audit`,
                {
                    headers: {
                        "X-API-Key":
                            API_KEY
                    }
                }
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load audit history."
            );
        }


        const entries =
            await response.json();


        if (
            !Array.isArray(entries) ||
            entries.length === 0
        ) {

            container.innerHTML = `
                <p>
                    No clinician actions have been recorded yet.
                </p>
            `;

            return;
        }


        container.innerHTML =
            entries.map(
                entry => {

                    const previous =
                        entry.previous_decision
                            ? entry.previous_decision
                                .toUpperCase()
                            : "NONE";

                    const current =
                        entry.new_decision
                            ? entry.new_decision
                                .toUpperCase()
                            : "NONE";

                    const date =
                        entry.created_at ||
                        "Unknown time";


                    return `
                        <div class="audit-entry">

                            <div class="audit-action">
                                ${escapeHtml(
                                    entry.action
                                )}
                            </div>

                            <div class="audit-details">

                                <p>
                                    <strong>
                                        Previous decision:
                                    </strong>
                                    ${previous}
                                </p>

                                <p>
                                    <strong>
                                        New decision:
                                    </strong>
                                    ${current}
                                </p>

                                <p>
                                    <strong>
                                        Time:
                                    </strong>
                                    ${escapeHtml(
                                        date
                                    )}
                                </p>

                            </div>

                        </div>
                    `;
                }
            ).join("");


    } catch (error) {

        console.error(
            "Audit history error:",
            error
        );

        container.innerHTML = `
            <p>
                Unable to load decision history.
            </p>
        `;
    }
}


// =========================================================
// HTML ESCAPE
// =========================================================

function escapeHtml(
    value
) {

    return String(
        value ?? ""
    )
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}


// =========================================================
// START
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    loadCase
);