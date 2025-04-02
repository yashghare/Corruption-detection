# backend/app/ml_model/preprocessing.py
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def preprocess_data(df, numerical_features, categorical_features):
    """
    Preprocesses the procurement data for model training/prediction
    
    Args:
        df: Pandas DataFrame containing the raw data
        numerical_features: List of numerical feature names
        categorical_features: List of categorical feature names
        
    Returns:
        X: Processed feature matrix
        y: Target variable (if present in df)
    """
    # Create a copy to avoid modifying the original dataframe
    df = df.copy()
    
    # Define target variable if present
    y = None
    if 'is_fraud' in df.columns:
        y = df['is_fraud'].values
        df = df.drop(columns=['is_fraud'])
    
    # Create preprocessing pipelines
    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    # Apply preprocessing
    X = preprocessor.fit_transform(df)
    
    return X, y