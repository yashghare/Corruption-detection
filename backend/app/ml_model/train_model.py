import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from pathlib import Path
import json

# Configuration
MODEL_DIR = Path(__file__).parent.parent / "model"
MODEL_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODEL_DIR / "fraud_detection_model.joblib"
DATA_PATH = Path(__file__).parent.parent.parent / "data" / "procurement_data.csv"

def load_data():
    """Load and preprocess data"""
    df = pd.read_csv(DATA_PATH)
    df['is_fraud'] = df['is_fraud'].astype(int)
    
    # Select only the features we want to use
    features = [
        'amount',
        'num_bidders',
        'winning_bid_ratio',
        'previous_contracts',
        'officer_tenure',
        'is_fraud'
    ]
    df = df[features]
    
    return df

def train_and_evaluate():
    df = load_data()
    
    # Features and target
    X = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight='balanced',
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    
    # Save model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_and_evaluate()