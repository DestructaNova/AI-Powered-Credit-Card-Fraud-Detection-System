# Credit Card Fraud Detection System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)](https://flask.palletsprojects.com/)
[![Machine Learning](https://img.shields.io/badge/ML-RandomForest-orange.svg)](https://scikit-learn.org/)

A machine learning web application for detecting credit card fraud using advanced algorithms and modern web technologies.

## Features

- **Web Interface**: User-friendly Bootstrap-based interface for CSV file uploads
- **Machine Learning**: Advanced fraud detection using RandomForest with SMOTETomek
- **Real-time Analysis**: Process transaction data and get instant fraud predictions
- **Detailed Results**: View fraudulent transactions with confidence scores
- **Export Functionality**: Download results as CSV files
- **Responsive Design**: Works on desktop and mobile devices
- **API Endpoints**: RESTful API for programmatic access

## Technology Stack

- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn, imbalanced-learn
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Data Processing**: pandas, numpy
- **Deployment**: Gunicorn, Render.com

## Project Structure

```
├── app.py                 # Main Flask application
├── ml_pipeline.py         # ML pipeline and model training
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
├── runtime.txt           # Python version specification
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   ├── 404.html
│   └── 500.html
├── static/               # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── model/                # Trained model artifacts
│   ├── fraud_model.pkl
│   ├── scaler.pkl
│   └── feature_columns.pkl
└── uploads/              # Temporary file uploads
```

## Dataset Requirements

The application expects CSV files with the following structure:

### Required Columns
- `Time`: Transaction time (numeric)
- `Amount`: Transaction amount (numeric)
- `V1` to `V28`: PCA-transformed features (numeric)

### Data Format
- All values must be numeric
- No missing values
- Standard CSV format with headers
- Maximum file size: 16MB

## API Endpoints

### Web Interface
- `GET /` - Main upload page
- `POST /upload` - Process uploaded CSV file
- `GET /health` - Health check endpoint
- `GET /model-info` - Model information

### API Endpoints
- `POST /api/predict` - JSON API for predictions


## Model Information

### Algorithm
- **Base Model**: RandomForestClassifier
- **Sampling**: SMOTETomek for handling class imbalance
- **Features**: 30 features (Time, Amount, V1-V28)
- **Preprocessing**: StandardScaler normalization

### Performance
- High accuracy on imbalanced fraud detection datasets
- Optimized for precision and recall balance
- Handles class imbalance effectively

## Usage Instructions

1. **Prepare your data**
   - Ensure CSV has required columns
   - Check data format and types
   - Remove any missing values

2. **Upload and analyze**
   - Go to the web interface
   - Upload your CSV file
   - Wait for analysis to complete

3. **Review results**
   - View fraud statistics
   - Examine flagged transactions
   - Export results if needed

## Troubleshooting

### Common Issues

1. **Model not found error**
   - Ensure model files exist in `model/` directory
   - Run `python ml_pipeline.py` to train the model

2. **CSV format errors**
   - Check column names and data types
   - Ensure no missing values
   - Verify file size is under 16MB

3. **Deployment issues**
   - Check Render logs for errors
   - Verify all dependencies in requirements.txt
   - Ensure Procfile is correctly configured

### Support

For issues and questions:
1. Check the application logs
2. Verify data format requirements
3. Ensure all dependencies are installed

## Acknowledgments

- Built using Flask and scikit-learn
- Bootstrap for responsive UI design
- Render.com for deployment platform
