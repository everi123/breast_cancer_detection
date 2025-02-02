"""
  "importance_order": {
    "worst area": 1,
    "worst concave points": 2,
    "mean concave points": 3,
    "worst radius": 4,
    "mean concavity": 5,
    "worst perimeter": 6,
    "mean perimeter": 7,
    "mean radius": 8,
    "mean area": 9,
    "worst concavity": 10
  }
}
Model accuracy on test set: 0.9561
Model and scaler saved successfully.

--- Testing 10 Cases from X_test ---

Test Case 1:
Input Features:
{
  "worst area": 677.9,
  "worst concave points": 0.1015,
  "mean concave points": 0.03821,
  "worst radius": 14.97,
  "mean concavity": 0.08005,
  "worst perimeter": 96.05,
  "mean perimeter": 81.09,
  "mean radius": 12.47,
  "mean area": 481.9,
  "worst concavity": 0.2671
}
Prediction Results:
{
  "Diagnosis": "Benign",
  "Confidence": "76.0%",
  "Severity": "Low Risk",
  "Message": "The model is highly confident in a benign diagnosis. Routine screening is advised.",
  "Recommended Actions": [
    "Maintain regular check-ups",
    "Continue with standard health monitoring"
  ],
  "Ground Truth": "Benign",
  "Correct Prediction": true
}

Test Case 2:
Input Features:
{
  "worst area": 1866.0,
  "worst concave points": 0.1789,
  "mean concave points": 0.07951,
  "worst radius": 24.86,
  "mean concavity": 0.108,
  "worst perimeter": 165.9,
  "mean perimeter": 123.6,
  "mean radius": 18.94,
  "mean area": 1130.0,
  "worst concavity": 0.2687
}
Prediction Results:
{
  "Diagnosis": "Malignant",
  "Confidence": "100.0%",
  "Severity": "High Risk",
  "Message": "High likelihood of malignancy detected. Please consult a doctor immediately.",
  "Recommended Actions": [
    "Schedule immediate follow-up",
    "Prepare detailed medical history",
    "Contact oncology department"
  ],
  "Ground Truth": "Malignant",
  "Correct Prediction": true
}

Test Case 3:
Input Features:
{
  "worst area": 1156.0,
  "worst concave points": 0.1514,
  "mean concave points": 0.08087,
  "worst radius": 19.26,
  "mean concavity": 0.1466,
  "worst perimeter": 124.9,
  "mean perimeter": 101.7,
  "mean radius": 15.46,
  "mean area": 748.9,
  "worst concavity": 0.3791
}
Prediction Results:
{
  "Diagnosis": "Malignant",
  "Confidence": "100.0%",
  "Severity": "High Risk",
  "Message": "High likelihood of malignancy detected. Please consult a doctor immediately.",
  "Recommended Actions": [
    "Schedule immediate follow-up",
    "Prepare detailed medical history",
    "Contact oncology department"
  ],
  "Ground Truth": "Malignant",
  "Correct Prediction": true
}

Test Case 4:
Input Features:
{
  "worst area": 515.8,
  "worst concave points": 0.0737,
  "mean concave points": 0.02799,
  "worst radius": 12.88,
  "mean concavity": 0.07741,
  "worst perimeter": 89.61,
  "mean perimeter": 81.47,
  "mean radius": 12.4,
  "mean area": 467.8,
  "worst concavity": 0.2403
}
Prediction Results:
{
  "Diagnosis": "Benign",
  "Confidence": "99.0%",
  "Severity": "Low Risk",
  "Message": "The model is highly confident in a benign diagnosis. Routine screening is advised.",
  "Recommended Actions": [
    "Maintain regular check-ups",
    "Continue with standard health monitoring"
  ],
  "Ground Truth": "Benign",
  "Correct Prediction": true
}

Test Case 5:
Input Features:
{
  "worst area": 457.8,
  "worst concave points": 0.06918,
  "mean concave points": 0.02594,
  "worst radius": 12.26,
  "mean concavity": 0.06737,
  "worst perimeter": 78.78,
  "mean perimeter": 74.65,
  "mean radius": 11.54,
  "mean area": 402.9,
  "worst concavity": 0.1797
}
Prediction Results:
{
  "Diagnosis": "Benign",
  "Confidence": "100.0%",
  "Severity": "Low Risk",
  "Message": "The model is highly confident in a benign diagnosis. Routine screening is advised.",
  "Recommended Actions": [
    "Maintain regular check-ups",
    "Continue with standard health monitoring"
  ],
  "Ground Truth": "Benign",
  "Correct Prediction": true
}

Test Case 6:
Input Features:
{
  "worst area": 1821.0,
  "worst concave points": 0.265,
  "mean concave points": 0.152,
  "worst radius": 25.74,
  "mean concavity": 0.3514,
  "worst perimeter": 184.6,
  "mean perimeter": 140.1,
  "mean radius": 20.6,
  "mean area": 1265.0,
  "worst concavity": 0.9387
}
Prediction Results:
{
  "Diagnosis": "Malignant",
  "Confidence": "100.0%",
  "Severity": "High Risk",
  "Message": "High likelihood of malignancy detected. Please consult a doctor immediately.",
  "Recommended Actions": [
    "Schedule immediate follow-up",
    "Prepare detailed medical history",
    "Contact oncology department"
  ],
  "Ground Truth": "Malignant",
  "Correct Prediction": true
}

Test Case 7:
Input Features:
{
  "worst area": 2227.0,
  "worst concave points": 0.2432,
  "mean concave points": 0.1501,
  "worst radius": 27.66,
  "mean concavity": 0.2448,
  "worst perimeter": 195.0,
  "mean perimeter": 147.2,
  "mean radius": 22.01,
  "mean area": 1482.0,
  "worst concavity": 0.4756
}
Prediction Results:
{
  "Diagnosis": "Malignant",
  "Confidence": "100.0%",
  "Severity": "High Risk",
  "Message": "High likelihood of malignancy detected. Please consult a doctor immediately.",
  "Recommended Actions": [
    "Schedule immediate follow-up",
    "Prepare detailed medical history",
    "Contact oncology department"
  ],
  "Ground Truth": "Malignant",
  "Correct Prediction": true
}

Test Case 8:
Input Features:
{
  "worst area": 1227.0,
  "worst concave points": 0.1456,
  "mean concave points": 0.07953,
  "worst radius": 20.01,
  "mean concavity": 0.09875,
  "worst perimeter": 134.9,
  "mean perimeter": 115.0,
  "mean radius": 17.57,
  "mean area": 955.1,
  "worst concavity": 0.2489
}
Prediction Results:
{
  "Diagnosis": "Malignant",
  "Confidence": "100.0%",
  "Severity": "High Risk",
  "Message": "High likelihood of malignancy detected. Please consult a doctor immediately.",
  "Recommended Actions": [
    "Schedule immediate follow-up",
    "Prepare detailed medical history",
    "Contact oncology department"
  ],
  "Ground Truth": "Malignant",
  "Correct Prediction": true
}

Test Case 9:
Input Features:
{
  "worst area": 614.9,
  "worst concave points": 0.1708,
  "mean concave points": 0.06987,
  "worst radius": 15.53,
  "mean concavity": 0.1169,
  "worst perimeter": 96.66,
  "mean perimeter": 86.49,
  "mean radius": 13.34,
  "mean area": 520.0,
  "worst concavity": 0.4858
}
Prediction Results:
{
  "Diagnosis": "Malignant",
  "Confidence": "77.0%",
  "Severity": "High Risk",
  "Message": "High likelihood of malignancy detected. Please consult a doctor immediately.",
  "Recommended Actions": [
    "Schedule immediate follow-up",
    "Prepare detailed medical history",
    "Contact oncology department"
  ],
  "Ground Truth": "Benign",
  "Correct Prediction": false
}

Test Case 10:
Input Features:
{
  "worst area": 718.9,
  "worst concave points": 0.06222,
  "mean concave points": 0.01339,
  "worst radius": 15.14,
  "mean concavity": 0.02224,
  "worst perimeter": 101.2,
  "mean perimeter": 88.97,
  "mean radius": 13.9,
  "mean area": 599.4,
  "worst concavity": 0.1384
}
Prediction Results:
{
  "Diagnosis": "Benign",
  "Confidence": "100.0%",
  "Severity": "Low Risk",
  "Message": "The model is highly confident in a benign diagnosis. Routine screening is advised.",
  "Recommended Actions": [
    "Maintain regular check-ups",
    "Continue with standard health monitoring"
  ],
  "Ground Truth": "Benign",
  "Correct Prediction": true
}

"""
curl -X POST http://localhost:5000/predict/predict \
  -H "Content-Type: application/json" \
  -H "Authorization:"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczODQ3NDIxNCwianRpIjoiNDg2ZTkyMzMtYjZhNC00NmEyLWE0MDQtYzU0Y2JhNWExNGY3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6ImRvY3RvcjEiLCJyb2xlIjoiZG9jdG9yIn0sIm5iZiI6MTczODQ3NDIxNCwiZXhwIjoxNzM4NDc3ODE0fQ.Xec0tuWP7lxF1QgtA3_uIZM3W0OUbUmGq8dmTT1YtWI" " \
  -d '{
    "features": {
      "worst area": 515.8,
      "worst concave points": 0.0737,
      "mean concave points": 0.02799,
      "worst radius": 12.88,
      "mean concavity": 0.07741,
      "worst perimeter": 89.61,
      "mean perimeter": 81.47,
      "mean radius": 12.4,
      "mean area": 467.8,
      "worst concavity": 0.2403
    }
  }'
