import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import os

def train_model():
    # Set paths
    data_path = os.path.join('data', 'dataset.csv')
    model_path = os.path.join('model', 'model.pkl')
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    try:
        # Load the dataset
        df = pd.read_csv(data_path)
        print("Dataset loaded successfully!")
    except FileNotFoundError:
        print("Dataset not found. Creating sample dataset...")
        # Create sample dataset
        np.random.seed(42)
        X = np.random.rand(100, 4)
        y = 2 + 3*X[:, 0] + 4*X[:, 1] - 2*X[:, 2] + 0.5*X[:, 3] + np.random.normal(0, 0.5, 100)
        
        df = pd.DataFrame(X, columns=['feature1', 'feature2', 'feature3', 'feature4'])
        df['target'] = y
        
        # Save the sample dataset
        df.to_csv(data_path, index=False)
        print(f"Sample dataset created and saved to {data_path}")
    
    # Prepare features and target
    X = df.drop('target', axis=1).values
    y = df['target'].values
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate the model
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Model trained successfully!")
    print(f"Training Score (R²): {train_score:.4f}")
    print(f"Testing Score (R²): {test_score:.4f}")
    
    # Save the model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {model_path}")
    
    return model

if __name__ == "__main__":
    train_model()