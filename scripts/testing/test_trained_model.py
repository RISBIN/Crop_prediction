"""
Test Trained Crop Prediction Model
===================================
Quick script to test your trained model with sample predictions
"""

import numpy as np
from apps.predictions.ml_services.crop_predictor import get_crop_predictor

# Test cases for different crops
TEST_CASES = {
    'Sugarcane': {
        'nitrogen': 120, 'phosphorus': 60, 'potassium': 80,
        'temperature': 28, 'humidity': 75, 'ph_value': 6.8, 'rainfall': 2000
    },
    'Wheat': {
        'nitrogen': 80, 'phosphorus': 40, 'potassium': 40,
        'temperature': 18, 'humidity': 65, 'ph_value': 6.8, 'rainfall': 600
    },
    'Rice': {
        'nitrogen': 90, 'phosphorus': 42, 'potassium': 43,
        'temperature': 21, 'humidity': 82, 'ph_value': 6.5, 'rainfall': 203
    },
    'Maize': {
        'nitrogen': 90, 'phosphorus': 40, 'potassium': 40,
        'temperature': 21, 'humidity': 82, 'ph_value': 6.5, 'rainfall': 100
    },
    'Coffee': {
        'nitrogen': 100, 'phosphorus': 50, 'potassium': 35,
        'temperature': 25, 'humidity': 85, 'ph_value': 6.8, 'rainfall': 200
    },
    'Cotton': {
        'nitrogen': 120, 'phosphorus': 50, 'potassium': 50,
        'temperature': 25, 'humidity': 70, 'ph_value': 7.0, 'rainfall': 100
    },
    'Chickpea': {
        'nitrogen': 40, 'phosphorus': 60, 'potassium': 80,
        'temperature': 25, 'humidity': 60, 'ph_value': 7.0, 'rainfall': 60
    },
    'Banana': {
        'nitrogen': 100, 'phosphorus': 80, 'potassium': 50,
        'temperature': 28, 'humidity': 85, 'ph_value': 6.5, 'rainfall': 150
    }
}

def print_result(expected_crop, features, result):
    """Pretty print prediction results"""
    print(f"\n{'='*70}")
    print(f"🌾 Test Case: {expected_crop}")
    print(f"{'='*70}")

    print(f"\n📊 Input Parameters:")
    print(f"   N={features['nitrogen']}, P={features['phosphorus']}, K={features['potassium']}")
    print(f"   Temp={features['temperature']}°C, Humidity={features['humidity']}%")
    print(f"   pH={features['ph_value']}, Rainfall={features['rainfall']}mm")

    print(f"\n🎯 Prediction Results:")
    print(f"   Predicted Crop: {result['predicted_crop']}")
    print(f"   Confidence: {result['confidence_percent']:.1f}%")

    print(f"\n🏆 Top-3 Recommendations:")
    for i, crop in enumerate(result['top_3_crops'], 1):
        bar_length = int(crop['confidence_percent'] / 2)
        bar = '█' * bar_length + '░' * (50 - bar_length)
        print(f"   {i}. {crop['crop']:15s} {bar} {crop['confidence_percent']:5.1f}%")

    # Check if prediction matches expected
    if result['predicted_crop'].lower() == expected_crop.lower():
        print(f"\n✅ CORRECT! Predicted '{result['predicted_crop']}' (expected '{expected_crop}')")
    else:
        # Check if in top-3
        top3_names = [c['crop'].lower() for c in result['top_3_crops']]
        if expected_crop.lower() in top3_names:
            print(f"\n⚠️  Expected '{expected_crop}' is in Top-3 (ranked #{top3_names.index(expected_crop.lower())+1})")
        else:
            print(f"\n❌ MISS: Predicted '{result['predicted_crop']}' (expected '{expected_crop}')")

def main():
    print("\n" + "="*70)
    print("🧪 TESTING TRAINED CROP PREDICTION MODEL")
    print("="*70)

    # Load predictor
    print("\n📦 Loading model...")
    predictor = get_crop_predictor()

    if not predictor.is_trained:
        print("\n❌ Model not trained!")
        print("   Please run: python train_crop_model.py")
        return

    print(f"✅ Model loaded successfully")
    print(f"   Total crops: {predictor.num_crops}")
    print(f"   Available: {', '.join(predictor.crops_list[:10])}...")

    # Run tests
    print(f"\n🧪 Running {len(TEST_CASES)} test cases...\n")

    correct = 0
    top3_correct = 0

    for expected_crop, features in TEST_CASES.items():
        result = predictor.predict(features)
        print_result(expected_crop, features, result)

        # Count accuracy
        if result['predicted_crop'].lower() == expected_crop.lower():
            correct += 1
            top3_correct += 1
        else:
            top3_names = [c['crop'].lower() for c in result['top_3_crops']]
            if expected_crop.lower() in top3_names:
                top3_correct += 1

    # Summary
    print(f"\n{'='*70}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*70}")
    print(f"   Total tests: {len(TEST_CASES)}")
    print(f"   Exact matches: {correct}/{len(TEST_CASES)} ({correct/len(TEST_CASES)*100:.1f}%)")
    print(f"   Top-3 matches: {top3_correct}/{len(TEST_CASES)} ({top3_correct/len(TEST_CASES)*100:.1f}%)")

    if correct == len(TEST_CASES):
        print(f"\n🎉 Perfect! All predictions correct!")
    elif top3_correct == len(TEST_CASES):
        print(f"\n✅ Good! All expected crops in Top-3")
    else:
        print(f"\n⚠️  Some predictions missed - model may need more training data")

    print(f"\n✅ Testing completed!")
    print()

if __name__ == '__main__':
    main()
