"""
Soil Classification Service
This module handles soil classification using PyTorch CNN model.
Currently using mock predictions - will be replaced with trained model.
"""

import random
from typing import Dict
from PIL import Image
import numpy as np


class SoilClassifier:
    """Service class for soil classification."""

    SOIL_TYPES = {
        'black': 'Black Soil',
        'clay': 'Clay Soil',
        'loamy': 'Loamy Soil',
        'sandy': 'Sandy Soil'
    }

    def __init__(self):
        """Initialize the soil classifier."""
        self.model = None  # Will load actual PyTorch model here
        self.is_trained = False

    def classify(self, image_path: str) -> Dict:
        """
        Classify soil type from image.

        Args:
            image_path: Path to the soil image

        Returns:
            Dictionary with soil_type, confidence_score, and all_predictions
        """
        # Load and preprocess image
        try:
            img = Image.open(image_path)
            # In actual implementation, we would:
            # - Resize to 224x224
            # - Normalize
            # - Convert to tensor
            # - Pass through model
        except Exception as e:
            raise ValueError(f"Error loading image: {str(e)}")

        # Mock prediction (will be replaced with actual model)
        soil_type, predictions = self._mock_classification()

        return {
            'soil_type': soil_type,
            'confidence_score': predictions[soil_type],
            'all_predictions': predictions
        }

    def _mock_classification(self) -> tuple:
        """
        Mock classification logic (will be replaced with actual model).
        Returns random soil type with mock probabilities.
        """
        # Generate random probabilities that sum to ~1.0
        soil_types = list(self.SOIL_TYPES.keys())

        # Pick a winner
        winner = random.choice(soil_types)

        # Generate probabilities
        predictions = {}
        remaining = 1.0

        for soil in soil_types:
            if soil == winner:
                predictions[soil] = round(random.uniform(0.6, 0.9), 2)
            else:
                max_val = remaining - predictions.get(winner, 0.7)
                if max_val > 0:
                    predictions[soil] = round(random.uniform(0.05, min(0.3, max_val)), 2)
                else:
                    predictions[soil] = 0.05
            remaining -= predictions[soil]

        # Normalize to sum to 1.0
        total = sum(predictions.values())
        predictions = {k: round(v/total, 2) for k, v in predictions.items()}

        return winner, predictions


# Singleton instance
_classifier = None

def get_soil_classifier() -> SoilClassifier:
    """Get or create the soil classifier singleton."""
    global _classifier
    if _classifier is None:
        _classifier = SoilClassifier()
    return _classifier
