# backend/app/ml_model/model.py
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from .preprocessing import preprocess_data

class FraudDetectionModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.features = [
            'contract_value', 'contract_duration', 'num_bidders', 
            'winning_bid_ratio', 'previous_contracts', 'officer_tenure'
        ]
        self.categorical_features = ['department', 'supplier', 'bidding_process']
        
    def train(self, data_path):
        df = pd.read_csv(data_path)
        X, y = preprocess_data(df, self.features, self.categorical_features)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
        
        joblib.dump(self.model, 'fraud_detection_model.pkl')
        joblib.dump(self.features, 'model_features.pkl')
        joblib.dump(self.categorical_features, 'model_categorical_features.pkl')
        
    def predict(self, transaction_data):
        model = joblib.load('fraud_detection_model.pkl')
        features = joblib.load('model_features.pkl')
        categorical_features = joblib