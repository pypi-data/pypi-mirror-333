from .data import symptom_to_condition

def analyze_symptoms(user_symptoms, medical_history=None):  # d default empty list
    # Ensure medical_history is always a list
    if medical_history is None:
        medical_history = []

    # Normalize user input
    user_symptoms = [symptom.strip().lower() for symptom in user_symptoms]
    medical_history = [condition.strip().lower() for condition in medical_history]

    matched_conditions = []
    highest_severity = "Mild"  # Default severity
    recommendation = "No immediate action required."

    # Iterate through known symptoms
    for symptom, conditions in symptom_to_condition.items():
        if symptom in user_symptoms:
            for condition in conditions:
                severity = determine_severity(condition, medical_history)
                matched_conditions.append({"condition": condition, "severity": severity})

                # Update highest severity if needed
                if severity in ["High", "Severe"]:
                    highest_severity = severity

    # Provide recommendation based on severity
    if highest_severity == "Severe":
        recommendation = "Consult a doctor immediately."
    # elif highest_severity == "Moderate":
    #     recommendation == "Take precautions, have a right diet. Good Health, better days!"
    elif highest_severity == "High":
        recommendation = "Monitor symptoms and seek medical attention if it worsens."

    if not matched_conditions:
        return {
            "conditions": ["No matching allergy or deficiency found."],
            "severity": "N/A",
            "recommendation": "No immediate action required."
        }

    return {
        "conditions": matched_conditions,
        "severity": highest_severity,
        "recommendation": recommendation
    }

def determine_severity(condition, medical_history):
    # Define severity levels based on conditions
    severity_map = {
        "pollen allergy": "Mild",
        "iron deficiency": "Moderate",
        "dust allergy": "Mild",
        "migraine": "Severe",
        "vitamin d deficiency": "Moderate",
        "sinus allergy": "Mild",
        "chest pain": "High",
        "asthma": "Severe",
        "heart disease": "Severe"
    }
    
    severity = severity_map.get(condition.lower(), "Mild")  # Default severity
    
    # Increase severity if relevant medical history exists
    if condition.lower() == "heart disease" and "hypertension" in medical_history:
        severity = "Severe"
    if condition.lower() == "asthma" and "respiratory infection" in medical_history:
        severity = "Severe"
    if condition.lower() == "chest pain" and "hypertension" in medical_history:
        severity = "High"

    return severity
