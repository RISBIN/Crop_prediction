"""
Test the updated Django crop predictor with Random Forest model
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from apps.predictions.ml_services.crop_predictor import get_crop_predictor

def test_predictions():
    """Test the crop predictor with real samples."""

    print("=" * 70)
    print("TESTING DJANGO CROP PREDICTOR (Random Forest)")
    print("=" * 70)

    # Get predictor
    predictor = get_crop_predictor()

    # Test cases (same as in Kaggle notebook)
    test_cases = [
        {
            'name': 'Rice',
            'nitrogen': 90, 'phosphorus': 42, 'potassium': 43,
            'temperature': 21, 'humidity': 82, 'ph_value': 6.5, 'rainfall': 203
        },
        {
            'name': 'Maize',
            'nitrogen': 71, 'phosphorus': 54, 'potassium': 16,
            'temperature': 23, 'humidity': 64, 'ph_value': 5.7, 'rainfall': 88
        },
        {
            'name': 'Coffee',
            'nitrogen': 100, 'phosphorus': 25, 'potassium': 30,
            'temperature': 25, 'humidity': 58, 'ph_value': 6.8, 'rainfall': 150
        },
        {
            'name': 'Coconut',
            'nitrogen': 20, 'phosphorus': 10, 'potassium': 30,
            'temperature': 27, 'humidity': 94, 'ph_value': 6.0, 'rainfall': 175
        },
        {
            'name': 'Apple',
            'nitrogen': 20, 'phosphorus': 130, 'potassium': 200,
            'temperature': 22, 'humidity': 85, 'ph_value': 6.5, 'rainfall': 120
        },
    ]

    print(f"\nModel Info:")
    print(f"   Trained: {predictor.is_trained}")
    print(f"   Total Crops: {predictor.num_crops}")

    print(f"\nRunning {len(test_cases)} test cases...\n")

    correct = 0
    for i, test in enumerate(test_cases, 1):
        expected = test.pop('name')
        result = predictor.predict(test)

        print(f"{i}. Expected: {expected}")
        print(f"   Predicted: {result['predicted_crop']} ({result['confidence_percent']:.1f}%)")
        print(f"   Top-3:")
        for j, crop_info in enumerate(result['top_3_crops'], 1):
            print(f"      {j}. {crop_info['crop']:15s} {crop_info['confidence_percent']:5.1f}%")

        if result['predicted_crop'].lower() == expected.lower():
            print("   CORRECT!")
            correct += 1
        else:
            top3_names = [c['crop'].lower() for c in result['top_3_crops']]
            if expected.lower() in top3_names:
                print("   In Top-3")
            else:
                print("   Not in Top-3")
        print()

    print("=" * 70)
    print(f"Results: {correct}/{len(test_cases)} correct ({correct/len(test_cases)*100:.0f}%)")
    print("=" * 70)

if __name__ == '__main__':
    test_predictions()
