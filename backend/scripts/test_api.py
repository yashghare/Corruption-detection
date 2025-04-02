import requests
import json
from requests.exceptions import RequestException

API_URL = "http://localhost:8000/predict"

def run_test_case(test_data):
    try:
        print(f"\nTesting transaction: {test_data['transaction_id']}")
        print("Input data:", json.dumps(test_data, indent=2))
        
        response = requests.post(API_URL, json=test_data, timeout=5)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Prediction Result:")
            print(f"Fraud Probability: {result['fraud_probability']:.2%}")
            print(f"Flagged: {'✅' if result['is_flagged'] else '❌'}")
        else:
            print(f"Error Response: {response.text}")
            
    except RequestException as e:
        print(f"Request failed: {str(e)}")
    except json.JSONDecodeError:
        print(f"Invalid JSON response: {response.text}")

def main():
    test_cases = [
        {
            "transaction_id": "TEST-001",
            "amount": 150000,
            "num_bidders": 3,
            "winning_bid_ratio": 0.75,
            "previous_contracts": 2,
            "officer_tenure": 3.5
        },
        {
            "transaction_id": "TEST-002",
            "amount": 500000,
            "num_bidders": 1,
            "winning_bid_ratio": 0.95,
            "previous_contracts": 5,
            "officer_tenure": 0.5
        }
    ]

    print("Starting API Tests...")
    for case in test_cases:
        run_test_case(case)
        print("-" * 60)

if __name__ == "__main__":
    main()