
import sounddevice as sd
import scipy.io.wavfile as wav
import os
import torch
import torchaudio
from transformers import AutoModel
from symptom_extractor import extract_symptoms

# ---------------------------------------
# 1. Settings
# ---------------------------------------

SAMPLE_RATE = 16000
RECORD_SECONDS = 30

audio_folder = "Data/raw/audio"
os.makedirs(audio_folder, exist_ok=True)

audio_path = os.path.join(audio_folder, "patient_voice.wav")


# ---------------------------------------
# 2. Available Languages
# ---------------------------------------

languages = {
    "1": ("English", "en"),
    "2": ("Hindi", "hi"),
    "3": ("Odia", "or"),
    "4": ("Bengali", "bn"),
    "5": ("Telugu", "te"),
    "6": ("Tamil", "ta"),
    "7": ("Marathi", "mr"),
    "8": ("Gujarati", "gu"),
    "9": ("Kannada", "kn"),
    "10": ("Malayalam", "ml"),
    "11": ("Punjabi", "pa"),
    "12": ("Urdu", "ur"),
    "13": ("Assamese", "as")
}


# ---------------------------------------
# 3. Display Language Menu
# ---------------------------------------

print("\n========================================")
print("       MEDIFUSION-AI")
print("       PATIENT VOICE INPUT")
print("========================================")

print("\nPlease select your language:\n")

for number, (language_name, _) in languages.items():
    print(f"{number}. {language_name}")


# ---------------------------------------
# 4. Get Language Choice
# ---------------------------------------

while True:

    choice = input("\nEnter your language choice: ")

    if choice in languages:
        selected_language, language_code = languages[choice]
        break

    print("Invalid choice. Please select a number from the list.")


print("\nSelected language:", selected_language)


# ---------------------------------------
# 5. Load Speech Recognition Model
# ---------------------------------------

if language_code == "en":

    print("\nLoading Whisper model for English...")

    import whisper

    whisper_model = whisper.load_model("base")

    print("Whisper model loaded successfully!")

else:

    print("\nLoading AI4Bharat IndicConformer model...")

    indic_model = AutoModel.from_pretrained(
        "ai4bharat/indic-conformer-600m-multilingual",
        trust_remote_code=True
    )

    print("IndicConformer model loaded successfully!")

# ---------------------------------------
# 6. Record Patient's Voice
# ---------------------------------------

print("\n========================================")
print("       VOICE RECORDING")
print("========================================")

print(f"\nRecording for {RECORD_SECONDS} seconds...")
print(f"Please speak in {selected_language}.")
print("You can describe your symptoms naturally.")

input_device = None

for i, device_info in enumerate(sd.query_devices()):
    if (
        "Microphone Array" in device_info["name"]
        and device_info["max_input_channels"] > 0
    ):
        input_device = i
        print("Using microphone:", device_info["name"])
        print("Device index:", input_device)
        break

if input_device is None:
    raise RuntimeError("No microphone found.")

