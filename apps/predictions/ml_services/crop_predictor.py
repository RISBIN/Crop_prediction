"""
Crop Prediction Service
This module handles crop prediction using XGBoost model.
Currently using mock predictions - will be replaced with trained model.
"""

import numpy as np
from typing import Dict, List, Tuple
import random


class CropPredictor:
    """Service class for crop prediction."""

    CROPS = [
        'Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Pulses',
        'Millets', 'Soybean', 'Groundnut', 'Sunflower', 'Chickpea',
        'Kidney Beans', 'Pigeon Peas', 'Banana', 'Mango', 'Grapes',
        'Orange', 'Papaya', 'Coconut', 'Pomegranate', 'Apple', 'Coffee'
    ]

    def __init__(self):
        """Initialize the crop predictor."""
        self.model = None  # Will load actual model here
        self.is_trained = False

    def predict(self, features: Dict[str, float]) -> Dict:
        """
        Predict the best crop based on input features.

        Args:
            features: Dictionary containing N, P, K, temperature, humidity, ph, rainfall

        Returns:
            Dictionary with predicted_crop, confidence_score, and top_3_crops
        """
        # Extract features
        nitrogen = features.get('nitrogen', 0)
        phosphorus = features.get('phosphorus', 0)
        potassium = features.get('potassium', 0)
        temperature = features.get('temperature', 0)
        humidity = features.get('humidity', 0)
        ph = features.get('ph_value', 0)
        rainfall = features.get('rainfall', 0)

        # Mock prediction logic based on simple rules
        # This will be replaced with actual ML model
        predicted_crop, top_crops = self._mock_prediction(
            nitrogen, phosphorus, potassium, temperature,
            humidity, ph, rainfall
        )

        return {
            'predicted_crop': predicted_crop,
            'confidence_score': round(random.uniform(0.75, 0.95), 2),
            'top_3_crops': top_crops
        }

    def _mock_prediction(self, n, p, k, temp, humidity, ph, rainfall) -> Tuple[str, List[Dict]]:
        """
        Mock prediction logic (will be replaced with actual model).
        Uses simple rules based on NPK values and climate.
        """
        scores = {}

        # Rice: High water, moderate NPK
        if rainfall > 150 and humidity > 70:
            scores['Rice'] = 0.9

        # Wheat: Moderate water, cooler climate
        if 15 < temp < 25 and 50 < rainfall < 100:
            scores['Wheat'] = 0.85

        # Cotton: High K, warm climate
        if k > 100 and temp > 25:
            scores['Cotton'] = 0.82

        # Sugarcane: High N, high rainfall
        if n > 90 and rainfall > 120:
            scores['Sugarcane'] = 0.88

        # Pulses: Moderate NPK, less water
        if 40 < n < 80 and rainfall < 80:
            scores['Pulses'] = 0.80

        # Maize: Balanced NPK, moderate conditions
        if 60 < n < 100 and 40 < p < 80:
            scores['Maize'] = 0.83

        # If no specific match, add some random crops
        if not scores:
            for crop in random.sample(self.CROPS, 3):
                scores[crop] = round(random.uniform(0.6, 0.8), 2)

        # Sort by score and get top 3
        sorted_crops = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

        # Ensure we have at least 3 crops
        while len(sorted_crops) < 3:
            random_crop = random.choice([c for c in self.CROPS if c not in [x[0] for x in sorted_crops]])
            sorted_crops.append((random_crop, round(random.uniform(0.5, 0.7), 2)))

        top_3 = [{'crop': crop, 'score': score} for crop, score in sorted_crops[:3]]

        return sorted_crops[0][0], top_3


# Singleton instance
_predictor = None

def get_crop_predictor() -> CropPredictor:
    """Get or create the crop predictor singleton."""
    global _predictor
    if _predictor is None:
        _predictor = CropPredictor()
    return _predictor
