const translations = {
    en: {
        patientAssessment: "Patient Assessment",
        logout: "Logout",
        badge: "AI-ASSISTED TRIAGE",
        heading: "Tell us how you're feeling",
        intro: "Provide the information below so our system can help healthcare staff assess your urgency.",

        patientDetails: "Patient Details",
        patientDetailsDesc: "Basic information about the patient",
        patientName: "Patient Name",
        patientNamePlaceholder: "Enter patient name",
        age: "Age",
        agePlaceholder: "Enter age",
        gender: "Gender",
        selectGender: "Select gender",
        female: "Female",
        male: "Male",
        other: "Other",
        preferNot: "Prefer not to say",
        existingConditions: "Existing Conditions",
        conditionsPlaceholder: "e.g. Diabetes, asthma",

        symptoms: "Describe Your Symptoms",
        symptomsDesc: "Type what you're experiencing in your own words.",
        symptomsPlaceholder: "For example: I have been having fever and cough for two days...",
        speak: "🎙️ Speak",
        symptomNote: "You can describe your symptoms naturally.",

        vitals: "Vitals",
        vitalsDesc: "Optional clinical measurements, if available",
        vitalsNote: "Enter vitals only if they have been measured. Leave blank if unavailable.",
        temperature: "Temperature (°C)",
        temperaturePlaceholder: "e.g. 37.5",
        heartRate: "Heart Rate (BPM)",
        heartRatePlaceholder: "e.g. 80",
        spo2: "SpO₂ (%)",
        spo2Placeholder: "e.g. 98",
        respiratoryRate: "Respiratory Rate (/min)",
        respiratoryRatePlaceholder: "e.g. 18",
        systolicBp: "Systolic BP (mmHg)",
        systolicBpPlaceholder: "e.g. 120",
        diastolicBp: "Diastolic BP (mmHg)",
        diastolicBpPlaceholder: "e.g. 80",

        medicalHistory: "Medical History & Additional Information",
        medicalHistoryDesc: "Optional information that may help the AI-assisted assessment",
        diabetes: "Diabetes",
        hypertension: "Hypertension",
        asthma: "Asthma",
        heartDisease: "Heart Disease",
        previousHospitalization: "Previous Hospitalization",
        select: "Select",
        yes: "Yes",
        no: "No",
        unknown: "Unknown",
        painLevel: "Pain Level (0–10)",
        painPlaceholder: "e.g. 4",
        symptomDuration: "Symptom Duration (days)",
        durationPlaceholder: "e.g. 3",
        medicationCount: "Number of Medications",
        medicationPlaceholder: "e.g. 2",

        uploadSupporting: "Upload Supporting Information",
        uploadDesc: "Optional: Add an image, prescription or medical report.",
        uploadImage: "Upload Image",
        imageDesc: "Injury, rash, swelling or other visible symptoms",
        chooseImage: "Choose image",
        medicalReport: "Medical Report",
        reportDesc: "Upload a prescription or medical report",
        chooseFile: "Choose file",
        uploadNote: "You may upload one image or one medical report.",

        consent: "I consent to my submitted information being processed for AI-assisted triage and reviewed by healthcare staff.",

        analyze: "Analyze Case",

        important: "⚠️ Important:",
        disclaimer: "HealthTriage provides AI-assisted triage support and is not a diagnosis. A healthcare professional has the final decision."
    },

    hi: {
        patientAssessment: "मरीज़ का आकलन",
        logout: "लॉगआउट",
        badge: "AI-सहायता प्राप्त ट्रायेज",
        heading: "हमें बताएं कि आप कैसा महसूस कर रहे हैं",
        intro: "नीचे दी गई जानकारी प्रदान करें ताकि हमारी प्रणाली स्वास्थ्य कर्मचारियों को आपकी प्राथमिकता का आकलन करने में सहायता कर सके।",

        patientDetails: "मरीज़ की जानकारी",
        patientDetailsDesc: "मरीज़ की मूल जानकारी",
        patientName: "मरीज़ का नाम",
        patientNamePlaceholder: "मरीज़ का नाम दर्ज करें",
        age: "उम्र",
        agePlaceholder: "उम्र दर्ज करें",
        gender: "लिंग",
        selectGender: "लिंग चुनें",
        female: "महिला",
        male: "पुरुष",
        other: "अन्य",
        preferNot: "बताना पसंद नहीं",
        existingConditions: "मौजूदा बीमारियाँ",
        conditionsPlaceholder: "जैसे मधुमेह, अस्थमा",

        symptoms: "अपने लक्षण बताएं",
        symptomsDesc: "आप जो महसूस कर रहे हैं उसे अपने शब्दों में लिखें।",
        symptomsPlaceholder: "उदाहरण: मुझे दो दिनों से बुखार और खांसी है...",
        speak: "🎙️ बोलें",
        symptomNote: "आप अपने लक्षण सामान्य तरीके से बता सकते हैं।",

        vitals: "महत्वपूर्ण संकेत",
        vitalsDesc: "यदि उपलब्ध हों तो वैकल्पिक चिकित्सीय माप",
        vitalsNote: "महत्वपूर्ण संकेत केवल तभी दर्ज करें जब उन्हें मापा गया हो। उपलब्ध न होने पर खाली छोड़ दें।",
        temperature: "तापमान (°C)",
        temperaturePlaceholder: "जैसे 37.5",
        heartRate: "हृदय गति (BPM)",
        heartRatePlaceholder: "जैसे 80",
        spo2: "SpO₂ (%)",
        spo2Placeholder: "जैसे 98",
        respiratoryRate: "श्वसन दर (/मिनट)",
        respiratoryRatePlaceholder: "जैसे 18",
        systolicBp: "सिस्टोलिक BP (mmHg)",
        systolicBpPlaceholder: "जैसे 120",
        diastolicBp: "डायस्टोलिक BP (mmHg)",
        diastolicBpPlaceholder: "जैसे 80",

        medicalHistory: "चिकित्सीय इतिहास और अतिरिक्त जानकारी",
        medicalHistoryDesc: "वैकल्पिक जानकारी जो AI-सहायता प्राप्त आकलन में मदद कर सकती है",
        diabetes: "मधुमेह",
        hypertension: "उच्च रक्तचाप",
        asthma: "अस्थमा",
        heartDisease: "हृदय रोग",
        previousHospitalization: "पिछली अस्पताल भर्ती",
        select: "चुनें",
        yes: "हाँ",
        no: "नहीं",
        unknown: "पता नहीं",
        painLevel: "दर्द का स्तर (0–10)",
        painPlaceholder: "जैसे 4",
        symptomDuration: "लक्षणों की अवधि (दिन)",
        durationPlaceholder: "जैसे 3",
        medicationCount: "दवाओं की संख्या",
        medicationPlaceholder: "जैसे 2",

        uploadSupporting: "सहायक जानकारी अपलोड करें",
        uploadDesc: "वैकल्पिक: कोई चित्र, प्रिस्क्रिप्शन या मेडिकल रिपोर्ट जोड़ें।",
        uploadImage: "चित्र अपलोड करें",
        imageDesc: "चोट, दाने, सूजन या अन्य दिखाई देने वाले लक्षण",
        chooseImage: "चित्र चुनें",
        medicalReport: "मेडिकल रिपोर्ट",
        reportDesc: "प्रिस्क्रिप्शन या मेडिकल रिपोर्ट अपलोड करें",
        chooseFile: "फ़ाइल चुनें",
        uploadNote: "आप एक चित्र या एक मेडिकल रिपोर्ट अपलोड कर सकते हैं।",

        consent: "मैं सहमति देता/देती हूँ कि मेरी दी गई जानकारी को AI-सहायता प्राप्त ट्रायेज के लिए संसाधित किया जा सकता है और स्वास्थ्य कर्मचारियों द्वारा इसकी समीक्षा की जा सकती है।",

        analyze: "केस का विश्लेषण करें",

        important: "⚠️ महत्वपूर्ण:",
        disclaimer: "HealthTriage AI-सहायता प्राप्त ट्रायेज सहायता प्रदान करता है और यह कोई निदान नहीं है। अंतिम निर्णय स्वास्थ्य पेशेवर का होगा।"
    },

    or: {
        patientAssessment: "ରୋଗୀ ମୂଲ୍ୟାଙ୍କନ",
        logout: "ଲଗ୍ ଆଉଟ୍",
        badge: "AI-ସହାୟିତ ଟ୍ରାଏଜ୍",
        heading: "ଆପଣ କିପରି ଅନୁଭବ କରୁଛନ୍ତି ଆମକୁ କୁହନ୍ତୁ",
        intro: "ନିମ୍ନରେ ଦିଆଯାଇଥିବା ସୂଚନା ପ୍ରଦାନ କରନ୍ତୁ, ଯାହାଦ୍ୱାରା ଆମ ସିଷ୍ଟମ୍ ସ୍ୱାସ୍ଥ୍ୟକର୍ମୀଙ୍କୁ ଆପଣଙ୍କ ଜରୁରୀକତା ମୂଲ୍ୟାଙ୍କନରେ ସାହାଯ୍ୟ କରିପାରିବ।",

        patientDetails: "ରୋଗୀଙ୍କ ସୂଚନା",
        patientDetailsDesc: "ରୋଗୀଙ୍କ ମୌଳିକ ସୂଚନା",
        patientName: "ରୋଗୀଙ୍କ ନାମ",
        patientNamePlaceholder: "ରୋଗୀଙ୍କ ନାମ ଲେଖନ୍ତୁ",
        age: "ବୟସ",
        agePlaceholder: "ବୟସ ଲେଖନ୍ତୁ",
        gender: "ଲିଙ୍ଗ",
        selectGender: "ଲିଙ୍ଗ ବାଛନ୍ତୁ",
        female: "ମହିଳା",
        male: "ପୁରୁଷ",
        other: "ଅନ୍ୟ",
        preferNot: "କହିବାକୁ ଚାହୁଁନାହିଁ",
        existingConditions: "ବର୍ତ୍ତମାନ ଥିବା ରୋଗ",
        conditionsPlaceholder: "ଯଥା ମଧୁମେହ, ଆସ୍ଥମା",

        symptoms: "ଆପଣଙ୍କ ଲକ୍ଷଣ ବର୍ଣ୍ଣନା କରନ୍ତୁ",
        symptomsDesc: "ଆପଣ କ’ଣ ଅନୁଭବ କରୁଛନ୍ତି ନିଜ ଶବ୍ଦରେ ଲେଖନ୍ତୁ।",
        symptomsPlaceholder: "ଉଦାହରଣ: ମୋର ଦୁଇ ଦିନ ହେଲା ଜ୍ୱର ଏବଂ କାଶ ହେଉଛି...",
        speak: "🎙️ କୁହନ୍ତୁ",
        symptomNote: "ଆପଣ ସାଧାରଣ ଭାବରେ ନିଜ ଲକ୍ଷଣ ବର୍ଣ୍ଣନା କରିପାରିବେ।",

        vitals: "ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ସଙ୍କେତ",
        vitalsDesc: "ଉପଲବ୍ଧ ଥିଲେ ବୈକଳ୍ପିକ ଚିକିତ୍ସା ମାପ",
        vitalsNote: "କେବଳ ମାପ କରାଯାଇଥିଲେ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ସଙ୍କେତ ଦିଅନ୍ତୁ। ଉପଲବ୍ଧ ନଥିଲେ ଖାଲି ରଖନ୍ତୁ।",
        temperature: "ତାପମାତ୍ରା (°C)",
        temperaturePlaceholder: "ଯଥା 37.5",
        heartRate: "ହୃଦ୍‌ସ୍ପନ୍ଦନ ହାର (BPM)",
        heartRatePlaceholder: "ଯଥା 80",
        spo2: "SpO₂ (%)",
        spo2Placeholder: "ଯଥା 98",
        respiratoryRate: "ଶ୍ୱାସ ପ୍ରଶ୍ୱାସ ହାର (/ମିନିଟ୍)",
        respiratoryRatePlaceholder: "ଯଥା 18",
        systolicBp: "ସିଷ୍ଟୋଲିକ୍ BP (mmHg)",
        systolicBpPlaceholder: "ଯଥା 120",
        diastolicBp: "ଡାଏଷ୍ଟୋଲିକ୍ BP (mmHg)",
        diastolicBpPlaceholder: "ଯଥା 80",

        medicalHistory: "ଚିକିତ୍ସା ଇତିହାସ ଏବଂ ଅତିରିକ୍ତ ସୂଚନା",
        medicalHistoryDesc: "AI-ସହାୟିତ ମୂଲ୍ୟାଙ୍କନରେ ସାହାଯ୍ୟ କରିପାରୁଥିବା ବୈକଳ୍ପିକ ସୂଚନା",
        diabetes: "ମଧୁମେହ",
        hypertension: "ଉଚ୍ଚ ରକ୍ତଚାପ",
        asthma: "ଆସ୍ଥମା",
        heartDisease: "ହୃଦ୍‌ରୋଗ",
        previousHospitalization: "ପୂର୍ବରୁ ହସ୍ପିଟାଲରେ ଭର୍ତ୍ତି",
        select: "ବାଛନ୍ତୁ",
        yes: "ହଁ",
        no: "ନା",
        unknown: "ଜଣାନାହିଁ",
        painLevel: "ଯନ୍ତ୍ରଣାର ସ୍ତର (0–10)",
        painPlaceholder: "ଯଥା 4",
        symptomDuration: "ଲକ୍ଷଣର ଅବଧି (ଦିନ)",
        durationPlaceholder: "ଯଥା 3",
        medicationCount: "ଔଷଧ ସଂଖ୍ୟା",
        medicationPlaceholder: "ଯଥା 2",

        uploadSupporting: "ସହାୟକ ସୂଚନା ଅପଲୋଡ୍ କରନ୍ତୁ",
        uploadDesc: "ବୈକଳ୍ପିକ: ଏକ ଚିତ୍ର, ପ୍ରେସକ୍ରିପସନ୍ କିମ୍ବା ମେଡିକାଲ୍ ରିପୋର୍ଟ ଯୋଡନ୍ତୁ।",
        uploadImage: "ଚିତ୍ର ଅପଲୋଡ୍ କରନ୍ତୁ",
        imageDesc: "ଚୋଟ, ଚର୍ମରେ ଦାଗ, ଫୁଲା କିମ୍ବା ଅନ୍ୟ ଦୃଶ୍ୟମାନ ଲକ୍ଷଣ",
        chooseImage: "ଚିତ୍ର ବାଛନ୍ତୁ",
        medicalReport: "ମେଡିକାଲ୍ ରିପୋର୍ଟ",
        reportDesc: "ପ୍ରେସକ୍ରିପସନ୍ କିମ୍ବା ମେଡିକାଲ୍ ରିପୋର୍ଟ ଅପଲୋଡ୍ କରନ୍ତୁ",
        chooseFile: "ଫାଇଲ୍ ବାଛନ୍ତୁ",
        uploadNote: "ଆପଣ ଗୋଟିଏ ଚିତ୍ର କିମ୍ବା ଗୋଟିଏ ମେଡିକାଲ୍ ରିପୋର୍ଟ ଅପଲୋଡ୍ କରିପାରିବେ।",

        consent: "ମୁଁ ସମ୍ମତି ଦେଉଛି ଯେ ମୋ ଦ୍ୱାରା ଦିଆଯାଇଥିବା ସୂଚନା AI-ସହାୟିତ ଟ୍ରାଏଜ୍ ପାଇଁ ପ୍ରକ୍ରିୟାକରଣ କରାଯାଇପାରେ ଏବଂ ସ୍ୱାସ୍ଥ୍ୟକର୍ମୀଙ୍କ ଦ୍ୱାରା ସମୀକ୍ଷା କରାଯାଇପାରେ।",

        analyze: "କେସ୍ ବିଶ୍ଳେଷଣ କରନ୍ତୁ",

        important: "⚠️ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ:",
        disclaimer: "HealthTriage AI-ସହାୟିତ ଟ୍ରାଏଜ୍ ସହାୟତା ପ୍ରଦାନ କରେ ଏବଂ ଏହା କୌଣସି ରୋଗ ନିର୍ଣ୍ଣୟ ନୁହେଁ। ଅନ୍ତିମ ନିଷ୍ପତ୍ତି ସ୍ୱାସ୍ଥ୍ୟ ପେଶାଦାରଙ୍କର ହେବ।"
    }
};


