import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from imblearn.combine import SMOTETomek
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class FraudDetectionPipeline:
    def __init__(self, model_dir='model'):
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.is_trained = False
        os.makedirs(model_dir, exist_ok=True)

    def preprocess_data(self, df, is_training=True):
        data = df.copy()
        data = data.fillna(0)

        if is_training and 'Class' in data.columns:
            X = data.drop('Class', axis=1)
            y = data['Class']

            self.feature_columns = X.columns.tolist()

            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

            return X_scaled, y
        else:
            if self.feature_columns is not None:
                missing_cols = set(self.feature_columns) - set(data.columns)
                for col in missing_cols:
                    data[col] = 0
                
                # Select only the columns used in training
                X = data[self.feature_columns]
            else:
                # If no feature columns stored, assume all columns except Class
                if 'Class' in data.columns:
                    X = data.drop('Class', axis=1)
                else:
                    X = data
            
            # Scale the features using the fitted scaler
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X)
                X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
                return X_scaled
            else:
                return X
    
    def train_model(self, df, test_size=0.3, random_state=42):
        print("Starting model training...")

        X, y = self.preprocess_data(df, is_training=True)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"Original class distribution: {Counter(y_train)}")
        
        # Apply SMOTETomek for handling imbalanced data
        smote_tomek = SMOTETomek(sampling_strategy=0.5, random_state=random_state)
        X_train_resampled, y_train_resampled = smote_tomek.fit_resample(X_train, y_train)
        
        print(f"After SMOTETomek: {Counter(y_train_resampled)}")
        
        # Train RandomForest model
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=random_state,
            n_jobs=-1
        )
        
        print("Training RandomForest model...")
        self.model.fit(X_train_resampled, y_train_resampled)
        
        # Make predictions on test set
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred, output_dict=True)
        
        self.is_trained = True
        
        # Save the model and scaler
        self.save_model()
        
        results = {
            'accuracy': accuracy,
            'confusion_matrix': conf_matrix.tolist(),
            'classification_report': class_report,
            'test_predictions': y_pred.tolist(),
            'test_actual': y_test.tolist()
        }
        
        print(f"Model training completed. Accuracy: {accuracy:.4f}")
        return results
    
    def predict(self, df):
        """
        Make predictions on new data
        
        Args:
            df (pd.DataFrame): Input dataframe for prediction
            
        Returns:
            dict: Prediction results
        """
        if not self.is_trained and not self.load_model():
            raise ValueError("Model is not trained. Please train the model first or ensure model files exist.")
        
        # Preprocess the data
        X = self.preprocess_data(df, is_training=False)
        
        # Make predictions
        prediction_proba = self.model.predict_proba(X)

        # Get fraud probabilities (class 1)
        fraud_probabilities = prediction_proba[:, 1] if prediction_proba.shape[1] > 1 else prediction_proba[:, 0]

        # Use a lower threshold for fraud detection (0.3 instead of 0.5)
        # This is more appropriate for imbalanced fraud detection
        fraud_threshold = 0.3
        predictions = (fraud_probabilities >= fraud_threshold).astype(int)
        
        # Create results dataframe
        results_df = df.copy()
        results_df['Prediction'] = predictions
        results_df['Fraud_Probability'] = fraud_probabilities

        # Add original index for tracking
        results_df['original_index'] = range(len(results_df))

        # Get fraudulent transactions
        fraud_transactions = results_df[results_df['Prediction'] == 1]
        
        results = {
            'total_transactions': len(df),
            'fraudulent_count': int(np.sum(predictions)),
            'fraud_percentage': float(np.sum(predictions) / len(predictions) * 100),
            'fraudulent_transactions': fraud_transactions.to_dict('records'),
            'all_predictions': predictions.tolist(),
            'fraud_probabilities': fraud_probabilities.tolist()
        }
        
        return results
    
    def save_model(self):
        """Save the trained model and scaler to disk"""
        if self.model is not None:
            model_path = os.path.join(self.model_dir, 'fraud_model.pkl')
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            print(f"Model saved to {model_path}")
        
        if self.scaler is not None:
            scaler_path = os.path.join(self.model_dir, 'scaler.pkl')
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            print(f"Scaler saved to {scaler_path}")
        
        if self.feature_columns is not None:
            features_path = os.path.join(self.model_dir, 'feature_columns.pkl')
            with open(features_path, 'wb') as f:
                pickle.dump(self.feature_columns, f)
            print(f"Feature columns saved to {features_path}")
    
    def load_model(self):
        """
        Load the trained model and scaler from disk
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            model_path = os.path.join(self.model_dir, 'fraud_model.pkl')
            scaler_path = os.path.join(self.model_dir, 'scaler.pkl')
            features_path = os.path.join(self.model_dir, 'feature_columns.pkl')
            
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print("Model loaded successfully")
            
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                print("Scaler loaded successfully")
            
            if os.path.exists(features_path):
                with open(features_path, 'rb') as f:
                    self.feature_columns = pickle.load(f)
                print("Feature columns loaded successfully")
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False


def train_model_from_csv(csv_path, model_dir='model'):
    """
    Convenience function to train model directly from CSV file
    
    Args:
        csv_path (str): Path to the CSV file
        model_dir (str): Directory to save model artifacts
        
    Returns:
        dict: Training results
    """
    # Load data
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Initialize pipeline
    pipeline = FraudDetectionPipeline(model_dir=model_dir)
    
    # Train model
    results = pipeline.train_model(df)
    
    return results


if __name__ == "__main__":
    # Example usage
    csv_path = "creditcard.csv"
    if os.path.exists(csv_path):
        results = train_model_from_csv(csv_path)
        print("Training completed!")
        print(f"Accuracy: {results['accuracy']:.4f}")
    else:
        print(f"CSV file {csv_path} not found.")
