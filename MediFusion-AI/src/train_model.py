import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ---------------------------------------
# 1. Load Dataset
# ---------------------------------------

data_path = "Data/raw/synthetic_patient_data.csv"

df = pd.read_csv(data_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ---------------------------------------
# 2. Select Structured Features
# ---------------------------------------

features = [
    "age",
    "sex",
    "temperature",
    "heart_rate",
    "spo2",
    "respiratory_rate",
    "systolic_bp",
    "diastolic_bp",
    "fever",
    "cough",
    "headache",
    "vomiting",
    "diarrhea",
    "fatigue",
    "abdominal_pain",
    "dizziness",
    "chest_pain",
    "breathing_difficulty",
    "diabetes_history",
    "hypertension_history",
    "asthma_history",
    "heart_disease_history",
    "previous_hospitalization",
    "pain_level",
    "symptom_duration_days",
    "medication_count"
]

target = "triage_priority"


# ---------------------------------------
# 3. Prepare Data
# ---------------------------------------

X = df[features].copy()
y = df[target]


# Convert sex into numerical values
X["sex"] = X["sex"].map({
    "Male": 0,
    "Female": 1,
    "Other": 2
})


# ---------------------------------------
# 4. Train-Test Split
# ---------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ---------------------------------------
# 5. Train Random Forest
# ---------------------------------------

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    max_depth=12,
    min_samples_split=5
)

model.fit(X_train, y_train)

print("Model training completed!")


# ---------------------------------------
# 6. Model Evaluation
# ---------------------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n========================================")
print("        MODEL PERFORMANCE")
print("========================================")

print("\nAccuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ---------------------------------------
# 7. Save Model
# ---------------------------------------

model_folder = "model"

os.makedirs(model_folder, exist_ok=True)

model_path = os.path.join(
    model_folder,
    "structured_triage_model.pkl"
)

joblib.dump(model, model_path)

print("\nModel saved successfully!")
print("Saved at:", model_path)

print("\n========================================")
print("       TRAINING COMPLETED")
print("========================================")