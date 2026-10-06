const API_URL = "https://healthtriage-backend-s5rz.onrender.com";
const API_KEY = "demo-healthtriage-key";

let allCases = [];


// =========================================================
// LOAD CASES
// =========================================================

async function loadCases() {

    const tableBody =
        document.getElementById("caseTableBody");

    if (!tableBody) {
        console.error("caseTableBody not found.");
        return;
    }

    tableBody.innerHTML = `
        <tr>
            <td colspan="8" style="text-align:center; padding:30px;">
                Loading cases...
            </td>
        </tr>
    `;

    try {

        const response = await fetch(
            `${API_URL}/api/cases`,
            {
                method: "GET",
                headers: {
                    "X-API-Key": API_KEY
                }
            }
        );

        if (!response.ok) {
            throw new Error(
                `Server returned ${response.status}`
            );
        }

        allCases = await response.json();

// Load MediFusion AI confidence for each case
allCases = await Promise.all(
    allCases.map(async caseData => {

        try {

            const detailResponse = await fetch(
                `${API_URL}/api/cases/${encodeURIComponent(caseData.case_id)}`,
                {
                    headers: {
                        "X-API-Key": API_KEY
                    }
                }
            );

            if (detailResponse.ok) {

                const detailData =
                    await detailResponse.json();

                caseData.medifusion_confidence =
                    detailData
                        .multimodal_analysis
                        ?.medifusion
                        ?.confidence ?? null;

            } else {

                caseData.medifusion_confidence = null;
            }

        } catch (error) {

            console.error(
                `Failed to load MediFusion data for ${caseData.case_id}:`,
                error
            );

            caseData.medifusion_confidence = null;
        }

        return caseData;
    })
);

updateSummary(allCases);

displayCases(allCases);

    } catch (error) {

        console.error(
            "Failed to load cases:",
            error
        );

        tableBody.innerHTML = `
            <tr>
                <td
                    colspan="8"
                    style="text-align:center; padding:30px; color:#b91c1c;">
                    Unable to load cases.
                    Please make sure the backend is running.
                </td>
            </tr>
        `;
    }
}


// =========================================================
// UPDATE SUMMARY CARDS
// =========================================================

function updateSummary(cases) {

    const totalCases =
        document.getElementById("totalCases");

    const emergencyCases =
        document.getElementById("emergencyCases");

    const urgentCases =
        document.getElementById("urgentCases");

    const nonUrgentCases =
        document.getElementById("nonUrgentCases");


    let red = 0;
    let yellow = 0;
    let green = 0;


    cases.forEach(caseData => {

        const level = (
            caseData.final_decision ||
            caseData.triage_level ||
            ""
        ).toLowerCase();

        if (level === "red") {
            red++;
        }

        else if (level === "yellow") {
            yellow++;
        }

        else if (level === "green") {
            green++;
        }

    });


    totalCases.textContent = cases.length;
    emergencyCases.textContent = red;
    urgentCases.textContent = yellow;
    nonUrgentCases.textContent = green;
}


// =========================================================
// DISPLAY CASES
// =========================================================

function displayCases(cases) {

    const tableBody =
        document.getElementById("caseTableBody");


    if (!tableBody) {
        return;
    }


    if (!cases || cases.length === 0) {

        tableBody.innerHTML = `
            <tr>
                <td
                    colspan="8"
                    style="text-align:center; padding:30px;">
                    No cases found.
                </td>
            </tr>
        `;

        return;
    }


    tableBody.innerHTML = cases.map(caseData => {

        const level = (
            caseData.final_decision ||
            caseData.triage_level ||
            "unknown"
        ).toLowerCase();


        const reviewRequired =
            Boolean(
                caseData.human_review_required
            );


        const status =
            caseData.status || "WAITING";


        const priorityLabel = {

            red: "Emergency",
            yellow: "Urgent",
            green: "Non-Urgent"

        }[level] || "Unknown";


        return `
            <tr>

                <!-- PRIORITY -->
                <td>

                    <span class="triage-badge ${level}">
                        ${priorityLabel}
                    </span>

                </td>


                <!-- CASE ID -->
                <td>

                    <strong>
                        ${escapeHtml(
                            caseData.case_id
                        )}
                    </strong>

                </td>


                <!-- PATIENT -->
                <td>

                    ${escapeHtml(
                        caseData.patient_name ||
                        "Unnamed Patient"
                    )}

                </td>


                <!-- AGE -->
                <td>

                    ${caseData.age ?? "N/A"}

                </td>


                <!-- SYMPTOMS -->
                <td>

                    <span title="${escapeHtml(
                        caseData.symptoms || ""
                    )}">

                        ${escapeHtml(
                            truncateText(
                                caseData.symptoms ||
                                "No symptoms provided",
                                80
                            )
                        )}

                    </span>

                </td>


                <!-- CONFIDENCE -->
                <td>

                    ${formatConfidence(
                    caseData.medifusion_confidence
                    )}

                </td>


                <!-- STATUS -->
                <td>

                    <div>
                        ${escapeHtml(status)}
                    </div>

                    ${
                        reviewRequired
                        ? `
                            <small
                                style="
                                    color:#b45309;
                                    display:block;
                                    margin-top:4px;
                                ">
                                ⚠ Human review
                            </small>
                        `
                        : ""
                    }

                </td>


                <!-- ACTION -->
                <td>

                    <button
                        class="view-case-button"
                        onclick="openCase('${escapeHtml(
                            caseData.case_id
                        )}')">

                        View Case

                    </button>

                </td>

            </tr>
        `;

    }).join("");
}


// =========================================================
// FILTER CASES
// =========================================================

function filterCases(filter) {

    if (filter === "all") {

        displayCases(allCases);

        return;
    }


    const filteredCases =
        allCases.filter(caseData => {

            const level = (
                caseData.final_decision ||
                caseData.triage_level ||
                ""
            ).toLowerCase();

            return level === filter;

        });


    displayCases(filteredCases);
}


// =========================================================
// OPEN CASE
// =========================================================

function openCase(caseId) {

    window.location.href =
        `case.html?id=${encodeURIComponent(caseId)}`;
}


// =========================================================
// FORMAT CONFIDENCE
// =========================================================

function formatConfidence(value) {

    if (
        value === null ||
        value === undefined ||
        isNaN(value)
    ) {
        return "N/A";
    }

    return `${Math.round(
        Number(value) * 100
    )}%`;
}


// =========================================================
// TRUNCATE TEXT
// =========================================================

function truncateText(
    text,
    maxLength
) {

    if (!text) {
        return "";
    }

    text = String(text);


    if (text.length <= maxLength) {
        return text;
    }


    return (
        text.substring(0, maxLength)
        + "..."
    );
}


// =========================================================
// BASIC HTML ESCAPING
// =========================================================

function escapeHtml(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// =========================================================
// INITIAL LOAD
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    loadCases
);