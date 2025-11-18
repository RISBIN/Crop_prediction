# -*- coding: utf-8 -*-
"""Test Multiple Climate Scenarios"""
import joblib
import numpy as np

model = joblib.load('model.pkl')

crops = ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
         'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
         'banana', 'mango', 'grapes', 'watermelon', 'muskmelon',
         'apple', 'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee']

scenarios = [
    {
        'name': 'Scenario 1: High Rainfall & Humidity (Your Data)',
        'data': [90, 42, 43, 20.8, 82.0, 6.5, 202.9],
        'description': 'Current conditions - monsoon/wet season'
    },
    {
        'name': 'Scenario 2: Rice-Friendly Conditions',
        'data': [80, 40, 40, 25.0, 85.0, 6.5, 250.0],
        'description': 'High water, warm temp, high humidity'
    },
    {
        'name': 'Scenario 3: Wheat Conditions',
        'data': [50, 60, 40, 18.0, 60.0, 7.0, 80.0],
        'description': 'Cool, moderate rain, lower humidity'
    },
    {
        'name': 'Scenario 4: Cotton Conditions',
        'data': [75, 50, 120, 28.0, 70.0, 7.0, 100.0],
        'description': 'Warm, high potassium, moderate rain'
    },
    {
        'name': 'Scenario 5: Lentil/Chickpea Conditions',
        'data': [40, 60, 80, 22.0, 55.0, 7.0, 65.0],
        'description': 'Cool-warm, low rain, low humidity'
    },
    {
        'name': 'Scenario 6: Tropical Fruit (Banana)',
        'data': [100, 75, 50, 27.0, 85.0, 6.5, 180.0],
        'description': 'Tropical: high N, warm, humid'
    }
]

print("="*100)
print("TESTING MULTIPLE CLIMATE SCENARIOS")
print("="*100)

for scenario in scenarios:
    X = np.array([scenario['data']])
    pred = model.predict(X)[0]
    probs = model.predict_proba(X)[0]

    print(f"\n{scenario['name']}")
    print(f"Description: {scenario['description']}")
    print("-"*100)

    # Input summary
    labels = ['N', 'P', 'K', 'Temp', 'Humidity', 'pH', 'Rainfall']
    input_str = ", ".join([f"{label}={val}" for label, val in zip(labels, scenario['data'])])
    print(f"Input: {input_str}")

    # Top prediction
    print(f"\nPredicted Crop: {crops[pred].upper()} (Confidence: {probs[pred]*100:.2f}%)")

    # Top 3
    print("Top 3 Recommendations:")
    top3 = probs.argsort()[-3:][::-1]
    for i, idx in enumerate(top3, 1):
        print(f"  {i}. {crops[idx]:15s} - {probs[idx]*100:.2f}%")

    print()

print("="*100)
