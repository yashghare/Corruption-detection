# backend/app/ml_model/train_model.py
import pandas as pd
from .model import FraudDetectionModel

def train_and_save_model():
    # Sample data - in practice, you would use real procurement data
    data = {
        'transaction_id': [f'tx-{i}' for i in range(1000)],
        'department': ['health', 'education', 'transport', 'defense', 'infrastructure'] * 200,
        'contract_value': [10000 + i * 100 for i in range(1000)],
        'supplier': ['supplierA', 'supplierB', 'supplierC', 'supplierD', 'supplierE'] * 200,
        'contract_duration': [12 + (i % 24) for i in range(1000)],
        'bidding_process': ['open', 'restricted', 'direct', 'negotiated'] * 250,
        'num_bidders': [3 + (i % 5) for i in range(1000)],
        'winning_bid_ratio': [0.8 + (i * 0.002 % 0.4) for i in range(1000)],
        'previous_contracts': [i % 10 for i in range(1000)],
        'officer_tenure': [1 + (i % 20) for i in range(1000)],
        'is_fraud': [i % 20 == 0 for i in range(1000)]  # 5% fraud rate for example
    }
    
    df = pd.DataFrame(data)
    df.to_csv('procurement_data.csv', index=False)
    
    model = FraudDetectionModel()
    model.train('procurement_data.csv')
    print("Model trained and saved successfully!")

if __name__ == "__main__":
    train_and_save_model()