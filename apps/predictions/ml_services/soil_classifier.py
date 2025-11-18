"""
Soil Classification Service
This module handles soil classification using PyTorch ResNet18 CNN model.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Optional
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)


class SoilClassifier:
    """Service class for soil classification using PyTorch ResNet18."""

    SOIL_TYPES = {
        'black': 'Black Soil',
        'clay': 'Clay Soil',
        'loamy': 'Loamy Soil',
        'sandy': 'Sandy Soil'
    }

    def __init__(self):
        """Initialize the soil classifier."""
        self.model = None
        self.device = None
        self.transform = None
        self.is_trained = False
        self.metadata = None
        self.class_names = ['black', 'clay', 'loamy', 'sandy']

        # Try to load model
        try:
            self._load_model()
        except Exception as e:
            logger.warning(f"[WARNING] Could not load soil classification model: {str(e)}")
            logger.warning("[WARNING] Using fallback mode - model predictions will not be available")

    def _load_model(self):
        """Load the PyTorch model and metadata."""
        # Lazy imports - only import when needed
        import torch
        from torchvision import models, transforms
        import torch.nn as nn

        # Get model path from settings or use default
        from django.conf import settings
        model_dir = getattr(settings, 'SOIL_MODEL_PATH', 'ml_models/soil_classifier/v1.0')

        # Build paths
        base_dir = Path(settings.BASE_DIR)
        model_path = base_dir / model_dir / 'model.pth'
        metadata_path = base_dir / model_dir / 'metadata.json'

        # Check if files exist
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

        # Load metadata
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)

        logger.info(f"[INFO] Loading soil classifier model from {model_path}")

        # Set device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Create model architecture (must match training)
        model = models.resnet18(pretrained=False)
        num_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(256, 4)  # 4 soil classes
        )

        # Load trained weights
        state_dict = torch.load(model_path, map_location=self.device)
        model.load_state_dict(state_dict)
        model.to(self.device)
        model.eval()

        self.model = model

        # Define transforms (must match training)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        self.is_trained = True
        val_acc = self.metadata.get('val_accuracy', 0)
        logger.info(f"[SUCCESS] Soil classifier loaded! Validation accuracy: {val_acc:.2f}%")

    def classify(self, image_path: str) -> Dict:
        """
        Classify soil type from image.

        Args:
            image_path: Path to the soil image

        Returns:
            Dictionary with soil_type, confidence_score, and all_predictions
        """
        if not self.is_trained:
            raise RuntimeError(
                "Soil classification model not loaded. "
                "Please ensure model files exist at ml_models/soil_classifier/v1.0/"
            )

        # Load and preprocess image
        try:
            img = Image.open(image_path).convert('RGB')
        except Exception as e:
            raise ValueError(f"Error loading image: {str(e)}")

        # Preprocess
        img_tensor = self.transform(img).unsqueeze(0).to(self.device)

        # Make prediction
        import torch
        with torch.no_grad():
            outputs = self.model(img_tensor)
            probabilities = torch.softmax(outputs, dim=1)[0]
            predicted_idx = torch.argmax(probabilities).item()
            confidence = probabilities[predicted_idx].item()

        # Get predicted soil type
        predicted_soil = self.class_names[predicted_idx]

        # Create predictions dictionary
        all_predictions = {
            soil: float(probabilities[i].item())
            for i, soil in enumerate(self.class_names)
        }

        logger.info(f"[PREDICTION] Soil type: {predicted_soil} ({confidence*100:.2f}%)")

        return {
            'soil_type': predicted_soil,
            'confidence_score': confidence,
            'all_predictions': all_predictions,
            'soil_type_label': self.SOIL_TYPES[predicted_soil]
        }

    def get_model_info(self) -> Dict:
        """Get information about the loaded model."""
        if not self.is_trained:
            return {
                'loaded': False,
                'message': 'Model not loaded'
            }

        return {
            'loaded': True,
            'model_type': self.metadata.get('model_type', 'Unknown'),
            'validation_accuracy': self.metadata.get('val_accuracy', 0),
            'training_date': self.metadata.get('training_date', 'Unknown'),
            'num_classes': len(self.class_names),
            'classes': self.class_names,
            'device': str(self.device)
        }


# Singleton instance
_classifier: Optional[SoilClassifier] = None


def get_soil_classifier() -> SoilClassifier:
    """Get or create the soil classifier singleton."""
    global _classifier
    if _classifier is None:
        _classifier = SoilClassifier()
    return _classifier
