import re


def extract_symptoms(text):
    """
    Convert English patient speech into structured symptom features.
    Prototype rule-based extractor for MediFusion-AI.
    """

    text = text.lower()

    features = {
        "fever": 0,
        "cough": 0,
        "headache": 0,
        "vomiting": 0,
        "diarrhea": 0,
        "fatigue": 0,
        "abdominal_pain": 0,
        "dizziness": 0,
        "chest_pain": 0,
        "breathing_difficulty": 0
    }

    # Fever
    if any(word in text for word in [
        "fever",
        "high temperature",
        "temperature"
    ]):
        features["fever"] = 1

    # Cough
    if any(word in text for word in [
        "cough",
        "coughing"
    ]):
        features["cough"] = 1

    # Headache
    if any(word in text for word in [
        "headache",
        "head pain"
    ]):
        features["headache"] = 1

    # Vomiting
    if any(word in text for word in [
        "vomit",
        "vomiting",
        "threw up"
    ]):
        features["vomiting"] = 1

    # Diarrhea
    if any(word in text for word in [
        "diarrhea",
        "loose motion",
        "loose motions"
    ]):
        features["diarrhea"] = 1

    # Fatigue
    if any(word in text for word in [
        "fatigue",
        "tired",
        "very weak",
        "weakness",
        "weak"
    ]):
        features["fatigue"] = 1

    # Abdominal pain
    if any(word in text for word in [
        "stomach pain",
        "abdominal pain",
        "belly pain"
    ]):
        features["abdominal_pain"] = 1

    # Dizziness
    if any(word in text for word in [
        "dizzy",
        "dizziness",
        "lightheaded"
    ]):
        features["dizziness"] = 1

    # Chest pain
    if any(word in text for word in [
        "chest pain",
        "pain in my chest"
    ]):
        features["chest_pain"] = 1

    # Breathing difficulty
    if any(word in text for word in [
        "difficulty breathing",
        "breathing difficulty",
        "shortness of breath",
        "hard to breathe",
        "cannot breathe"
    ]):
        features["breathing_difficulty"] = 1

    return features


if __name__ == "__main__":

    test_text = """
    I have fever and headache.
    I am feeling very weak and dizzy.
    I also have chest pain.
    """

    result = extract_symptoms(test_text)

    print("\nExtracted symptoms:")
    print(result)