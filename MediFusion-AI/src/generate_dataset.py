import pandas as pd
import numpy as np
import os

# ============================================================
# MediFusion AI - Advanced Synthetic Patient Dataset
# ============================================================

# Reproducibility
np.random.seed(42)

# Number of synthetic patients
N = 5000

# ------------------------------------------------------------
# 1. Basic patient information
# ------------------------------------------------------------

patient_id = [f"P{10000 + i}" for i in range(N)]

age = np.random.randint(1, 91, N)

sex = np.random.choice(
    ["Male", "Female"],
    size=N
)

# ------------------------------------------------------------
# 2. Vital signs
# ------------------------------------------------------------

temperature = np.round(
    np.clip(np.random.normal(37.0, 0.8, N), 35.5, 41.0),
    1
)

heart_rate = np.clip(
    np.random.normal(82, 18, N).astype(int),
    45,
    160
)

spo2 = np.clip(
    np.random.normal(97, 2.5, N).round(1),
    80,
    100
)

respiratory_rate = np.clip(
    np.random.normal(18, 5, N).astype(int),
    8,
    45
)

systolic_bp = np.clip(
    np.random.normal(120, 20, N).astype(int),
    70,
    200
)

diastolic_bp = np.clip(
    np.random.normal(78, 12, N).astype(int),
    40,
    130
)

# ------------------------------------------------------------
# 3. Symptoms
# ------------------------------------------------------------

fever = np.random.binomial(1, 0.25, N)

cough = np.random.binomial(1, 0.25, N)

headache = np.random.binomial(1, 0.20, N)

vomiting = np.random.binomial(1, 0.15, N)

diarrhea = np.random.binomial(1, 0.10, N)

fatigue = np.random.binomial(1, 0.25, N)

abdominal_pain = np.random.binomial(1, 0.12, N)

dizziness = np.random.binomial(1, 0.18, N)

chest_pain = np.random.binomial(1, 0.10, N)

breathing_difficulty = np.random.binomial(1, 0.12, N)

# ------------------------------------------------------------
# 4. Medical history
# ------------------------------------------------------------

diabetes_history = np.random.binomial(1, 0.15, N)

hypertension_history = np.random.binomial(1, 0.20, N)

asthma_history = np.random.binomial(1, 0.08, N)

heart_disease_history = np.random.binomial(1, 0.07, N)

previous_hospitalization = np.random.binomial(1, 0.12, N)

# ------------------------------------------------------------
# 5. Other patient information
# ------------------------------------------------------------

pain_level = np.random.randint(0, 11, N)

symptom_duration_days = np.random.randint(0, 15, N)

medication_count = np.random.randint(0, 7, N)

# ------------------------------------------------------------
# 6. Medical history summary
# ------------------------------------------------------------

medical_history = (
    diabetes_history
    + hypertension_history
    + asthma_history
    + heart_disease_history
    + previous_hospitalization
)

# Convert to 0/1
medical_history = (medical_history > 0).astype(int)

# ------------------------------------------------------------
# 7. Synthetic triage scoring
# ------------------------------------------------------------
# IMPORTANT:
# These are ONLY synthetic prototype rules.
# They are NOT clinical guidelines or medical thresholds.

risk_score = np.zeros(N)

# Vital-sign related synthetic scoring

risk_score += np.where(spo2 < 92, 4, 0)
risk_score += np.where(spo2 < 95, 2, 0)

risk_score += np.where(heart_rate > 120, 3, 0)
risk_score += np.where(heart_rate > 100, 1, 0)

risk_score += np.where(respiratory_rate > 28, 3, 0)
risk_score += np.where(respiratory_rate > 22, 1, 0)

risk_score += np.where(temperature > 39, 2, 0)
risk_score += np.where(temperature > 38, 1, 0)

risk_score += np.where(systolic_bp < 90, 3, 0)
risk_score += np.where(systolic_bp > 180, 2, 0)

# Symptom-related synthetic scoring

risk_score += breathing_difficulty * 4
risk_score += chest_pain * 4
risk_score += dizziness * 1
risk_score += vomiting * 1
risk_score += fever * 1
risk_score += fatigue * 1

# Medical-history-related synthetic scoring

