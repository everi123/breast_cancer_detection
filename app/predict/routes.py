# app/predict/routes.py
# app/predict/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import joblib
import numpy as np

predict_bp = Blueprint('predict', __name__)

# Load the final model and scaler
final_model = joblib.load('final_model.pkl')
scaler_top = joblib.load('scaler_top.pkl')

@predict_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    current_user = get_jwt_identity()
    if current_user["role"] not in ["doctor", "admin"]:
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.json
    if not data or not isinstance(data, list) or len(data) != 10:
        return jsonify({"error": "Invalid input format. Expected 10 feature values."}), 400

    try:
        input_data = np.array(data).reshape(1, -1)
        scaled_data = scaler_top.transform(input_data)
        prediction = final_model.predict(scaled_data)
        result = "malignant" if prediction[0] == 0 else "benign"

        if result == "malignant":
            return jsonify({
                "prediction": result,
                "message": "Please consult a doctor immediately.",
                "recommended_doctors": ["Dr. Smith", "Dr. Johnson", "Dr. Lee"]
            }), 200
        else:
            return jsonify({
                "prediction": result,
                "message": "No immediate action required."
            }), 200

    except Exception as e:
        return jsonify({"error": "Prediction failed", "details": str(e)}), 500