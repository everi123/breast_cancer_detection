# train_model.py

import pandas as pd
import numpy as np
import json
import joblib

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# ----------------------------
# 1. LOAD DATASET AND TRAIN MODEL
# ----------------------------

# Load dataset
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train an initial model to obtain feature importances
initial_model = RandomForestClassifier(random_state=42)
initial_model.fit(X_train, y_train)

# Get feature importances and sort indices in descending order
importances = initial_model.feature_importances_
indices = np.argsort(importances)[::-1]

# Get top 10 features
top_features = X.columns[indices][:10].tolist()

# Save feature names and (dummy) descriptions
feature_info = {
    "features": top_features,
    "descriptions": {name: f"Description for {name}" for name in top_features},
    "importance_order": {name: idx + 1 for idx, name in enumerate(top_features)}
}
print("Selected Feature Info:")
print(json.dumps(feature_info, indent=2))

with open('feature_info.json', 'w') as f:
    json.dump(feature_info, f, indent=2)

# Select and scale top features
X_train_top = X_train[top_features]
X_test_top = X_test[top_features]

scaler_top = StandardScaler()
X_train_top_scaled = scaler_top.fit_transform(X_train_top)
X_test_top_scaled = scaler_top.transform(X_test_top)

# Train final model using the top features
final_model = RandomForestClassifier(random_state=42)
final_model.fit(X_train_top_scaled, y_train)

# Evaluate the final model on the test set
y_pred_final = final_model.predict(X_test_top_scaled)
accuracy = accuracy_score(y_test, y_pred_final)
print(f"Model accuracy on test set: {accuracy:.4f}")

# Save model and scaler
joblib.dump(final_model, 'final_model.pkl')
joblib.dump(scaler_top, 'scaler_top.pkl')
print("Model and scaler saved successfully.")

# ----------------------------
# 2. DEFINE PREDICTION FUNCTION WITH CONFIDENCE & RISK LEVEL
# ----------------------------

def get_risk_assessment(pred_class, confidence_pct):
    """
    Map confidence to risk level and provide an action message.
    
    For malignant predictions (class 0):
      - High Risk: confidence >= 75%
      - Moderate Risk: 60% <= confidence < 75%
      - Low Risk: confidence < 60%
    
    For benign predictions (class 1), we assume Low Risk.
    """
    # Note: In the breast cancer dataset, typically:
    #    0 = malignant, 1 = benign
    if pred_class == 0:  # malignant
        if confidence_pct >= 75:
            risk = "High Risk"
            message = "High likelihood of malignancy detected. Please consult a doctor immediately."
            actions = [
                "Schedule immediate follow-up",
                "Prepare detailed medical history",
                "Contact oncology department"
            ]
        elif confidence_pct >= 60:
            risk = "Moderate Risk"
            message = "The results are borderline. Additional diagnostic tests are advised."
            actions = [
                "Consider further imaging and tests",
                "Review previous medical records",
                "Consult with a specialist"
            ]
        else:
            risk = "Low Risk"
            message = "Malignancy probability is lower; however, further monitoring is recommended."
            actions = [
                "Schedule regular follow-ups",
                "Monitor any changes",
                "Discuss concerns with your physician"
            ]
    else:  # benign
        risk = "Low Risk"
        message = "The model is highly confident in a benign diagnosis. Routine screening is advised."
        actions = [
            "Maintain regular check-ups",
            "Continue with standard health monitoring"
        ]
    return risk, message, actions

def predict_case(input_features):
    """
    Given a dictionary of input features, scale them,
    generate a prediction with confidence and risk assessment.
    
    If any feature is missing, fill it with the training mean.
    """
    # Create a DataFrame with the expected columns (top_features)
    df_input = pd.DataFrame([input_features], columns=top_features)
    
    # Check for missing features (columns with NaN) and fill them with training mean from scaler_top
    missing_features = df_input.columns[df_input.isnull().any()].tolist()
    if missing_features:
        fill_values = {feature: scaler_top.mean_[i] for i, feature in enumerate(top_features) if feature in missing_features}
        df_input.fillna(fill_values, inplace=True)
    
    # Scale features
    scaled_input = scaler_top.transform(df_input)
    
    # Get prediction probabilities from the trained model
    proba = final_model.predict_proba(scaled_input)[0]
    # The model's classes: 0 -> malignant, 1 -> benign
    pred_class = np.argmax(proba)
    confidence_pct = round(proba[pred_class] * 100, 1)
    diagnosis = "Malignant" if pred_class == 0 else "Benign"
    risk, message, actions = get_risk_assessment(pred_class, confidence_pct)
    
    result = {
        "Diagnosis": diagnosis,
        "Confidence": f"{confidence_pct}%",
        "Severity": risk,
        "Message": message,
        "Recommended Actions": actions
    }
    return result

# ----------------------------
# 3. TEST ON 10 CASES FROM X_TEST WITH GROUND TRUTH COMPARISON
# ----------------------------

print("\n--- Testing 10 Cases from X_test ---")

# Convert y_test to a list for easy lookup (the order is maintained from train_test_split)
y_test_list = y_test.tolist()

for i in range(10):
    # Extract the i-th row from the original X_test_top DataFrame
    input_case = X_test_top.iloc[i].to_dict()
    
    # Get prediction results for the input case
    prediction = predict_case(input_case)
    
    # Map ground truth: 0 -> "Malignant", 1 -> "Benign"
    ground_truth = y_test_list[i]
    gt_label = "Malignant" if ground_truth == 0 else "Benign"
    
    # Add ground truth to prediction output and compare with predicted label
    prediction["Ground Truth"] = gt_label
    prediction["Correct Prediction"] = (prediction["Diagnosis"] == gt_label)
    
    print(f"\nTest Case {i+1}:")
    print("Input Features:")
    print(json.dumps(input_case, indent=2))
    print("Prediction Results:")
    print(json.dumps(prediction, indent=2))
