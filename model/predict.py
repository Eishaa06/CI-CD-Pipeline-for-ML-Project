import pickle
import numpy as np
import os

def load_model():
    model_path = os.path.join('model', 'model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def predict(features):
    """
    Make predictions using the trained model
    
    Args:
        features (list or array): List of feature values [feature1, feature2, feature3, feature4]
        
    Returns:
        float: Predicted value
    """
    model = load_model()
    features_array = np.array(features).reshape(1, -1)
    prediction = model.predict(features_array)[0]
    return float(prediction)

if __name__ == "__main__":
    # Example prediction
    sample_features = [0.5, 0.5, 0.5, 0.5]
    result = predict(sample_features)
    print(f"Prediction for {sample_features}: {result:.4f}")