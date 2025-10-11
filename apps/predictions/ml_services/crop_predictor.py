"""
Crop Prediction Service - 101 Crops Production Model
=====================================================
Uses trained Deep Learning model with 101 crops.
Provides Top-3 crop recommendations with confidence scores.
"""

import numpy as np
from typing import Dict, List, Tuple
import os
from pathlib import Path

# Lazy imports for ML libraries (loaded only when needed)
_tf = None
_keras = None
_joblib = None


def _load_ml_libraries():
    """Lazy load ML libraries to improve startup time."""
    global _tf, _keras, _joblib
    if _tf is None:
        import tensorflow as tf
        from tensorflow import keras
        import joblib
        _tf = tf
        _keras = keras
        _joblib = joblib
    return _tf, _keras, _joblib


class CropPredictor:
    """
    Production Crop Predictor Service.

    Features:
    - 101 crop classes (expanded from 22)
    - Deep Learning MLP model
    - Top-3 recommendations with confidence scores
    - Feature engineering (15 features from 7 inputs)
    """

    def __init__(self):
        """Initialize the crop predictor with trained model."""
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.is_trained = False
        self.num_crops = 101
        self.crops_list = []

        # Lazy loading - load model on first prediction
        self._model_loaded = False

    def _load_model(self):
        """Load the trained model and preprocessing artifacts."""
        if self._model_loaded:
            return

        try:
            # Load ML libraries
            tf, keras, joblib = _load_ml_libraries()

            # Get base directory
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            model_dir = base_dir / 'ml_models'

            # Check if models exist
            model_path = model_dir / 'best_crop_model.h5'
            scaler_path = model_dir / 'scaler.pkl'
            encoder_path = model_dir / 'label_encoder.pkl'

            if not model_path.exists():
                raise FileNotFoundError(f"Model not found at {model_path}")

            # Load model
            print(f"Loading crop prediction model from {model_path}...")
            self.model = keras.models.load_model(str(model_path))
            print("[OK] Model loaded successfully")

            # Load preprocessing artifacts
            self.scaler = joblib.load(str(scaler_path))
            self.label_encoder = joblib.load(str(encoder_path))

            # Get crop list
            self.crops_list = self.label_encoder.classes_.tolist()
            self.num_crops = len(self.crops_list)

            self.is_trained = True
            self._model_loaded = True

            print(f"[OK] Loaded {self.num_crops} crops: {', '.join(self.crops_list[:5])}...")

        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            print("[WARNING] Falling back to mock predictions")
            self.is_trained = False

    def predict(self, features: Dict[str, float]) -> Dict:
        """
        Predict the best crop based on input features.

        Args:
            features: Dictionary containing:
                - nitrogen (N): 0-200
                - phosphorus (P): 0-150
                - potassium (K): 0-500
                - temperature: -5 to 50°C
                - humidity: 10-100%
                - ph_value: 3-10
                - rainfall: 0-4000mm

        Returns:
            Dictionary with:
                - predicted_crop: Top recommendation
                - confidence_score: Confidence (0-1)
                - top_3_crops: List of top 3 with scores
                - num_total_crops: Total crops available
        """
        # Load model on first prediction
        if not self._model_loaded:
            self._load_model()

        # If model not loaded, use mock predictions
        if not self.is_trained or self.model is None:
            return self._mock_prediction(features)

        try:
            # Extract features
            N = features.get('nitrogen', 0)
            P = features.get('phosphorus', 0)
            K = features.get('potassium', 0)
            temperature = features.get('temperature', 0)
            humidity = features.get('humidity', 0)
            ph = features.get('ph_value', 0)
            rainfall = features.get('rainfall', 0)

            # Engineer features (same as training)
            X = self._engineer_features(N, P, K, temperature, humidity, ph, rainfall)

            # Scale features
            X_scaled = self.scaler.transform(X)

            # Predict probabilities
            proba = self.model.predict(X_scaled, verbose=0)[0]

            # Get top 3 predictions
            top3_idx = np.argsort(proba)[-3:][::-1]
            top3_crops = self.label_encoder.inverse_transform(top3_idx)
            top3_conf = proba[top3_idx]

            # Format results
            top_3 = [
                {
                    'crop': crop.capitalize(),
                    'score': float(conf),
                    'confidence_percent': float(conf * 100)
                }
                for crop, conf in zip(top3_crops, top3_conf)
            ]

            return {
                'predicted_crop': top_3[0]['crop'],
                'confidence_score': top_3[0]['score'],
                'confidence_percent': top_3[0]['confidence_percent'],
                'top_3_crops': top_3,
                'num_total_crops': self.num_crops,
                'all_crops_available': self.crops_list
            }

        except Exception as e:
            print(f"[ERROR] Prediction failed: {e}")
            return self._mock_prediction(features)

    def _engineer_features(self, N, P, K, temperature, humidity, ph, rainfall):
        """
        Engineer features to match training data.
        Transforms 7 input features into 15 features.
        """
        features = [
            N,
            P,
            K,
            temperature,
            humidity,
            ph,
            rainfall,
            # Engineered features
            N + P + K,  # NPK_sum
            N / (P + 0.01),  # N_P_ratio
            N / (K + 0.01),  # N_K_ratio
            P / (K + 0.01),  # P_K_ratio
            temperature * humidity / 100,  # temp_humidity
            rainfall * humidity / 100,  # rainfall_humidity
            self._encode_temperature_category(temperature),  # temp_cat_encoded
            self._encode_rainfall_category(rainfall)  # rain_cat_encoded
        ]

        return np.array(features).reshape(1, -1)

    def _encode_temperature_category(self, temp):
        """Encode temperature into categories."""
        if temp < 15:
            return 0  # cold
        elif temp < 25:
            return 1  # cool
        elif temp < 35:
            return 2  # warm
        else:
            return 3  # hot

    def _encode_rainfall_category(self, rainfall):
        """Encode rainfall into categories."""
        if rainfall < 100:
            return 0  # low
        elif rainfall < 200:
            return 1  # medium
        elif rainfall < 300:
            return 2  # high
        else:
            return 3  # very_high

    def _mock_prediction(self, features: Dict[str, float]) -> Dict:
        """
        Fallback mock prediction when model is not available.
        Uses simple rule-based logic.
        """
        import random

        CROPS = [
            'Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Chickpea',
            'Kidney Beans', 'Pigeon Peas', 'Banana', 'Mango', 'Grapes',
            'Orange', 'Papaya', 'Coconut', 'Pomegranate', 'Apple', 'Coffee',
            'Barley', 'Peas', 'Soybean', 'Sunflower', 'Potato', 'Tomato'
        ]

        # Extract features
        n = features.get('nitrogen', 0)
        p = features.get('phosphorus', 0)
        k = features.get('potassium', 0)
        temp = features.get('temperature', 0)
        humidity = features.get('humidity', 0)
        ph = features.get('ph_value', 0)
        rainfall = features.get('rainfall', 0)

        scores = {}

        # Simple rule-based scoring
        if rainfall > 150 and humidity > 70:
            scores['Rice'] = 0.85
        if 15 < temp < 25 and 50 < rainfall < 100:
            scores['Wheat'] = 0.80
        if k > 100 and temp > 25:
            scores['Cotton'] = 0.78
        if n > 90 and rainfall > 120:
            scores['Sugarcane'] = 0.82
        if 60 < n < 100 and 40 < p < 80:
            scores['Maize'] = 0.75

        # Add random crops if needed
        if not scores:
            for crop in random.sample(CROPS, 3):
                scores[crop] = round(random.uniform(0.6, 0.75), 2)

        # Ensure we have at least 3
        while len(scores) < 3:
            crop = random.choice([c for c in CROPS if c not in scores])
            scores[crop] = round(random.uniform(0.5, 0.65), 2)

        # Sort and get top 3
        sorted_crops = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

        top_3 = [
            {
                'crop': crop,
                'score': score,
                'confidence_percent': score * 100
            }
            for crop, score in sorted_crops
        ]

        return {
            'predicted_crop': top_3[0]['crop'],
            'confidence_score': top_3[0]['score'],
            'confidence_percent': top_3[0]['confidence_percent'],
            'top_3_crops': top_3,
            'num_total_crops': len(CROPS),
            'all_crops_available': CROPS
        }

    def get_crop_info(self, crop_name: str) -> Dict:
        """
        Get information about a specific crop.

        Args:
            crop_name: Name of the crop

        Returns:
            Dictionary with crop information
        """
        # This can be extended with crop database
        return {
            'name': crop_name.capitalize(),
            'scientific_name': 'N/A',
            'season': 'N/A',
            'duration': 'N/A'
        }


# Singleton instance
_predictor = None


def get_crop_predictor() -> CropPredictor:
    """
    Get or create the crop predictor singleton.

    Returns:
        CropPredictor instance
    """
    global _predictor
    if _predictor is None:
        _predictor = CropPredictor()
    return _predictor


def get_all_crops() -> List[str]:
    """
    Get list of all available crops.

    Returns:
        List of crop names
    """
    predictor = get_crop_predictor()
    if predictor.is_trained and predictor.crops_list:
        return [crop.capitalize() for crop in predictor.crops_list]
    else:
        # Fallback list
        return [
            'Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Barley',
            'Chickpea', 'Kidney Beans', 'Pigeon Peas', 'Lentil', 'Peas',
            'Banana', 'Mango', 'Grapes', 'Orange', 'Papaya', 'Coconut',
            'Pomegranate', 'Apple', 'Coffee', 'Soybean', 'Sunflower',
            'Potato', 'Tomato', 'Onion', 'Garlic'
        ]