risk_score += diabetes_history * 1
risk_score += hypertension_history * 1
risk_score += asthma_history * 1
risk_score += heart_disease_history * 2
risk_score += previous_hospitalization * 1

# Pain

risk_score += np.where(pain_level >= 8, 2, 0)
risk_score += np.where(pain_level >= 5, 1, 0)

# Age

risk_score += np.where(age >= 65, 1, 0)

# ------------------------------------------------------------
# 8. Add small synthetic variation
# ------------------------------------------------------------

risk_score += np.random.normal(0, 0.8, N)

# ------------------------------------------------------------
# 9. Create triage priority
# ------------------------------------------------------------
# These categories are generated for ML demonstration only.

triage_priority = np.where(
    risk_score >= 7,
    "HIGH",
    np.where(
        risk_score >= 3,
        "MEDIUM",
        "LOW"
    )
)

# ------------------------------------------------------------
# 10. Patient symptom text
# ------------------------------------------------------------

symptom_text = []

for i in range(N):

    symptoms = []

    if fever[i]:
        symptoms.append("fever")

    if cough[i]:
        symptoms.append("cough")

    if headache[i]:
        symptoms.append("headache")

    if vomiting[i]:
        symptoms.append("vomiting")

    if diarrhea[i]:
        symptoms.append("diarrhea")

    if fatigue[i]:
        symptoms.append("fatigue")

    if abdominal_pain[i]:
        symptoms.append("abdominal pain")

    if dizziness[i]:
        symptoms.append("dizziness")

    if chest_pain[i]:
        symptoms.append("chest pain")

    if breathing_difficulty[i]:
        symptoms.append("breathing difficulty")

    if len(symptoms) == 0:
        symptoms.append("no major symptoms reported")

    symptom_text.append(", ".join(symptoms))

# ------------------------------------------------------------
# 11. Create medication information
# ------------------------------------------------------------

medication_history = []

for count in medication_count:

    if count == 0:
        medication_history.append("No regular medication reported")
    else:
        medication_history.append(
            f"{count} medication(s) reported"
        )

# ------------------------------------------------------------
# 12. Create dataset
# ------------------------------------------------------------

data = pd.DataFrame({

    "patient_id": patient_id,

    "age": age,

    "sex": sex,

    "temperature": temperature,

    "heart_rate": heart_rate,

    "spo2": spo2,

    "respiratory_rate": respiratory_rate,

    "systolic_bp": systolic_bp,

    "diastolic_bp": diastolic_bp,

    "fever": fever,

    "cough": cough,

    "headache": headache,

    "vomiting": vomiting,

    "diarrhea": diarrhea,

    "fatigue": fatigue,

    "abdominal_pain": abdominal_pain,

    "dizziness": dizziness,

    "chest_pain": chest_pain,

    "breathing_difficulty": breathing_difficulty,

    "diabetes_history": diabetes_history,

    "hypertension_history": hypertension_history,

    "asthma_history": asthma_history,

    "heart_disease_history": heart_disease_history,

    "previous_hospitalization": previous_hospitalization,

    "pain_level": pain_level,

    "symptom_duration_days": symptom_duration_days,

    "medication_count": medication_count,

    "medical_history": medical_history,

    "symptom_text": symptom_text,

    "medication_history": medication_history,

    "triage_priority": triage_priority
})

# ------------------------------------------------------------
# 13. Save dataset
# ------------------------------------------------------------

output_folder = "Data/raw"

os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(
    output_folder,
    "synthetic_patient_data.csv"
)

data.to_csv(output_file, index=False)

# ------------------------------------------------------------
# 14. Display information
# ------------------------------------------------------------

print("\n==============================================")
print("MediFusion AI - Dataset Generation Complete")
print("==============================================")

print("\nDataset shape:")
print(data.shape)

print("\nColumns:")
print(list(data.columns))

print("\nFirst 5 records:")
print(data.head())

print("\nTriage class distribution:")
print(data["triage_priority"].value_counts())

print("\nDataset saved successfully!")
print(f"Location: {output_file}")

print("\nNOTE:")
print("This dataset contains synthetic/demo data.")
print("The triage labels are generated using prototype")
print("rules and are NOT clinical guidelines.")