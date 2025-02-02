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

def get_risk_assessment(pred_class, confidence_pct):
    """
    Maps confidence (in percentage) to risk level and returns
    a tuple of (risk, message, recommended_actions).

    For malignant predictions (class 0):
      - High Risk: confidence >= 75%
      - Moderate Risk: 60% <= confidence < 75%
      - Low Risk: confidence < 60%
      
    For benign predictions (class 1), we always return Low Risk.
    """
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
            message = "Results are borderline. Additional diagnostic tests are advised."
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

@predict_bp.route('/features', methods=['GET'])
def get_features():
    """Endpoint to get the required features and their descriptions."""
    if feature_info is None:
        return jsonify({"error": "Feature information not available"}), 500
    return jsonify(feature_info), 200

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
        
        # Support both dictionary and list inputs.
        if isinstance(data, dict):
            # Either a dictionary with a "features" key or a dictionary with feature names
            if 'features' in data:
                # Expecting a list in the "features" key
                features = data['features']
            else:
                # Build list from required features; missing keys will be set to None
                features = [data.get(feature, None) for feature in REQUIRED_FEATURES]
        else:
            features = data

        # Validate features count
        if len(features) != len(REQUIRED_FEATURES):
            return jsonify({
                "error": "Invalid number of features",
                "message": f"Expected {len(REQUIRED_FEATURES)} features, got {len(features)}",
                "required_features": feature_info
            }), 400

        # Validate that all features are numbers
        if not all(isinstance(x, (int, float)) for x in features):
            return jsonify({
                "error": "Invalid feature values",
                "message": "All features must be numerical values"
            }), 400

        # Prepare input data for prediction
        input_data = np.array(features).reshape(1, -1)
        scaled_data = scaler_top.transform(input_data)
        
        # Obtain prediction and probabilities from the model
        prediction = final_model.predict(scaled_data)
        probabilities = final_model.predict_proba(scaled_data)[0]
        
        # Model classes: 0 -> malignant, 1 -> benign
        pred_class = prediction[0]
        result_label = "malignant" if pred_class == 0 else "benign"
        
        # Use the corresponding probability for the predicted class as confidence
        confidence = float(probabilities[0] if pred_class == 0 else probabilities[1])
        confidence_pct = round(confidence * 100, 2)
        
        # Determine risk assessment based on prediction and confidence
        risk, message, recommended_actions = get_risk_assessment(pred_class, confidence_pct)
        
        response = {
            "prediction": result_label,
            "confidence": confidence_pct,
            "severity": risk,
            "message": message,
            "recommended_actions": recommended_actions,
            "features_received": dict(zip(REQUIRED_FEATURES, features))
        }
        
        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "message": str(e),
            "required_features": feature_info
        }), 500
