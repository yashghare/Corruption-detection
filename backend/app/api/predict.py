from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path
import json
import numpy as np

router = APIRouter()

# Load artifacts
MODEL_DIR = Path(__file__).parent.parent / "model"
model = joblib.load(MODEL_DIR / "fraud_detection_model_v2.joblib")
with open(MODEL_DIR / "feature_schema_v2.json") as f:
    feature_schema = json.load(f)
with open(MODEL_DIR / "decision_thresholds_v2.json") as f:
    thresholds = json.load(f)

class TransactionRequest(BaseModel):
    transaction_id: str
    amount: float
    department: str
    supplier: str
    officer_id: str
    contract_duration: int
    bidding_process: str
    num_bidders: int
    winning_bid_ratio: float
    previous_contracts: int
    officer_tenure: float

@router.post("/predict")
async def predict(request: TransactionRequest, threshold: str = "default"):
    try:
        # Validate input
        if request.department not in feature_schema['categorical_mappings']['department']:
            raise HTTPException(status_code=400, detail=f"Invalid department. Allowed: {feature_schema['categorical_mappings']['department']}")
        
        if request.bidding_process not in feature_schema['categorical_mappings']['bidding_process']:
            raise HTTPException(status_code=400, detail=f"Invalid bidding process. Allowed: {feature_schema['categorical_mappings']['bidding_process']}")
        
        # Prepare features
        input_data = request.dict()
        features = pd.DataFrame([input_data])
        
        # Feature engineering
        features['amount_to_duration'] = features['amount'] / features['contract_duration']
        features['bidders_to_contracts'] = features['num_bidders'] / (features['previous_contracts'] + 1)
        
        # One-hot encoding
        features = pd.get_dummies(features)
        for col in feature_schema['required_features']:
            if col not in features.columns:
                features[col] = 0
        
        # Predict
        fraud_prob = model.predict_proba(features[feature_schema['required_features']])[0][1]
        threshold_value = thresholds.get(threshold, thresholds['default'])
        
        return {
            "transaction_id": request.transaction_id,
            "fraud_probability": round(fraud_prob, 4),
            "threshold_used": threshold_value,
            "is_flagged": fraud_prob > threshold_value,
            "threshold_type": threshold
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))