function applyLanguage(language) {

    const t = translations[language];

    if (!t) return;

    document.documentElement.lang = language;

    const setText = (selector, value) => {
        const element = document.querySelector(selector);
        if (element) {
            element.textContent = value;
        }
    };

    const setPlaceholder = (selector, value) => {
        const element = document.querySelector(selector);
        if (element) {
            element.placeholder = value;
        }
    };

    // Header
    setText(".header-right span", t.patientAssessment);

    const logoutButton = document.querySelector(".header-right button");
    if (logoutButton) {
        logoutButton.textContent = t.logout;
    }

    // Heading
    setText(".page-badge", t.badge);
    setText(".assessment-heading h1", t.heading);
    setText(".assessment-heading p", t.intro);

    // Section 01
    setText(".form-section:nth-of-type(1) .section-title h2", t.patientDetails);
    setText(".form-section:nth-of-type(1) .section-title p", t.patientDetailsDesc);

    setText('label[for="patientName"]', t.patientName);
    setPlaceholder("#patientName", t.patientNamePlaceholder);

    setText('label[for="age"]', t.age);
    setPlaceholder("#age", t.agePlaceholder);

    setText('label[for="gender"]', t.gender);
    setText('#gender option[value=""]', t.selectGender);
    setText('#gender option[value="female"]', t.female);
    setText('#gender option[value="male"]', t.male);
    setText('#gender option[value="other"]', t.other);
    setText('#gender option[value="prefer_not"]', t.preferNot);

    setText('label[for="conditions"]', t.existingConditions);
    setPlaceholder("#conditions", t.conditionsPlaceholder);

    // Section 02
    setText(".form-section:nth-of-type(2) .section-title h2", t.symptoms);
    setText(".form-section:nth-of-type(2) .section-title p", t.symptomsDesc);
    setPlaceholder("#symptoms", t.symptomsPlaceholder);
    setText("#voiceButton", t.speak);

    const symptomNote = document.querySelector("#voiceButton + .tool-note");
    if (symptomNote) symptomNote.textContent = t.symptomNote;

    // Section 03
    setText(".form-section:nth-of-type(3) .section-title h2", t.vitals);
    setText(".form-section:nth-of-type(3) .section-title p", t.vitalsDesc);

    const vitalsNote = document.querySelector(".form-section:nth-of-type(3) > .tool-note");
    if (vitalsNote) vitalsNote.textContent = t.vitalsNote;

    setText('label[for="temperature"]', t.temperature);
    setPlaceholder("#temperature", t.temperaturePlaceholder);

    setText('label[for="heartRate"]', t.heartRate);
    setPlaceholder("#heartRate", t.heartRatePlaceholder);

    setText('label[for="spo2"]', t.spo2);
    setPlaceholder("#spo2", t.spo2Placeholder);

    setText('label[for="respiratoryRate"]', t.respiratoryRate);
    setPlaceholder("#respiratoryRate", t.respiratoryRatePlaceholder);

    setText('label[for="systolicBp"]', t.systolicBp);
    setPlaceholder("#systolicBp", t.systolicBpPlaceholder);

    setText('label[for="diastolicBp"]', t.diastolicBp);
    setPlaceholder("#diastolicBp", t.diastolicBpPlaceholder);

    // Section 04
    setText(".form-section:nth-of-type(4) .section-title h2", t.medicalHistory);
    setText(".form-section:nth-of-type(4) .section-title p", t.medicalHistoryDesc);

    setText('label[for="diabetesHistory"]', t.diabetes);
    setText('label[for="hypertensionHistory"]', t.hypertension);
    setText('label[for="asthmaHistory"]', t.asthma);
    setText('label[for="heartDiseaseHistory"]', t.heartDisease);
    setText('label[for="previousHospitalization"]', t.previousHospitalization);

    [
        "#diabetesHistory",
        "#hypertensionHistory",
        "#asthmaHistory",
        "#heartDiseaseHistory",
        "#previousHospitalization"
    ].forEach(selector => {
        setText(`${selector} option[value=""]`, t.select);
        setText(`${selector} option[value="yes"]`, t.yes);
        setText(`${selector} option[value="no"]`, t.no);
        setText(`${selector} option[value="unknown"]`, t.unknown);
    });

    setText('label[for="painLevel"]', t.painLevel);
    setPlaceholder("#painLevel", t.painPlaceholder);

    setText('label[for="symptomDuration"]', t.symptomDuration);
    setPlaceholder("#symptomDuration", t.durationPlaceholder);

    setText('label[for="medicationCount"]', t.medicationCount);
    setPlaceholder("#medicationCount", t.medicationPlaceholder);

    // Section 05
    setText(".form-section:nth-of-type(5) .section-title h2", t.uploadSupporting);
    setText(".form-section:nth-of-type(5) .section-title p", t.uploadDesc);

    const uploadCards = document.querySelectorAll(".upload-card");

    if (uploadCards.length >= 2) {

        setText(".upload-card:nth-of-type(1) h3", t.uploadImage);
        setText(".upload-card:nth-of-type(1) p", t.imageDesc);
        setText(".upload-card:nth-of-type(1) .upload-link", t.chooseImage);

        setText(".upload-card:nth-of-type(2) h3", t.medicalReport);
        setText(".upload-card:nth-of-type(2) p", t.reportDesc);
        setText(".upload-card:nth-of-type(2) .upload-link", t.chooseFile);
    }

    setText("#uploadNote", t.uploadNote);

    // Consent
    const consentText = document.querySelector(".consent-label span");
    if (consentText) {
        consentText.textContent = t.consent;
    }

    // Submit
    setText("#analyzeButton", t.analyze);

    // Disclaimer
    const disclaimer = document.querySelector(".disclaimer");

    if (disclaimer) {
        disclaimer.innerHTML =
            `${t.important} <strong>${t.disclaimer}</strong>`;
    }

    // Save selected language
    localStorage.setItem("healthtriage_language", language);
}


document.addEventListener("DOMContentLoaded", () => {

    const languageSelect = document.getElementById("languageSelect");

    if (!languageSelect) return;

    const savedLanguage =
        localStorage.getItem("healthtriage_language") || "en";

    languageSelect.value = savedLanguage;

    applyLanguage(savedLanguage);

    languageSelect.addEventListener("change", () => {
        applyLanguage(languageSelect.value);
    });
});