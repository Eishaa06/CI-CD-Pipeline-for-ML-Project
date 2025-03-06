import unittest
import os
import sys
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.train import train_model
from model.predict import predict, load_model

class TestModel(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Train model if it doesn't exist
        model_path = os.path.join('model', 'model.pkl')
        if not os.path.exists(model_path):
            train_model()
    
    def test_model_exists(self):
        model_path = os.path.join('model', 'model.pkl')
        self.assertTrue(os.path.exists(model_path), f"Model file not found at {model_path}")
    
    def test_model_loading(self):
        model = load_model()
        self.assertIsNotNone(model, "Model failed to load")
    
    def test_model_prediction(self):
        # Test single prediction
        features = [0.5, 0.5, 0.5, 0.5]
        prediction = predict(features)
        self.assertIsInstance(prediction, float, "Prediction should be a float")
    
    def test_model_prediction_batch(self):
        # Test that model can handle multiple feature sets
        model = load_model()
        features = np.random.rand(5, 4)  # 5 samples with 4 features each
        predictions = model.predict(features)
        self.assertEqual(len(predictions), 5, "Should return 5 predictions")

if __name__ == '__main__':
    unittest.main()