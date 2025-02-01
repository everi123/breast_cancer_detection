# train_model.py
# train_model.py
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train initial model using all features
initial_model = RandomForestClassifier(random_state=42)
initial_model.fit(X_train_scaled, y_train)

# Test the initial model on the test set
y_pred_initial = initial_model.predict(X_test_scaled)
print(f"Accuracy using all features: {accuracy_score(y_test, y_pred_initial)}")

# Get feature importances
importances = initial_model.feature_importances_
indices = np.argsort(importances)[::-1]  # Sort in descending order

# Visualize feature importances
plt.figure(figsize=(10, 6))
plt.title("Feature Importances (All Features)")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), X.columns[indices], rotation=90)
plt.xlabel("Feature")
plt.ylabel("Importance")
plt.show()

# Select top 10 most important features
top_features = X.columns[indices][:10]
print("Top 10 most important features:", top_features.tolist())

# Retrain the model using only the top 10 features
X_train_top = X_train[top_features]
X_test_top = X_test[top_features]

# Scale the top features
scaler_top = StandardScaler()
X_train_top_scaled = scaler_top.fit_transform(X_train_top)
X_test_top_scaled = scaler_top.transform(X_test_top)

# Train final model using top 10 features
final_model = RandomForestClassifier(random_state=42)
final_model.fit(X_train_top_scaled, y_train)

# Test the final model on the test set
y_pred_final = final_model.predict(X_test_top_scaled)
print(f"Accuracy using top 10 features: {accuracy_score(y_test, y_pred_final)}")

# Save the final model and scaler
joblib.dump(final_model, 'final_model.pkl')
joblib.dump(scaler_top, 'scaler_top.pkl')
print("Final model and scaler saved.")

# Test the final model on unseen data (using the test set as unseen data)
unseen_data = X_test_top_scaled[:5]  # Use the first 5 samples from the test set as unseen data
unseen_predictions = final_model.predict(unseen_data)
print("Predictions for unseen data:", unseen_predictions)
print("Actual labels for unseen data:", y_test[:5])