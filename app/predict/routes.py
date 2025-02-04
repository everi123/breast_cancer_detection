# app/predict/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import joblib
import numpy as np
import os
import json

predict_bp = Blueprint('predict', __name__)

# Load the model, scaler, and feature information
try:
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    model_path = os.path.join(base_dir, 'final_model.pkl')
    scaler_path = os.path.join(base_dir, 'scaler_top.pkl')
    feature_info_path = os.path.join(base_dir, 'feature_info.json')
    
    final_model = joblib.load(model_path)
    scaler_top = joblib.load(scaler_path)
    
    with open(feature_info_path, 'r') as f:
        feature_info = json.load(f)
    
    REQUIRED_FEATURES = feature_info['features']
    print("Model, scaler, and feature info loaded successfully")
    
except Exception as e:
    print(f"Error loading files: {str(e)}")
    final_model = None
    scaler_top = None
    feature_info = None
    REQUIRED_FEATURES = []

@predict_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    if final_model is None or scaler_top is None:
        return jsonify({"error": "Model not initialized"}), 500

    try:
        current_user = get_jwt_identity()
        if current_user["role"] not in ["doctor", "admin"]:
            return jsonify({"error": "Unauthorized access"}), 403

        data = request.get_json(force=True)
        
        # Handle dictionary input format
        if not isinstance(data, dict) or 'features' not in data:
            return jsonify({
                "error": "Invalid input format",
                "message": "Expected format: {'features': {feature_name: value, ...}}",
                "example": {
                    "features": {
                        "worst area": 515.8,
                        "worst concave points": 0.0737,
                        # ... other features
                    }
                }
            }), 400

        features_dict = data['features']
        
        # Validate all required features are present
        missing_features = set(REQUIRED_FEATURES) - set(features_dict.keys())
        if missing_features:
            return jsonify({
                "error": "Missing features",
                "missing_features": list(missing_features),
                "required_features": REQUIRED_FEATURES
            }), 400

        # Convert dictionary to ordered list based on feature importance
        features_list = [features_dict[feature] for feature in REQUIRED_FEATURES]

        # Validate numerical values
        if not all(isinstance(x, (int, float)) for x in features_list):
            return jsonify({
                "error": "Invalid feature values",
                "message": "All features must be numerical values"
            }), 400

        # Make prediction
        input_data = np.array(features_list).reshape(1, -1)
        scaled_data = scaler_top.transform(input_data)
        prediction = final_model.predict(scaled_data)
        probabilities = final_model.predict_proba(scaled_data)[0]
        
        result = "malignant" if prediction[0] == 0 else "benign"
        confidence = float(probabilities[0] if result == "malignant" else probabilities[1])

        response = {
            "prediction": result,
            "confidence": round(confidence * 100, 2),
            "features_received": {
                feature: value for feature, value in zip(REQUIRED_FEATURES, features_list)
            }
        }

        if result == "malignant":
            response.update({
                "severity": "High Risk",
                "message": "Please consult a doctor immediately.",
                "recommended_actions": [
                    "Schedule immediate follow-up",
                    "Prepare medical history",
                    "Contact oncology department"
                ]
            })
        else:
            response.update({
                "severity": "Low Risk",
                "message": "No immediate action required.",
                "recommended_actions": [
                    "Continue regular check-ups",
                    "Schedule next screening as recommended"
                ]
            })

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "message": str(e),
            "required_features": REQUIRED_FEATURES
        }), 500