"""
Test Django predictor with user-provided samples
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from apps.predictions.ml_services.crop_predictor import get_crop_predictor

def test_samples():
    """Test with user-provided samples."""

    print("=" * 80)
    print("TESTING DJANGO CROP PREDICTOR - User Samples")
    print("=" * 80)

    predictor = get_crop_predictor()

    # User test cases
    test_cases = [
        {'name': 'rice', 'nitrogen': 90, 'phosphorus': 42, 'potassium': 43, 'temperature': 20.8, 'humidity': 82, 'ph_value': 6.5, 'rainfall': 202.9},
        {'name': 'rice', 'nitrogen': 85, 'phosphorus': 58, 'potassium': 41, 'temperature': 21.7, 'humidity': 80, 'ph_value': 6.4, 'rainfall': 226.6},
        {'name': 'jute', 'nitrogen': 40, 'phosphorus': 55, 'potassium': 60, 'temperature': 18.9, 'humidity': 72, 'ph_value': 6.8, 'rainfall': 250.2},
        {'name': 'sugarcane', 'nitrogen': 12, 'phosphorus': 20, 'potassium': 25, 'temperature': 27.2, 'humidity': 80, 'ph_value': 6.4, 'rainfall': 210.0},
        {'name': 'maize', 'nitrogen': 60, 'phosphorus': 40, 'potassium': 60, 'temperature': 23.1, 'humidity': 68, 'ph_value': 6.6, 'rainfall': 90.3},
        {'name': 'wheat', 'nitrogen': 30, 'phosphorus': 20, 'potassium': 25, 'temperature': 19.4, 'humidity': 60, 'ph_value': 6.7, 'rainfall': 85.0},
        {'name': 'chickpea', 'nitrogen': 45, 'phosphorus': 30, 'potassium': 45, 'temperature': 22.5, 'humidity': 70, 'ph_value': 6.8, 'rainfall': 100.2},
        {'name': 'cotton', 'nitrogen': 70, 'phosphorus': 55, 'potassium': 60, 'temperature': 25.0, 'humidity': 75, 'ph_value': 6.4, 'rainfall': 130.0},
        {'name': 'lentil', 'nitrogen': 20, 'phosphorus': 30, 'potassium': 25, 'temperature': 17.5, 'humidity': 78, 'ph_value': 6.2, 'rainfall': 200.5},
        {'name': 'mango', 'nitrogen': 50, 'phosphorus': 45, 'potassium': 55, 'temperature': 24.2, 'humidity': 65, 'ph_value': 6.9, 'rainfall': 160.7},
        {'name': 'banana', 'nitrogen': 60, 'phosphorus': 50, 'potassium': 50, 'temperature': 26.3, 'humidity': 78, 'ph_value': 6.3, 'rainfall': 180.4},
        {'name': 'barley', 'nitrogen': 25, 'phosphorus': 35, 'potassium': 20, 'temperature': 18.5, 'humidity': 70, 'ph_value': 6.5, 'rainfall': 120.1},
        {'name': 'peas', 'nitrogen': 65, 'phosphorus': 35, 'potassium': 40, 'temperature': 22.0, 'humidity': 68, 'ph_value': 6.8, 'rainfall': 105.5},
        {'name': 'kidneybeans', 'nitrogen': 75, 'phosphorus': 40, 'potassium': 50, 'temperature': 21.0, 'humidity': 60, 'ph_value': 6.6, 'rainfall': 95.5},
        {'name': 'pigeonpeas', 'nitrogen': 55, 'phosphorus': 45, 'potassium': 50, 'temperature': 20.0, 'humidity': 70, 'ph_value': 6.5, 'rainfall': 150.0},
        {'name': 'blackgram', 'nitrogen': 40, 'phosphorus': 30, 'potassium': 40, 'temperature': 24.8, 'humidity': 85, 'ph_value': 6.3, 'rainfall': 200.2},
        {'name': 'mungbean', 'nitrogen': 50, 'phosphorus': 40, 'potassium': 45, 'temperature': 25.2, 'humidity': 82, 'ph_value': 6.4, 'rainfall': 195.8},
        {'name': 'coffee', 'nitrogen': 80, 'phosphorus': 40, 'potassium': 35, 'temperature': 20.5, 'humidity': 65, 'ph_value': 6.6, 'rainfall': 110.2},
        {'name': 'papaya', 'nitrogen': 60, 'phosphorus': 35, 'potassium': 40, 'temperature': 24.5, 'humidity': 70, 'ph_value': 6.7, 'rainfall': 175.0},
        {'name': 'apple', 'nitrogen': 30, 'phosphorus': 25, 'potassium': 30, 'temperature': 17.8, 'humidity': 68, 'ph_value': 6.4, 'rainfall': 85.5},
    ]

    # Crops NOT in dataset
    not_in_dataset = {'wheat', 'sugarcane', 'barley', 'peas'}

    print(f"\nModel has {predictor.num_crops} crops")
    print(f"\nNOTE: 4 crops are NOT in the trained model:")
    print(f"  {', '.join(not_in_dataset)}")
    print(f"\nRunning {len(test_cases)} test cases...\n")

    correct = 0
    top3_correct = 0
    not_in_model = 0

    for i, test in enumerate(test_cases, 1):
        expected = test.pop('name')
        result = predictor.predict(test)

        # Check if expected crop exists in model
        is_in_model = expected.lower() not in not_in_dataset

        predicted = result['predicted_crop'].lower()
        confidence = result['confidence_percent']

        # Check if correct
        is_correct = predicted == expected.lower()

        # Check if in top-3
        top3_names = [c['crop'].lower() for c in result['top_3_crops']]
        in_top3 = expected.lower() in top3_names

        # Status
        if is_correct:
            status = "CORRECT"
            correct += 1
            top3_correct += 1
        elif in_top3:
            status = "In Top-3"
            top3_correct += 1
        elif not is_in_model:
            status = "NOT IN MODEL"
            not_in_model += 1
        else:
            status = "WRONG"

        print(f"{i:2d}. Expected: {expected:12s} | Predicted: {predicted:12s} ({confidence:5.1f}%) | {status}")

        if not is_in_model:
            print(f"    Top-3: {', '.join(top3_names)}")

    print("\n" + "=" * 80)
    print(f"RESULTS:")
    print(f"  Exact matches:     {correct}/{len(test_cases) - not_in_model} ({correct/(len(test_cases)-not_in_model)*100:.1f}%)")
    print(f"  Top-3 matches:     {top3_correct}/{len(test_cases) - not_in_model} ({top3_correct/(len(test_cases)-not_in_model)*100:.1f}%)")
    print(f"  Not in model:      {not_in_model} (wheat, sugarcane, barley, peas)")
    print(f"  Total tested:      {len(test_cases)}")
    print("=" * 80)

if __name__ == '__main__':
    test_samples()
