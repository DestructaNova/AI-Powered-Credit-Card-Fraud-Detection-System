import os
import sys
from ml_pipeline import train_model_from_csv

def main():
    csv_file = "creditcard.csv"

    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        print("Please ensure the credit card dataset is available in the current directory.")
        sys.exit(1)

    print("Starting model training...")
    print(f"Dataset: {csv_file}")
    print(f"File size: {os.path.getsize(csv_file) / (1024*1024):.2f} MB")

    try:
        results = train_model_from_csv(csv_file, model_dir='model')
        
        print("\n" + "="*50)
        print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
        print("="*50)
        print(f"Accuracy: {results['accuracy']:.4f}")
        print(f"Confusion Matrix:")
        print(f"  {results['confusion_matrix']}")
        
        # Print classification report
        if 'classification_report' in results:
            report = results['classification_report']
            print(f"\nClassification Report:")
            print(f"  Precision (Class 0): {report['0']['precision']:.4f}")
            print(f"  Recall (Class 0): {report['0']['recall']:.4f}")
            print(f"  F1-Score (Class 0): {report['0']['f1-score']:.4f}")
            print(f"  Precision (Class 1): {report['1']['precision']:.4f}")
            print(f"  Recall (Class 1): {report['1']['recall']:.4f}")
            print(f"  F1-Score (Class 1): {report['1']['f1-score']:.4f}")
        
        print(f"\nModel files saved in 'model/' directory:")
        model_files = ['fraud_model.pkl', 'scaler.pkl', 'feature_columns.pkl']
        for file in model_files:
            filepath = os.path.join('model', file)
            if os.path.exists(filepath):
                size = os.path.getsize(filepath) / 1024  # KB
                print(f"  ✓ {file} ({size:.1f} KB)")
            else:
                print(f"  ✗ {file} (missing)")
        
        print("\nYou can now run the Flask application:")
        print("  python app.py")
        
    except Exception as e:
        print(f"\nError during training: {str(e)}")
        print("Please check the dataset format and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
