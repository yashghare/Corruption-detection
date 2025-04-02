import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_input(input_data):
    """Preprocess incoming API request data for model prediction"""
    # Convert to DataFrame for easier manipulation
    data = pd.DataFrame([input_data])
    
    # One-hot encode categorical variables
    data = pd.get_dummies(data, columns=['department', 'bidding_process'])
    
    # Ensure all expected columns are present
    expected_columns = [
        'amount', 'contract_duration', 'num_bidders', 
        'winning_bid_ratio', 'previous_contracts', 'officer_tenure',
        'department_health', 'department_education', 'department_defense',
        'department_infrastructure', 'bidding_process_open',
        'bidding_process_restricted', 'bidding_process_direct',
        'bidding_process_negotiated'
    ]
    
    for col in expected_columns:
        if col not in data.columns:
            data[col] = 0
    
    # Select features in correct order
    features = data[expected_columns]
    
    # Scale numerical features (assuming scaler was fit during training)
    numerical_cols = [
        'amount', 'contract_duration', 'num_bidders',
        'winning_bid_ratio', 'previous_contracts', 'officer_tenure'
    ]
    scaler = StandardScaler()
    features[numerical_cols] = scaler.fit_transform(features[numerical_cols])
    
    return features.values[0]