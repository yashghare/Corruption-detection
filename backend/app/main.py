from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

app = FastAPI()

class TransactionData(BaseModel):
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
    officer_tenure: int
    
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test endpoint
@app.get("/api/test")
async def test_endpoint():
    return {"status": "success", "message": "API is working!"}

@app.post("/api/detect")
async def detect_fraud(transaction: TransactionData):
    # Your detection logic here
    return {
        "transaction_id": transaction.transaction_id,
        "is_fraud": False,  # Replace with actual detection
        "confidence": 0.95
    }
# Root endpoint
@app.get("/")
async def root():
    return {"message": "Backend is running"}

@app.post("/api/detect-fraud")
async def detect_fraud(data: TransactionData):
    # Your ML model integration here
    risk_factors = []
    
    # Example risk factors (replace with actual model logic)
    if data.amount > 100000:
        risk_factors.append("Unusually high transaction amount")
    if data.winning_bid_ratio > 0.9:
        risk_factors.append("Suspiciously high winning bid ratio")
    if data.previous_contracts > 5:
        risk_factors.append("Repeated contracts with same supplier")
    if data.officer_tenure < 1:
        risk_factors.append("New procurement officer with short tenure")
    
    is_fraud = len(risk_factors) >= 2  # Simple threshold logic
    
    return {
        "transaction_id": data.transaction_id,
        "amount": data.amount,
        "department": data.department,
        "is_fraud": is_fraud,
        "confidence": 0.95 if is_fraud else 0.15,  # Replace with model confidence
        "risk_factors": risk_factors if is_fraud else ["No significant risk factors"],
        "timestamp": datetime.datetime.now().isoformat()
    }