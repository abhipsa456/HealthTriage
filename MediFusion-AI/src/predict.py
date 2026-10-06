import joblib
import pandas as pd

# Load trained model
model_path = "model/triage_model.pkl"
model = joblib.load(model_path)

print("\n===================================")
print("   MediFusion AI - Risk Predictor")
print("===================================\n")

# Get patient information
age = int(input("Enter age: "))
temperature = float(input("Enter temperature (°C): "))
heart_rate = int(input("Enter heart rate: "))
spo2 = float(input("Enter SpO2 (%): "))
respiratory_rate = int(input("Enter respiratory rate: "))
systolic_bp = int(input("Enter systolic BP: "))
diastolic_bp = int(input("Enter diastolic BP: "))

print("\nEnter 1 for YES and 0 for NO")

fever = int(input("Fever: "))
breathing_difficulty = int(input("Breathing difficulty: "))
chest_pain = int(input("Chest pain: "))
dizziness = int(input("Dizziness: "))
medical_history = int(input("Medical history: "))

# Create patient data
patient = pd.DataFrame([{
    "age": age,
    "temperature": temperature,
    "heart_rate": heart_rate,
    "spo2": spo2,
    "respiratory_rate": respiratory_rate,
    "systolic_bp": systolic_bp,
    "diastolic_bp": diastolic_bp,
    "fever": fever,
    "breathing_difficulty": breathing_difficulty,
    "chest_pain": chest_pain,
    "dizziness": dizziness,
    "medical_history": medical_history
}])


# Prediction
prediction = model.predict(patient)[0]

# Get prediction probabilities
probabilities = model.predict_proba(patient)[0]
classes = model.classes_

# Create probability dictionary
risk_probabilities = dict(zip(classes, probabilities))

print("\n========================================")
print("          MEDIFUSION AI")
print("       TRIAGE ASSESSMENT")
print("========================================")

print("\nPredicted Risk Level:", prediction)

print("\nRisk Probability:")
for risk in classes:
    print(f"{risk}: {risk_probabilities[risk] * 100:.2f}%")

# Simple explanation based on entered values
print("\nImportant Factors:")

if spo2 < 94:
    print("• Low SpO2 value")

if breathing_difficulty == 1:
    print("• Breathing difficulty reported")

if chest_pain == 1:
    print("• Chest pain reported")

if fever == 1:
    print("• Fever reported")

if heart_rate < 60 or heart_rate > 100:
    print("• Heart rate is outside the typical adult resting range")

if respiratory_rate < 12 or respiratory_rate > 20:
    print("• Respiratory rate is outside the typical adult resting range")

if dizziness == 1:
    print("• Dizziness reported")

if medical_history == 1:
    print("• Medical history reported")

print("\nPrototype Recommendation:")

if prediction == "HIGH":
    print("Seek prompt assessment by a qualified healthcare professional.")
elif prediction == "MEDIUM":
    print("Further assessment by a qualified healthcare professional is recommended.")
else:
    print("Continue routine assessment and monitoring as appropriate.")

print("\nNOTE: This is an AI prototype using synthetic data.")
print("It is not a medical diagnosis or a substitute for professional care.")

print("\n========================================")


