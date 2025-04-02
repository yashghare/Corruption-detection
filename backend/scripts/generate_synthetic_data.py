import pandas as pd
import numpy as np
from pathlib import Path
import json

# Configuration
CONFIG = {
    "n_samples": 30000,
    "fraud_rate": 0.08,
    "output_path": Path("backend/data/procurement_data_v2.csv"),
    "metadata_path": Path("backend/data/data_metadata.json")
}

# Feature distributions
DEPARTMENTS = ["health", "education", "defense", "infrastructure"]
BID_TYPES = ["open", "restricted", "direct"]
VENDORS = [f"Vendor-{i}" for i in range(1, 301)]

def generate_realistic_data():
    np.random.seed(42)
    
    # Core features
    data = pd.DataFrame({
        "transaction_id": [f"TX-{i:06d}" for i in range(CONFIG['n_samples'])],
        "amount": np.clip(np.random.gamma(shape=2, scale=50000, size=CONFIG['n_samples']), 1000, 500000),
        "contract_duration": np.random.choice([3,6,12,24,36], CONFIG['n_samples'], p=[0.1,0.3,0.4,0.15,0.05]),
        "department": np.random.choice(DEPARTMENTS, CONFIG['n_samples'], p=[0.5,0.3,0.15,0.05]),
        "bidding_process": np.random.choice(BID_TYPES, CONFIG['n_samples'], p=[0.7,0.2,0.1]),
        "num_bidders": np.where(np.random.rand(CONFIG['n_samples']) > 0.9, 
                             np.random.poisson(1, CONFIG['n_samples']) + 1,
                             np.random.poisson(4, CONFIG['n_samples']) + 1),
        "winning_bid_ratio": np.clip(np.random.beta(2, 5, CONFIG['n_samples']), 0.5, 1.0),
        "supplier": np.random.choice(VENDORS, CONFIG['n_samples']),
        "previous_contracts": np.random.poisson(2, CONFIG['n_samples']),
        "officer_id": [f"OFF-{np.random.randint(1000,9999)}" for _ in range(CONFIG['n_samples'])],
        "officer_tenure": np.clip(np.random.exponential(3, CONFIG['n_samples']), 0.1, 20),
        "is_fraud": 0
    })

    # Inject fraud
    fraud_idx = np.random.choice(
        CONFIG['n_samples'], 
        int(CONFIG['n_samples'] * CONFIG['fraud_rate']), 
        replace=False
    )
    data.loc[fraud_idx, "is_fraud"] = 1
    
    # Fraud patterns (not all frauds show all signs)
    for col in fraud_idx:
        if np.random.rand() > 0.3:
            data.at[col, "winning_bid_ratio"] = min(1.0, data.at[col, "winning_bid_ratio"] * 1.25)
        if np.random.rand() > 0.4:
            data.at[col, "num_bidders"] = max(1, data.at[col, "num_bidders"] - 2)
        if np.random.rand() > 0.5:
            data.at[col, "previous_contracts"] += np.random.randint(2,5)

    # Add legitimate anomalies
    clean_idx = data.index.difference(fraud_idx)
    outlier_mask = np.random.rand(len(clean_idx)) < 0.08
    data.loc[clean_idx[outlier_mask], "winning_bid_ratio"] = np.random.uniform(0.85, 1.0, sum(outlier_mask))

    # Save with metadata
    CONFIG['output_path'].parent.mkdir(exist_ok=True)
    data.to_csv(CONFIG['output_path'], index=False)
    
    metadata = {
        "generated_at": pd.Timestamp.now().isoformat(),
        "n_samples": len(data),
        "fraud_rate": data['is_fraud'].mean(),
        "feature_distributions": {
            "amount": {"min": data['amount'].min(), "max": data['amount'].max()},
            "num_bidders": dict(data['num_bidders'].value_counts(normalize=True))
        }
    }
    
    with open(CONFIG['metadata_path'], 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Generated {len(data)} records ({data['is_fraud'].mean():.2%} fraud)")
    print(f"Data: {CONFIG['output_path']}")
    print(f"Metadata: {CONFIG['metadata_path']}")

if __name__ == "__main__":
    generate_realistic_data()