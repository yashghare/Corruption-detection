from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path
import numpy as np
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Model loading with validation
MODEL_PATH = Path(__file__).parent / "model" / "fraud_detection_model.joblib"

try:
    model = joblib.load(MODEL_PATH)
    logger.info(f"Model loaded successfully. Features expected: {model.feature_names_in_}")
except Exception as e:
    logger.error(f"Model loading failed: {str(e)}")
    raise RuntimeError("Failed to load model. Please retrain the model first.")

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    num_bidders: int
    winning_bid_ratio: float
    previous_contracts: int
    officer_tenure: float

@app.post("/predict")
async def predict(transaction: Transaction):
    try:
        # Prepare input with exact feature order
        input_data = [
            transaction.amount,
            transaction.num_bidders,
            transaction.winning_bid_ratio,
            transaction.previous_contracts,
            transaction.officer_tenure
        ]
        
        # Create DataFrame with correct column names
        features = pd.DataFrame([input_data], columns=model.feature_names_in_)
        
        # Predict
        proba = model.predict_proba(features)[0][1]
        
        return {
            "transaction_id": transaction.transaction_id,
            "fraud_probability": round(float(proba), 4),
            "is_flagged": proba > 0.7
        }
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return {
        "status": "running",
        "model_ready": True,
        "required_features": model.feature_names_in_.tolist()
    }

def start_server():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disabled to avoid warning
        log_level="info"
    )

if __name__ == "__main__":
    start_server()