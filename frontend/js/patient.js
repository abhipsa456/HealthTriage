const API_URL = "http://127.0.0.1:8000";


// =========================================================
// HELPER: GET OPTIONAL FIELD VALUE
// =========================================================

function getOptionalValue(id) {

    const element =
        document.getElementById(id);

    if (!element) {
        return null;
    }

    const value =
        element.value.trim();

    return value === "" ? null : value;
}


// =========================================================
// ANALYZE CASE
// =========================================================

async function analyzeCase() {

    const patientName =
        document.getElementById("patientName")?.value.trim() || "";

    const ageValue =
        document.getElementById("age")?.value || "";

    const gender =
        document.getElementById("gender")?.value || "";

    const existingConditions =
        document.getElementById("conditions")?.value.trim() || "";

    const symptomsElement =
        document.getElementById("symptoms");

    const symptoms =
        symptomsElement?.value.trim() || "";

    const consent =
        document.getElementById("consent");

    const imageInput =
        document.getElementById("imageUpload");

    const reportInput =
        document.getElementById("reportUpload");

    const analyzeButton =
        document.getElementById("analyzeButton");


    // =====================================================
    // VALIDATION
    // =====================================================

    if (!symptoms) {

        alert(
            "Please describe the patient's symptoms."
        );

        symptomsElement?.focus();

        return;
    }


    if (consent && !consent.checked) {

        alert(
            "Please provide consent before continuing."
        );

        return;
    }


    const imageFile =
        imageInput?.files?.[0] || null;

    const reportFile =
        reportInput?.files?.[0] || null;


    if (imageFile && reportFile) {

        alert(
            "Please upload either an image or a medical report, not both."
        );

        return;
    }


    if (analyzeButton) {

        analyzeButton.disabled = true;

        analyzeButton.textContent =
            "Analyzing...";
    }


    try {

        // =================================================
        // UPLOAD IMAGE / REPORT IF SELECTED
        // =================================================

        let uploadedFile = null;

        const selectedFile =
            imageFile || reportFile;


        if (selectedFile) {

            const formData =
                new FormData();

            formData.append(
                "file",
                selectedFile
            );


            const uploadResponse =
                await fetch(
                    `${API_URL}/api/patient/upload`,
                    {
                        method: "POST",
                        body: formData
                    }
                );


            if (!uploadResponse.ok) {

                let errorMessage =
                    "File upload failed.";

                try {

                    const errorData =
                        await uploadResponse.json();

                    if (errorData.detail) {

                        errorMessage =
                            errorData.detail;
                    }

                } catch (error) {

                    console.error(
                        error
                    );
                }


                throw new Error(
                    errorMessage
                );
            }


            uploadedFile =
                await uploadResponse.json();


            console.log(
                "Uploaded file:",
                uploadedFile
            );
        }


        // =================================================
        // GET VOICE TRANSCRIPT
        // =================================================

        const voiceTranscript =
            localStorage.getItem(
                "voiceTranscript"
            ) || null;


        // =================================================
        // GET STRUCTURED CLINICAL INFORMATION
        // =================================================

        const temperature =
            getOptionalValue("temperature");

        const heartRate =
            getOptionalValue("heartRate");

        const spo2 =
            getOptionalValue("spo2");

        const respiratoryRate =
            getOptionalValue(
                "respiratoryRate"
            );

        const systolicBp =
            getOptionalValue(
                "systolicBp"
            );

        const diastolicBp =
            getOptionalValue(
                "diastolicBp"
            );


        const diabetesHistory =
            getOptionalValue(
                "diabetesHistory"
            );

        const hypertensionHistory =
            getOptionalValue(
                "hypertensionHistory"
            );

        const asthmaHistory =
            getOptionalValue(
                "asthmaHistory"
            );

        const heartDiseaseHistory =
            getOptionalValue(
                "heartDiseaseHistory"
            );

        const previousHospitalization =
            getOptionalValue(
                "previousHospitalization"
            );


        const painLevel =
            getOptionalValue(
                "painLevel"
            );

        const symptomDuration =
            getOptionalValue(
                "symptomDuration"
            );

        const medicationCount =
            getOptionalValue(
                "medicationCount"
            );


        // =================================================
        // PREPARE TRIAGE REQUEST
        // =================================================

        const triageData = {

            // ---------------------------------------------
            // Basic patient information
            // ---------------------------------------------

            patient_name:
                patientName || null,

            age:
                ageValue
                    ? parseInt(
                        ageValue,
                        10
                    )
                    : null,

            gender:
                gender || null,

            existing_conditions:
                existingConditions || null,


            // ---------------------------------------------
            // Symptoms
            // ---------------------------------------------

            symptoms:
                symptoms,

            voice_transcript:
                voiceTranscript,


            // ---------------------------------------------
            // Vitals
            // ---------------------------------------------

            temperature:
                temperature !== null
                    ? parseFloat(
                        temperature
                    )
                    : null,

            heart_rate:
                heartRate !== null
                    ? parseFloat(
                        heartRate
                    )
                    : null,

            spo2:
                spo2 !== null
                    ? parseFloat(
                        spo2
                    )
                    : null,

            respiratory_rate:
                respiratoryRate !== null
                    ? parseFloat(
                        respiratoryRate
                    )
                    : null,

            systolic_bp:
                systolicBp !== null
                    ? parseFloat(
                        systolicBp
                    )
                    : null,

            diastolic_bp:
                diastolicBp !== null
                    ? parseFloat(
                        diastolicBp
                    )
                    : null,


            // ---------------------------------------------
            // Medical history
            // ---------------------------------------------

            diabetes_history:
                diabetesHistory || null,

            hypertension_history:
                hypertensionHistory || null,

            asthma_history:
                asthmaHistory || null,

            heart_disease_history:
                heartDiseaseHistory || null,

            previous_hospitalization:
                previousHospitalization || null,


            // ---------------------------------------------
            // Additional information
            // ---------------------------------------------

            pain_level:
                painLevel !== null
                    ? parseFloat(
                        painLevel
                    )
                    : null,

            symptom_duration_days:
                symptomDuration !== null
                    ? parseFloat(
                        symptomDuration
                    )
                    : null,

            medication_count:
                medicationCount !== null
                    ? parseInt(
                        medicationCount,
                        10
                    )
                    : null,


            // ---------------------------------------------
            // Uploaded file information
            // ---------------------------------------------

            image_filename:
                uploadedFile
                    ? uploadedFile.filename
                    : null,

            image_stored_as:
                uploadedFile
                    ? uploadedFile.stored_as
                    : null,

            image_file_type:
                uploadedFile
                    ? uploadedFile.file_type
                    : null
        };


        console.log(
            "Sending triage request:",
            triageData
        );


        // =================================================
        // SEND CASE TO BACKEND
        // =================================================

        try {

            const response =
                await fetch(
                    `${API_URL}/api/triage`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                triageData
                            )
                    }
                );


            // ---------------------------------------------
            // SERVER REJECTED REQUEST
            // ---------------------------------------------

            if (!response.ok) {

                let errorMessage =
                    "Backend request failed.";

                try {

                    const errorData =
                        await response.json();

                    if (errorData.detail) {

                        errorMessage =
                            errorData.detail;
                    }

                } catch (error) {

                    console.error(
                        error
                    );
                }


                throw new Error(
                    errorMessage
                );
            }


            // ---------------------------------------------
            // ONLINE SUCCESS
            // ---------------------------------------------

            const result =
                await response.json();


            console.log(
                "Triage result:",
                result
            );


            localStorage.setItem(
                "triageResult",
                JSON.stringify(
                    result
                )
            );


            localStorage.setItem(
                "triageMode",
                "online"
            );


            // Save uploaded file information
            if (uploadedFile) {

                localStorage.setItem(
                    "uploadedFile",
                    JSON.stringify(
                        uploadedFile
                    )
                );

            } else {

                localStorage.removeItem(
                    "uploadedFile"
                );
            }


            // Voice transcript is no longer needed
            localStorage.removeItem(
                "voiceTranscript"
            );


            // Open result page
            window.location.href =
                "result.html";


        } catch (error) {

    // =================================================
    // OFFLINE MODE
    // =================================================

    console.warn(
        "Backend unavailable. Switching to offline mode.",
        error
    );

    try {

        const offlineCase =
            saveOfflineCase(triageData);

        localStorage.setItem(
            "triageMode",
            "offline"
        );

        localStorage.setItem(
            "offlineCase",
            JSON.stringify(offlineCase)
        );

        localStorage.removeItem(
            "voiceTranscript"
        );

        console.log(
            "Case successfully saved offline:",
            offlineCase
        );

        alert(
            "No connection to the healthcare server.\n\n" +
            "Your case has been securely saved on this device " +
            "and will be synchronized when the connection is restored."
        );

        window.location.href =
            "result.html";

    } catch (offlineError) {

        console.error(
            "Offline save failed:",
            offlineError
        );

        alert(
            "The healthcare server is unavailable, " +
            "and the case could not be saved locally.\n\n" +
            offlineError.message
        );
    }
}


    } catch (error) {

        // =================================================
        // GENERAL ERROR
        // =================================================

        console.error(
            "Triage error:",
            error
        );


        alert(
            "Unable to process the case.\n\n" +
            error.message
        );


    } finally {

        if (analyzeButton) {

            analyzeButton.disabled =
                false;

            analyzeButton.textContent =
                "Analyze Case";
        }
    }
}


