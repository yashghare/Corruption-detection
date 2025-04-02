import joblib
import numpy as np
from pathlib import Path
from .preprocessing import preprocess_input

class FraudDetectionModel:
    def __init__(self, model_path="model/fraud_detection_model.joblib"):
        self.model = joblib.load(Path(__file__).parent.parent.parent / model_path)
        
    def predict(self, input_data):
        """Predict fraud probability and risk factors"""
        processed_data = preprocess_input(input_data)
        proba = self.model.predict_proba([processed_data])[0]
        prediction = self.model.predict([processed_data])[0]
        
        return {
            "is_fraud": bool(prediction),
            "confidence": float(proba[1]),  # Probability of fraud
            "risk_factors": self._get_risk_factors(input_data, processed_data)
        }
    
    def _get_risk_factors(self, raw_input, processed_data):
        """Generate human-readable risk factors"""
        risk_factors = []
        
        if raw_input["amount"] > 100000:
            risk_factors.append("High transaction amount (> $100,000)")
        if raw_input["winning_bid_ratio"] > 0.9:
            risk_factors.append("Suspicious winning bid ratio (> 90%)")
        if raw_input["num_bidders"] < 3:
            risk_factors.append("Low competition (< 3 bidders)")
            
        return risk_factors