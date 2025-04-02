import joblib
import pandas as pd
from pathlib import Path

model = joblib.load(Path(__file__).parent.parent / "model" / "fraud_detection_model.joblib")

def test_prediction():
    """Test case matching your training data structure"""
    test_data = {
        'amount': 120000,
        'contract_duration': 18,
        'num_bidders': 2,
        'winning_bid_ratio': 0.92,
        'previous_contracts': 4,
        'officer_tenure': 1.5,
        'department_health': True,
        'department_education': False,
        'department_defense': False,
        'department_infrastructure': False,
        'department_transport': False,
        'bidding_process_open': False,
        'bidding_process_restricted': True,
        'bidding_process_direct': False,
        'bidding_process_negotiated': False
    }
    
    # Convert to DataFrame
    X = pd.DataFrame([test_data])
    
    # Predict
    proba = model.predict_proba(X)[0][1]  # Probability of fraud
    print(f"\nTest Case Fraud Probability: {proba:.1%}")
    
    if proba > 0.7:
        print("ALERT: High fraud risk detected!")
    else:
        print("Status: Normal transaction")

if __name__ == "__main__":
    test_prediction()