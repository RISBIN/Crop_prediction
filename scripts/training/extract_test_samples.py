"""
Extract real test samples from the Crop_recommendation.csv dataset
"""
import pandas as pd
import json

# Load dataset
df = pd.read_csv('Crop_recommendation.csv')

# Get 3 samples per crop
samples = []
for crop in sorted(df['label'].unique()):
    crop_samples = df[df['label'] == crop].head(3)
    for _, row in crop_samples.iterrows():
        samples.append({
            'crop': crop,
            'nitrogen': int(row['N']),
            'phosphorus': int(row['P']),
            'potassium': int(row['K']),
            'temperature': round(float(row['temperature']), 1),
            'humidity': round(float(row['humidity']), 1),
            'ph_value': round(float(row['ph']), 1),
            'rainfall': round(float(row['rainfall']), 1)
        })

# Save as JSON
with open('test_samples_real.json', 'w') as f:
    json.dump(samples, f, indent=2)

# Save as CSV
samples_df = pd.DataFrame(samples)
samples_df.to_csv('test_samples_real.csv', index=False)

# Print summary
print(f"Extracted {len(samples)} real samples from dataset")
print(f"Saved to: test_samples_real.json and test_samples_real.csv")
print(f"\nCrops included: {len(df['label'].unique())}")
print(f"Sample crops: {', '.join(sorted(df['label'].unique())[:10])}")
