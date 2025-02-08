import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif
import warnings
warnings.filterwarnings('ignore')

class BreastCancerClassifier:
    def __init__(self, random_state=42):
        """Initialize the breast cancer classifier with configuration parameters."""
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.feature_selector = None
        self.model = None
        self.feature_names = None
        
    def load_data(self):
        """Load the breast cancer dataset and prepare features/target variables."""
        # Load built-in breast cancer dataset
        data = load_breast_cancer()
        self.feature_names = data.feature_names
        
        X = pd.DataFrame(data.data, columns=data.feature_names)
        y = pd.Series(data.target)
        
        return X, y
    
    def create_pipeline(self, n_features=15):
        """Create a pipeline with feature selection and model training."""
        # Feature selection using ANOVA F-value
        self.feature_selector = SelectKBest(score_func=f_classif, k=n_features)
        
        # Initialize base model with regularization to prevent overfitting
        base_model = LogisticRegression(
            C=0.1,  # Stronger regularization
            max_iter=1000,
            random_state=self.random_state
        )
        
        # Create pipeline
        return Pipeline([
            ('scaler', self.scaler),
            ('feature_selection', self.feature_selector),
            ('classifier', base_model)
        ])
    
    def evaluate_model(self, X, y, cv=5):
        """Evaluate model using cross-validation."""
        # Create stratified k-fold cross-validation
        skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=self.random_state)
        
        # Compute cross-validation scores
        cv_scores = cross_val_score(self.model, X, y, cv=skf, scoring='roc_auc')
        
        return {
            'mean_cv_score': cv_scores.mean(),
            'cv_score_std': cv_scores.std(),
            'cv_scores': cv_scores
        }
    
    def get_feature_importance(self, X, y):
        """Get feature importance scores after fitting the model."""
        # Fit the feature selector
        self.model.fit(X, y)
        
        # Get selected feature indices and their scores
        selected_features_mask = self.model.named_steps['feature_selection'].get_support()
        selected_features = X.columns[selected_features_mask].tolist()
        importance_scores = self.model.named_steps['feature_selection'].scores_[selected_features_mask]
        
        # Create feature importance DataFrame
        feature_importance = pd.DataFrame({
            'Feature': selected_features,
            'Importance': importance_scores
        }).sort_values('Importance', ascending=False)
        
        return feature_importance
    
    def train_and_evaluate(self, test_size=0.2):
        """Train the model and evaluate its performance."""
        # Load and split data
        X, y = self.load_data()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        # Create and fit pipeline
        self.model = self.create_pipeline()
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        cv_results = self.evaluate_model(X_train, y_train)
        
        # Get predictions on test set
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        test_auc = roc_auc_score(y_test, y_pred_proba)
        
        # Get feature importance
        feature_importance = self.get_feature_importance(X, y)
        
        return {
            'cv_results': cv_results,
            'test_auc': test_auc,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'feature_importance': feature_importance,
            'test_predictions': (y_test, y_pred, y_pred_proba)
        }

    def plot_results(self, results):
        """Plot evaluation results including ROC curve and feature importance."""
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot feature importance
        feature_importance = results['feature_importance']
        sns.barplot(
            data=feature_importance.head(10),
            x='Importance',
            y='Feature',
            ax=ax1
        )
        ax1.set_title('Top 10 Most Important Features')
        ax1.set_xlabel('Feature Importance Score')
        
        # Plot confusion matrix
        sns.heatmap(
            results['confusion_matrix'],
            annot=True,
            fmt='d',
            cmap='Blues',
            ax=ax2
        )
        ax2.set_title('Confusion Matrix')
        ax2.set_xlabel('Predicted')
        ax2.set_ylabel('Actual')
        
        plt.tight_layout()
        plt.show()

# Usage example
def main():
    # Initialize and train classifier
    classifier = BreastCancerClassifier()
    results = classifier.train_and_evaluate()
    
    # Print results
    print("\nCross-validation Results:")
    print(f"Mean ROC-AUC: {results['cv_results']['mean_cv_score']:.3f} "
          f"(±{results['cv_results']['cv_score_std']:.3f})")
    
    print(f"\nTest Set ROC-AUC: {results['test_auc']:.3f}")
    
    print("\nClassification Report:")
    print(results['classification_report'])
    
    # Plot results
    classifier.plot_results(results)

if __name__ == "__main__":
    main()