// =========================================================
// VOICE INPUT
// =========================================================

async function startVoiceInput() {

    const symptoms =
        document.getElementById("symptoms");

    const voiceButton =
        document.getElementById("voiceButton");

    const selectedLanguage =
        localStorage.getItem("healthtriage_language") || "en";


    // =====================================================
    // ODIA: LOCAL AI4BHARAT ASR
    // =====================================================

    if (selectedLanguage === "or") {

        if (
            !navigator.mediaDevices ||
            !navigator.mediaDevices.getUserMedia
        ) {
            alert(
                "Microphone recording is not supported in this browser."
            );

            return;
        }

        let mediaRecorder = null;
        let audioChunks = [];

        try {

            const stream =
                await navigator.mediaDevices.getUserMedia({
                    audio: true
                });

            mediaRecorder =
                new MediaRecorder(stream);

            audioChunks = [];

            mediaRecorder.ondataavailable =
                function (event) {

                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };

            mediaRecorder.onstart =
                function () {

                    console.log(
                        "🎙️ Recording Odia..."
                    );

                    if (voiceButton) {

                        voiceButton.textContent =
                            "🎙️ Recording...";

                        voiceButton.disabled =
                            true;
                    }
                };

            mediaRecorder.onstop =
                async function () {

                    console.log(
                        "🎙️ Odia recording stopped."
                    );

                    stream.getTracks().forEach(
                        track => track.stop()
                    );

                    if (voiceButton) {

                        voiceButton.textContent =
                            "⏳ Transcribing...";
                    }

                    try {

                        const audioBlob =
                            new Blob(
                                audioChunks,
                                {
                                    type:
                                        mediaRecorder.mimeType ||
                                        "audio/webm"
                                }
                            );

                        if (audioBlob.size === 0) {

                            throw new Error(
                                "No audio was recorded."
                            );
                        }

                        const formData =
                            new FormData();

                        formData.append(
                            "audio",
                            audioBlob,
                            "odia_voice.webm"
                        );

                        const response =
                            await fetch(
                                `${API_URL}/api/speech/transcribe`,
                                {
                                    method: "POST",
                                    body: formData
                                }
                            );

                        if (!response.ok) {

                            let errorMessage =
                                "Odia speech transcription failed.";

                            try {

                                const errorData =
                                    await response.json();

                                if (errorData.detail) {

                                    errorMessage =
                                        errorData.detail;
                                }

                            } catch (error) {

                                console.error(
                                    error
                                );
                            }

                            throw new Error(
                                errorMessage
                            );
                        }

                        const result =
                            await response.json();

                        const transcript =
                            result.transcript?.trim();

                        if (!transcript) {

                            throw new Error(
                                "No speech could be recognized."
                            );
                        }

                        if (symptoms) {

                            if (
                                symptoms.value.trim()
                            ) {

                                symptoms.value +=
                                    " " + transcript;

                            } else {

                                symptoms.value =
                                    transcript;
                            }
                        }

                        localStorage.setItem(
                            "voiceTranscript",
                            transcript
                        );

                        console.log(
                            "Odia voice recognized:",
                            transcript
                        );

                    } catch (error) {

                        console.error(
                            "Odia transcription error:",
                            error
                        );

                        alert(
                            "Could not transcribe the Odia speech.\n\n" +
                            error.message
                        );

                    } finally {

                        if (voiceButton) {

                            voiceButton.textContent =
                                "🎙️ Speak";

                            voiceButton.disabled =
                                false;
                        }
                    }
                };

            mediaRecorder.onerror =
                function (event) {

                    console.error(
                        "Odia recorder error:",
                        event.error
                    );

                    stream.getTracks().forEach(
                        track => track.stop()
                    );

                    if (voiceButton) {

                        voiceButton.textContent =
                            "🎙️ Speak";

                        voiceButton.disabled =
                            false;
                    }

                    alert(
                        "Microphone recording failed."
                    );
                };

            mediaRecorder.start();

            setTimeout(
                function () {

                    if (
                        mediaRecorder &&
                        mediaRecorder.state ===
                            "recording"
                    ) {

                        mediaRecorder.stop();
                    }

                },
                8000
            );

        } catch (error) {

            console.error(
                "Could not start Odia recording:",
                error
            );

            if (voiceButton) {

                voiceButton.textContent =
                    "🎙️ Speak";

                voiceButton.disabled =
                    false;
            }

            if (
                error.name ===
                "NotAllowedError"
            ) {

                alert(
                    "Microphone permission was denied."
                );

            } else {

                alert(
                    "Could not access the microphone.\n\n" +
                    error.message
                );
            }
        }

        return;
    }


    // =====================================================
    // ENGLISH / HINDI: BROWSER SPEECH RECOGNITION
    // =====================================================

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Speech recognition is not supported in this browser."
        );

        return;
    }


    const recognition =
        new SpeechRecognition();


    const speechLanguages = {

        en: "en-IN",

        hi: "hi-IN"
    };


    console.log(
        "Selected language:",
        selectedLanguage
    );


    recognition.lang =
        speechLanguages[selectedLanguage] ||
        "en-IN";


    recognition.continuous =
        false;


    recognition.interimResults =
        false;


    recognition.maxAlternatives =
        1;


    recognition.onstart =
        function () {

            console.log(
                "🎙️ Listening..."
            );


            if (voiceButton) {

                voiceButton.textContent =
                    "🎙️ Listening...";

                voiceButton.disabled =
                    true;
            }
        };


    recognition.onresult =
        function (event) {

            const transcript =
                event.results[0][0]
                    .transcript;


            if (symptoms) {

                if (
                    symptoms.value.trim()
                ) {

                    symptoms.value +=
                        " " + transcript;

                } else {

                    symptoms.value =
                        transcript;
                }
            }


            localStorage.setItem(
                "voiceTranscript",
                transcript
            );


            console.log(
                "Voice recognized:",
                transcript
            );
        };


    recognition.onerror =
        function (event) {

            console.error(
                "Speech recognition error:",
                event.error
            );


            if (
                event.error ===
                "network"
            ) {

                alert(
                    "Browser speech recognition is unavailable right now. " +
                    "Please use Chrome or Edge with an internet connection, " +
                    "or type your symptoms manually."
                );

            } else if (
                event.error ===
                "not-allowed"
            ) {

                alert(
                    "Microphone permission was denied."
                );

            } else if (
                event.error ===
                "no-speech"
            ) {

                alert(
                    "No speech detected. Please try speaking again."
                );

            } else {

                alert(
                    "Voice input error: " +
                    event.error
                );
            }
        };


    recognition.onend =
        function () {

            console.log(
                "🎙️ Voice recognition ended."
            );


            if (voiceButton) {

                voiceButton.textContent =
                    "🎙️ Speak";

                voiceButton.disabled =
                    false;
            }
        };


    try {

        recognition.start();

    } catch (error) {

        console.error(
            "Could not start voice recognition:",
            error
        );

    }
}


