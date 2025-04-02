from sklearn.ensemble import RandomForestClassifier
import joblib
from pathlib import Path
import json
import numpy as np

# Create model directory
model_dir = Path(__file__).parent.parent / "app" / "model"
model_dir.mkdir(exist_ok=True)

# Initialize a dummy model
model = RandomForestClassifier(n_estimators=10)
model.fit(np.random.rand(10, 5), np.random.randint(0, 2, 10))  # Dummy data

# Save artifacts
joblib.dump(model, model_dir / "fraud_detection_model.joblib")

# Create feature schema
feature_schema = {
    "required_features": [
        "amount", "contract_duration", "num_bidders", 
        "winning_bid_ratio", "previous_contracts", "officer_tenure",
        "amount_log", "contracts_per_bidder",
        "department_health", "department_education",
        "department_defense", "department_infrastructure",
        "bidding_process_open", "bidding_process_restricted", "bidding_process_direct"
    ],
    "categorical_mappings": {
        "department": ["health", "education", "defense", "infrastructure"],
        "bidding_process": ["open", "restricted", "direct"]
    }
}

with open(model_dir / "feature_schema.json", 'w') as f:
    json.dump(feature_schema, f, indent=2)

print("✅ Initialized model files at:", model_dir)