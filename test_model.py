# test_model.py
import requests
import json

# API configuration
BASE_URL = "http://localhost:5000"

def login():
    """Get authentication token"""
    login_data = {
        "username": "doctor1",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    return response.json()["access_token"]

def make_prediction(features, token):
    """Make prediction with given features"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{BASE_URL}/predict/predict",
        headers=headers,
        json={"features": features}
    )
    return response.json()

# Test cases - these are example values for the 10 most important features
test_cases = [
    # Test Case 1 - Likely Malignant
    {
        "mean radius": 20.57,
        "mean texture": 17.77,
        "mean perimeter": 132.9,
        "mean area": 1326.0,
        "mean smoothness": 0.08474,
        "mean compactness": 0.07864,
        "mean concavity": 0.0869,
        "mean concave points": 0.07017,
        "mean symmetry": 0.1812,
        "mean fractal dimension": 0.05667
    },
    # Test Case 2 - Likely Benign
    {
        "mean radius": 12.05,
        "mean texture": 14.63,
        "mean perimeter": 78.04,
        "mean area": 449.3,
        "mean smoothness": 0.10340,
        "mean compactness": 0.09791,
        "mean concavity": 0.06495,
        "mean concave points": 0.02513,
        "mean symmetry": 0.1731,
        "mean fractal dimension": 0.06267
    },
    # Test Case 3 - Borderline Case
    {
        "mean radius": 15.13,
        "mean texture": 15.51,
        "mean perimeter": 97.65,
        "mean area": 711.8,
        "mean smoothness": 0.09463,
        "mean compactness": 0.08650,
        "mean concavity": 0.07741,
        "mean concave points": 0.04768,
        "mean symmetry": 0.1794,
        "mean fractal dimension": 0.05742
    },
    # Test Case 4 - Strong Malignant Indicators
    {
        "mean radius": 19.69,
        "mean texture": 21.25,
        "mean perimeter": 130.0,
        "mean area": 1203.0,
        "mean smoothness": 0.10960,
        "mean compactness": 0.15990,
        "mean concavity": 0.1974,
        "mean concave points": 0.12790,
        "mean symmetry": 0.2069,
        "mean fractal dimension": 0.05999
    },
    # Test Case 5 - Strong Benign Indicators
    {
        "mean radius": 11.42,
        "mean texture": 12.95,
        "mean perimeter": 73.17,
        "mean area": 402.7,
        "mean smoothness": 0.09666,
        "mean compactness": 0.07806,
        "mean concavity": 0.03285,
        "mean concave points": 0.02037,
        "mean symmetry": 0.1574,
        "mean fractal dimension": 0.05847
    }
]

def run_tests():
    try:
        # Get authentication token
        token = login()
        print("Successfully logged in\n")

        # Run each test case
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest Case {i}:")
            print("Input features:")
            for feature, value in test_case.items():
                print(f"{feature}: {value}")
            
            # Convert dictionary to list maintaining feature order
            features_list = list(test_case.values())
            
            # Make prediction
            result = make_prediction(features_list, token)
            
            print("\nPrediction Results:")
            print(f"Diagnosis: {result['prediction']}")
            print(f"Confidence: {result.get('confidence', 'N/A')}%")
            print(f"Severity: {result.get('severity', 'N/A')}")
            print(f"Message: {result.get('message', 'N/A')}")
            if 'recommended_actions' in result:
                print("\nRecommended Actions:")
                for action in result['recommended_actions']:
                    print(f"- {action}")
            print("\n" + "="*50)

    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    run_tests()