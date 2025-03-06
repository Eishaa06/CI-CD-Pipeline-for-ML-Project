import unittest
import json
import os
import sys

# Fix path handling - use absolute paths and insert at position 0
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Try importing after path setup
try:
    from app.app import app
    from model.train import train_model
except ImportError as e:
    print(f"Import error: {e}")
    raise

class TestApp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Use absolute path for model
        model_path = os.path.join(project_root, 'model', 'model.pkl')
        print(f"Looking for model at: {model_path}")
        if not os.path.exists(model_path):
            print("Model not found. Training new model...")
            train_model()
            if not os.path.exists(model_path):
                print(f"Warning: Model still not found at {model_path} after training")
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ML Model", response.data)
    
    def test_health_endpoint(self):
        response = self.app.get('/health')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
    
    def test_predict_endpoint(self):
        test_data = {
            'feature1': 0.5,
            'feature2': 0.5,
            'feature3': 0.5,
            'feature4': 0.5
        }
        response = self.app.post('/predict',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('prediction', data)
        self.assertIsInstance(data['prediction'], (int, float))
    
    def test_predict_bad_input(self):
        # Test with missing features
        test_data = {'feature1': 0.5}
        response = self.app.post('/predict',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)  # Should still work with defaults
        
        # Test with non-numeric data
        test_data = {'feature1': 'not_a_number', 'feature2': 0.5, 'feature3': 0.5, 'feature4': 0.5}
        response = self.app.post('/predict',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 400)  # Should return bad request

if __name__ == '__main__':
    unittest.main()