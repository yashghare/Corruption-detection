import requests
import pandas as pd
from pathlib import Path

API_URL = "http://localhost:8000/predict"

def test_model():
    # Test data
    test_transactions = [
        {
            "transaction_id": "TEST-001",
            "amount": 150000,
            "department": "health",
            "bidding_process": "open",
            "num_bidders": 3,
            "winning_bid_ratio": 0.75,
            "previous_contracts": 2,
            "officer_tenure": 3.5
        },
        {
            "transaction_id": "TEST-002",
            "amount": 500000,
            "department": "defense",
            "bidding_process": "direct",
            "num_bidders": 1,
            "winning_bid_ratio": 0.95,
            "previous_contracts": 5,
            "officer_tenure": 0.5
        }
    ]

    print("Starting API tests...\n")
    
    for i, transaction in enumerate(test_transactions, 1):
        try:
            response = requests.post(API_URL, json=transaction)
            result = response.json()
            
            print(f"Test Case {i}:")
            print(f"Transaction: {transaction['transaction_id']}")
            print(f"Amount: ${transaction['amount']:,}")
            print(f"Fraud Probability: {result['fraud_probability']:.2%}")
            print(f"Flagged: {'✅' if result['is_flagged'] else '❌'}")
            print("-" * 40)
            
        except Exception as e:
            print(f"Error testing transaction {i}: {str(e)}")

if __name__ == "__main__":
    test_model()