audio = sd.rec(
    int(RECORD_SECONDS * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16",
    device=input_device
    
    
)

sd.wait()

print("\nRecording completed!")


# ---------------------------------------
# 7. Save Audio
# ---------------------------------------

wav.write(audio_path, SAMPLE_RATE, audio)

print("Audio saved at:", audio_path)


# ---------------------------------------
# 8. Convert Speech to Text
# ---------------------------------------

print("\nAnalyzing patient's voice...")
print("Please wait...")

if language_code == "en":

    # English → Whisper
    result = whisper_model.transcribe(
        audio_path,
        fp16=False
    )

    transcribed_text = result["text"]

else:

    # Indian languages → AI4Bharat IndicConformer

    sample_rate, audio_data = wav.read(audio_path)

    audio_tensor = torch.from_numpy(audio_data).float()

    # Convert stereo to mono if necessary
    if audio_tensor.ndim > 1:
        audio_tensor = audio_tensor.mean(dim=1)

    # Normalize int16 audio to approximately [-1, 1]
    audio_tensor = audio_tensor / 32768.0

    # Add batch/channel dimension
    audio_tensor = audio_tensor.unsqueeze(0)

    # The recording is already 16 kHz,
    # but keep this check for safety.
    if sample_rate != 16000:
        audio_tensor = torchaudio.functional.resample(
            audio_tensor,
            sample_rate,
            16000
        )

    # Run IndicConformer
    transcribed_text = indic_model(
        audio_tensor,
        language_code,
        "ctc"
    )

# ---------------------------------------
# 9. Display Result
# ---------------------------------------




print("\n========================================")
print("       VOICE ANALYSIS RESULT")
print("========================================")

print("\nSelected language:", selected_language)

print("\nPatient said:")
print(transcribed_text)


# ---------------------------------------
# 10. Extract Structured Symptoms
# ---------------------------------------

if language_code == "en":

    structured_symptoms = extract_symptoms(transcribed_text)

    print("\n========================================")
    print("       STRUCTURED SYMPTOMS")
    print("========================================")

    for symptom, value in structured_symptoms.items():
        print(f"{symptom}: {value}")


    # ---------------------------------------
    # 11. Patient Information
    # ---------------------------------------

    print("\n========================================")
    print("       PATIENT INFORMATION")
    print("========================================")

    age = int(input("\nAge: "))

    print("\nSex:")
    print("1. Male")
    print("2. Female")
    print("3. Other")

    sex_choice = input("Choose: ")

    sex_map = {
        "1": 0,
        "2": 1,
        "3": 2
    }

    sex = sex_map.get(sex_choice, 2)


    # ---------------------------------------
    # 12. Vital Signs
    # ---------------------------------------

    print("\nEnter vital signs:")

    temperature = float(input("Temperature: "))
    heart_rate = int(input("Heart rate: "))
    spo2 = int(input("SpO2: "))
    respiratory_rate = int(input("Respiratory rate: "))
    systolic_bp = int(input("Systolic BP: "))
    diastolic_bp = int(input("Diastolic BP: "))


    # ---------------------------------------
    # 13. Medical History
    # ---------------------------------------

    print("\nMedical history")

    diabetes_history = int(
        input("Diabetes history (0/1): ")
    )

    hypertension_history = int(
        input("Hypertension history (0/1): ")
    )

    asthma_history = int(
        input("Asthma history (0/1): ")
    )

    heart_disease_history = int(
        input("Heart disease history (0/1): ")
    )

    previous_hospitalization = int(
        input("Previous hospitalization (0/1): ")
    )


    # ---------------------------------------
    # 14. Additional Information
    # ---------------------------------------

    pain_level = int(
        input("\nPain level (0-10): ")
    )

    symptom_duration_days = int(
        input("Symptom duration in days: ")
    )

    medication_count = int(
        input("Number of current medications: ")
    )


    # ---------------------------------------
    # 15. Load Structured Model
    # ---------------------------------------

    import pandas as pd
    import joblib

    model_path = "model/structured_triage_model.pkl"

    model = joblib.load(model_path)

    print("\nStructured triage model loaded successfully!")


    # ---------------------------------------
    # 16. Create Patient Feature Data
    # ---------------------------------------

    patient_data = {

        "age": age,
        "sex": sex,

        "temperature": temperature,
        "heart_rate": heart_rate,
        "spo2": spo2,
        "respiratory_rate": respiratory_rate,
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp,

        "fever": structured_symptoms["fever"],
        "cough": structured_symptoms["cough"],
        "headache": structured_symptoms["headache"],
        "vomiting": structured_symptoms["vomiting"],
        "diarrhea": structured_symptoms["diarrhea"],
        "fatigue": structured_symptoms["fatigue"],
        "abdominal_pain": structured_symptoms["abdominal_pain"],
        "dizziness": structured_symptoms["dizziness"],
        "chest_pain": structured_symptoms["chest_pain"],
        "breathing_difficulty": structured_symptoms["breathing_difficulty"],

        "diabetes_history": diabetes_history,
        "hypertension_history": hypertension_history,
        "asthma_history": asthma_history,
        "heart_disease_history": heart_disease_history,
        "previous_hospitalization": previous_hospitalization,

        "pain_level": pain_level,
        "symptom_duration_days": symptom_duration_days,
        "medication_count": medication_count
    }


    input_data = pd.DataFrame([patient_data])


    # ---------------------------------------
# 17. Predict Triage Priority
# ---------------------------------------

prediction = model.predict(input_data)[0]

# Get model probability estimate
probabilities = model.predict_proba(input_data)[0]

confidence = max(probabilities) * 100


# ---------------------------------------
# 18. Get Top Model Features
# ---------------------------------------

feature_names = input_data.columns

feature_importance = model.feature_importances_

feature_info = list(
    zip(feature_names, feature_importance)
)

feature_info.sort(
    key=lambda x: x[1],
    reverse=True
)

top_features = feature_info[:5]


# ---------------------------------------
# 19. Display Triage Result
# ---------------------------------------

print("\n========================================")
print("          TRIAGE RESULT")
print("========================================")

print("\nPredicted priority:", prediction)

print(
    f"Model confidence estimate: "
    f"{confidence:.2f}%"
)


# ---------------------------------------
# 20. Display Detected Symptoms
# ---------------------------------------

print("\n========================================")
print("       DETECTED SYMPTOMS")
print("========================================")

detected_symptoms = [
    symptom
    for symptom, value in structured_symptoms.items()
    if value == 1
]

if detected_symptoms:

    for symptom in detected_symptoms:
        print("-", symptom)

else:

    print("- No supported symptoms detected")


# ---------------------------------------
# 21. Display Important Model Features
# ---------------------------------------

print("\n========================================")
print("       TOP MODEL FEATURES")
print("========================================")

for feature, importance in top_features:

    print(
        f"- {feature}: "
        f"{importance * 100:.2f}%"
    )


print("\n========================================")
print("Prototype result for demonstration only.")
print("Not a medical diagnosis.")
print("========================================")