// =========================================================
// FILE SELECTION
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const imageInput =
            document.getElementById(
                "imageUpload"
            );

        const reportInput =
            document.getElementById(
                "reportUpload"
            );

        const imageFileName =
            document.getElementById(
                "imageFileName"
            );

        const reportFileName =
            document.getElementById(
                "reportFileName"
            );


        // -------------------------------------------------
        // Image selection
        // -------------------------------------------------

        if (imageInput) {

            imageInput.addEventListener(
                "change",
                function () {

                    if (
                        imageInput.files.length >
                        0
                    ) {

                        const file =
                            imageInput.files[0];


                        // Clear report selection
                        if (reportInput) {

                            reportInput.value =
                                "";
                        }


                        if (reportFileName) {

                            reportFileName.textContent =
                                "";
                        }


                        if (imageFileName) {

                            imageFileName.textContent =
                                `Selected: ${file.name}`;
                        }

                    } else if (
                        imageFileName
                    ) {

                        imageFileName.textContent =
                            "";
                    }
                }
            );
        }


        // -------------------------------------------------
        // Report selection
        // -------------------------------------------------

        if (reportInput) {

            reportInput.addEventListener(
                "change",
                function () {

                    if (
                        reportInput.files.length >
                        0
                    ) {

                        const file =
                            reportInput.files[0];


                        // Clear image selection
                        if (imageInput) {

                            imageInput.value =
                                "";
                        }


                        if (imageFileName) {

                            imageFileName.textContent =
                                "";
                        }


                        if (reportFileName) {

                            reportFileName.textContent =
                                `Selected: ${file.name}`;
                        }

                    } else if (
                        reportFileName
                    ) {

                        reportFileName.textContent =
                            "";
                    }
                }
            );
        }
    }
);


// =========================================================
// LOGOUT
// =========================================================

function logout() {

    window.location.href =
        "login.html";
}