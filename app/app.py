from flask import Flask, request, jsonify
import sys
import os

# Add parent directory to path to import from model package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.predict import predict

app = Flask(__name__)

@app.route('/')
def home():
    return "ML Model Prediction API - Welcome!"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    try:
        data = request.get_json(force=True)
        
        # Extract features from request
        features = [
            float(data.get('feature1', 0)),
            float(data.get('feature2', 0)),
            float(data.get('feature3', 0)),
            float(data.get('feature4', 0))
        ]
        
        # Get prediction
        prediction = predict(features)
        
        # Return response
        return jsonify({
            'prediction': prediction,
            'features': features
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)