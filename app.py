import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import json
from ml_pipeline import FraudDetectionPipeline

app = Flask(__name__)
app.secret_key = 'fraud-detection-secret-key-2024'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ml_pipeline = FraudDetectionPipeline(model_dir='model')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_csv_structure(df):
    required_columns = ['Time', 'Amount']
    v_columns = [f'V{i}' for i in range(1, 29)]
    expected_columns = required_columns + v_columns

    missing_columns = set(expected_columns) - set(df.columns)
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    if len(df) == 0:
        return False, "CSV file is empty"

    for col in expected_columns:
        if col in df.columns:
            try:
                pd.to_numeric(df[col], errors='raise')
            except (ValueError, TypeError):
                return False, f"Column '{col}' contains non-numeric data"

    return True, "Valid CSV structure"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            df = pd.read_csv(filepath)

            is_valid, error_message = validate_csv_structure(df)
            if not is_valid:
                flash(f'Invalid CSV format: {error_message}')
                os.remove(filepath)
                return redirect(url_for('index'))

            if not ml_pipeline.is_trained:
                model_loaded = ml_pipeline.load_model()
                if not model_loaded:
                    flash('Model not found. Please ensure the model has been trained.')
                    os.remove(filepath)
                    return redirect(url_for('index'))
            
            # Make predictions
            results = ml_pipeline.predict(df)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            # Prepare data for template
            fraud_transactions = results['fraudulent_transactions']
            
            # Add row indices to fraudulent transactions
            for i, transaction in enumerate(fraud_transactions):
                # Find the original index in the dataframe
                original_index = None
                for idx, row in df.iterrows():
                    if all(row[col] == transaction[col] for col in ['Time', 'Amount'] if col in transaction):
                        original_index = idx
                        break
                transaction['original_index'] = original_index if original_index is not None else i
            
            return render_template('results.html', 
                                 total_transactions=results['total_transactions'],
                                 fraudulent_count=results['fraudulent_count'],
                                 fraud_percentage=round(results['fraud_percentage'], 2),
                                 fraud_transactions=fraud_transactions)
            
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            # Clean up uploaded file if it exists
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload a CSV file.')
        return redirect(url_for('index'))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions (JSON response)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please provide a CSV file.'}), 400
        
        # Save temporary file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read and validate CSV
        df = pd.read_csv(filepath)
        
        is_valid, error_message = validate_csv_structure(df)
        if not is_valid:
            os.remove(filepath)
            return jsonify({'error': f'Invalid CSV format: {error_message}'}), 400
        
        # Load model if needed
        if not ml_pipeline.is_trained:
            model_loaded = ml_pipeline.load_model()
            if not model_loaded:
                os.remove(filepath)
                return jsonify({'error': 'Model not available'}), 500
        
        # Make predictions
        results = ml_pipeline.predict(df)
        
        # Clean up
        os.remove(filepath)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': ml_pipeline.is_trained
    })

@app.route('/model-info')
def model_info():
    """Get information about the loaded model"""
    if ml_pipeline.is_trained:
        return jsonify({
            'model_loaded': True,
            'feature_count': len(ml_pipeline.feature_columns) if ml_pipeline.feature_columns else 0,
            'model_type': 'RandomForestClassifier with SMOTETomek'
        })
    else:
        return jsonify({
            'model_loaded': False,
            'message': 'Model not loaded'
        })

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File is too large. Maximum size is 16MB.')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Try to load the model on startup
    try:
        ml_pipeline.load_model()
        print("Model loaded successfully on startup")
    except Exception as e:
        print(f"Warning: Could not load model on startup: {e}")
        print("Model will be loaded when first prediction is requested")
    
    # Run the app
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
