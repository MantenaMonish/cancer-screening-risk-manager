from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Constants
SCREENING_WINDOW = 30  # days to look ahead for reminders
DATA_PATH = "data/patients.csv"
MODEL_DIR = "models"

# Ensure model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

def load_and_clean_data(filepath):
    """Load patient data and perform cleaning"""
    df = pd.read_csv(filepath)
    
    # Convert dates
    date_cols = ['last_breast_screen', 'last_cervical_screen', 'last_colorectal_screen']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
    
    # Handle missing values
    df['family_history'].fillna('None', inplace=True)
    df['lifestyle'].fillna('Unknown', inplace=True)
    
    # Create binary flags
    df['is_smoker'] = df['lifestyle'].apply(lambda x: 1 if 'smoker' in x.lower() else 0)
    df['alcohol_consumer'] = df['lifestyle'].apply(lambda x: 1 if 'alcohol' in x.lower() else 0)
    df['obese'] = df['lifestyle'].apply(lambda x: 1 if 'obese' in x.lower() else 0)
    
    # Create family history features
    df['fh_Breast'] = df['family_history'].apply(lambda x: 1 if 'breast' in x.lower() else 0)
    df['fh_Cervical'] = df['family_history'].apply(lambda x: 1 if 'cervical' in x.lower() else 0)
    df['fh_Colorectal'] = df['family_history'].apply(
        lambda x: 1 if any(word in x.lower() for word in ['colorectal', 'colon']) else 0
    )
    
    return df

def train_or_load_risk_model(cancer_type, df):
    """Train or load ML model for specific cancer risk stratification"""
    model_path = os.path.join(MODEL_DIR, f"{cancer_type.lower()}_model.pkl")
    
    # Try to load existing model
    if os.path.exists(model_path):
        print(f"Loading existing {cancer_type} model")
        return joblib.load(model_path)
    
    # Feature engineering
    df = df.copy()
    df['age'] = pd.to_numeric(df['age'])
    
    # Prepare features and target
    if cancer_type == "Breast":
        features = ['age', 'gender', 'fh_Breast', 'is_smoker', 'obese']
        target = 'risk_breast'
    elif cancer_type == "Cervical":
        features = ['age', 'gender', 'fh_Cervical', 'is_smoker', 'obese']
        target = 'risk_cervical'
    elif cancer_type == "Colorectal":
        features = ['age', 'gender', 'fh_Colorectal', 'alcohol_consumer', 'obese']
        target = 'risk_colorectal'
    else:
        raise ValueError(f"Unknown cancer type: {cancer_type}")
    
    # Check if target exists
    if target not in df.columns:
        raise KeyError(f"Required column '{target}' not found in data")
    
    X = pd.get_dummies(df[features], columns=['gender'])
    y = df[target]
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    print(f"{cancer_type} Model - Train Acc: {train_acc:.2f}, Test Acc: {test_acc:.2f}")
    
    # Save model
    joblib.dump(model, model_path)
    print(f"Saved {cancer_type} model to {model_path}")
    
    return model

def calculate_risk_levels(df, breast_model, cervical_model, colorectal_model):
    """Calculate risk levels for all patients"""
    # Breast cancer risk
    breast_features = pd.get_dummies(df[['age', 'gender', 'fh_Breast', 'is_smoker', 'obese']], columns=['gender'])
    df['breast_risk'] = breast_model.predict(breast_features)
    
    # Cervical cancer risk
    cervical_features = pd.get_dummies(df[['age', 'gender', 'fh_Cervical', 'is_smoker', 'obese']], columns=['gender'])
    df['cervical_risk'] = cervical_model.predict(cervical_features)
    
    # Colorectal cancer risk
    colorectal_features = pd.get_dummies(df[['age', 'gender', 'fh_Colorectal', 'alcohol_consumer', 'obese']], columns=['gender'])
    df['colorectal_risk'] = colorectal_model.predict(colorectal_features)
    
    return df

