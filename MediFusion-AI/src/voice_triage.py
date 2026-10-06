import pandas as pd
import joblib

from symptom_extractor import extract_symptoms


# ---------------------------------------
# 1. Load trained model
# ---------------------------------------

model_path = "model/structured_triage_model.pkl"

model = joblib.load(model_path)

print("\nStructured triage model loaded successfully!")


# ---------------------------------------
# 2. Get patient information
# ---------------------------------------

print("\n========================================")
print("       PATIENT INFORMATION")
print("========================================")

age = int(input("Age: "))

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
# 3. Get vital signs
# ---------------------------------------

print("\nEnter vital signs:")

temperature = float(input("Temperature: "))
heart_rate = int(input("Heart rate: "))
spo2 = int(input("SpO2: "))
respiratory_rate = int(input("Respiratory rate: "))
systolic_bp = int(input("Systolic BP: "))
diastolic_bp = int(input("Diastolic BP: "))


# ---------------------------------------
# 4. Get medical history
# ---------------------------------------

print("\nMedical history")

diabetes_history = int(input("Diabetes history (0/1): "))
hypertension_history = int(input("Hypertension history (0/1): "))
asthma_history = int(input("Asthma history (0/1): "))
heart_disease_history = int(input("Heart disease history (0/1): "))
previous_hospitalization = int(
    input("Previous hospitalization (0/1): ")
)


# ---------------------------------------
# 5. Other structured information
# ---------------------------------------

pain_level = int(input("\nPain level (0-10): "))
symptom_duration_days = int(
    input("Symptom duration in days: ")
)
medication_count = int(
    input("Number of current medications: ")
)


# ---------------------------------------
# 6. Get English voice transcript
# ---------------------------------------

print("\n========================================")
print("       ENGLISH PATIENT STATEMENT")
print("========================================")

voice_text = input(
    "\nPaste the English Whisper transcript here:\n"
)


# ---------------------------------------
# 7. Extract symptoms from voice
# ---------------------------------------

symptoms = extract_symptoms(voice_text)

print("\nExtracted symptoms:")

for symptom, value in symptoms.items():
    print(f"{symptom}: {value}")


# ---------------------------------------
# 8. Create 26-feature input
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

    "fever": symptoms["fever"],
    "cough": symptoms["cough"],
    "headache": symptoms["headache"],
    "vomiting": symptoms["vomiting"],
    "diarrhea": symptoms["diarrhea"],
    "fatigue": symptoms["fatigue"],
    "abdominal_pain": symptoms["abdominal_pain"],
    "dizziness": symptoms["dizziness"],
    "chest_pain": symptoms["chest_pain"],
    "breathing_difficulty": symptoms["breathing_difficulty"],

    "diabetes_history": diabetes_history,
    "hypertension_history": hypertension_history,
    "asthma_history": asthma_history,
    "heart_disease_history": heart_disease_history,
    "previous_hospitalization": previous_hospitalization,

    "pain_level": pain_level,
    "symptom_duration_days": symptom_duration_days,
    "medication_count": medication_count
}


# ---------------------------------------
# 9. Convert to DataFrame
# ---------------------------------------

input_data = pd.DataFrame([patient_data])


# ---------------------------------------
# 10. Predict triage priority
# ---------------------------------------

prediction = model.predict(input_data)[0]

print("\n========================================")
print("       TRIAGE RESULT")
print("========================================")

print("\nPredicted priority:", prediction)

print("\n========================================")
print("Prototype result for demonstration only.")
print("Not a medical diagnosis.")
print("========================================")