def get_screening_interval(cancer_type, risk_level, gender, age):
    """Determine screening interval based on guidelines"""
    if cancer_type == "Breast":
        if gender != "Female":
            return None  # Only females are screened for breast cancer
        if risk_level == "High":
            return 1  # years
        elif risk_level == "Medium":
            return 2
        else:  # Low risk
            return 3
    
    elif cancer_type == "Cervical":
        if gender != "Female":
            return None  # Only females are screened for cervical cancer
        if risk_level == "High":
            return 1
        elif risk_level == "Medium":
            return 3
        else:  # Low risk
            return 5
    
    elif cancer_type == "Colorectal":
        if age < 45:
            return None  # Not eligible
        if risk_level == "High":
            return 5
        else:  # Medium/Low risk
            return 10
    
    return None

def next_screening_due(last_screen_date, interval_years, today):
    """Calculate next due date"""
    if pd.isna(last_screen_date) or last_screen_date is None:
        return today  # Immediately due if never screened
    
    # Calculate next due date and adjust if it's in the past
    due_date = last_screen_date + timedelta(days=interval_years*365)
    return max(due_date, today)  # Ensure due date isn't in the past

def generate_reminders(df, today):
    """Generate screening reminders for all patients"""
    reminders = []
    
    for _, row in df.iterrows():
        # Breast cancer screening
        interval = get_screening_interval(
            "Breast", row['breast_risk'], row['gender'], row['age']
        )
        if interval:
            due_date = next_screening_due(row['last_breast_screen'], interval, today)
            if due_date <= today + timedelta(days=SCREENING_WINDOW):
                reminders.append({
                    'patient_id': row['patient_id'],
                    'name': row['name'],
                    'type': 'Breast Cancer Screening',
                    'due_date': due_date.strftime('%Y-%m-%d'),
                    'risk': row['breast_risk'],
                    'last_screen': row['last_breast_screen'].strftime('%Y-%m-%d') if not pd.isna(row['last_breast_screen']) else 'Never'
                })
        
        # Cervical cancer screening
        interval = get_screening_interval(
            "Cervical", row['cervical_risk'], row['gender'], row['age']
        )
        if interval:
            due_date = next_screening_due(row['last_cervical_screen'], interval, today)
            if due_date <= today + timedelta(days=SCREENING_WINDOW):
                reminders.append({
                    'patient_id': row['patient_id'],
                    'name': row['name'],
                    'type': 'Cervical Cancer Screening',
                    'due_date': due_date.strftime('%Y-%m-%d'),
                    'risk': row['cervical_risk'],
                    'last_screen': row['last_cervical_screen'].strftime('%Y-%m-%d') if not pd.isna(row['last_cervical_screen']) else 'Never'
                })
        
        # Colorectal cancer screening
        interval = get_screening_interval(
            "Colorectal", row['colorectal_risk'], row['gender'], row['age']
        )
        if interval:
            due_date = next_screening_due(row['last_colorectal_screen'], interval, today)
            if due_date <= today + timedelta(days=SCREENING_WINDOW):
                reminders.append({
                    'patient_id': row['patient_id'],
                    'name': row['name'],
                    'type': 'Colorectal Cancer Screening',
                    'due_date': due_date.strftime('%Y-%m-%d'),
                    'risk': row['colorectal_risk'],
                    'last_screen': row['last_colorectal_screen'].strftime('%Y-%m-%d') if not pd.isna(row['last_colorectal_screen']) else 'Never'
                })
    
    return reminders

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    today = datetime.now().date()
    
    try:
        # Load and clean data
        df = load_and_clean_data(DATA_PATH)
        
        # Train or load models
        breast_model = train_or_load_risk_model("Breast", df)
        cervical_model = train_or_load_risk_model("Cervical", df)
        colorectal_model = train_or_load_risk_model("Colorectal", df)
        
        # Calculate risks
        df_with_risks = calculate_risk_levels(df, breast_model, cervical_model, colorectal_model)
        
        # Generate reminders
        reminders = generate_reminders(df_with_risks, today)
        
        return jsonify({
            'status': 'success',
            'date': today.strftime('%Y-%m-%d'),
            'reminders': reminders
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/patients', methods=['GET'])
def get_patients():
    try:
        df = load_and_clean_data(DATA_PATH)
        patients = df.to_dict(orient='records')
        return jsonify({
            'status': 'success',
            'patients': patients
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)