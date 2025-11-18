"""
Generate Sample Crop Recommendation Dataset
Creates synthetic data for testing the model training pipeline
"""
import pandas as pd
import numpy as np
import os

# Set random seed for reproducibility
np.random.seed(42)

# Define crop parameters (based on real agricultural data)
CROP_PROFILES = {
    'rice': {
        'N': (80, 100), 'P': (35, 50), 'K': (35, 50),
        'temp': (20, 27), 'humidity': (75, 90), 'ph': (6.0, 7.5), 'rain': (150, 300)
    },
    'wheat': {
        'N': (70, 90), 'P': (35, 50), 'K': (35, 50),
        'temp': (15, 25), 'humidity': (60, 75), 'ph': (6.5, 7.5), 'rain': (50, 100)
    },
    'maize': {
        'N': (75, 100), 'P': (35, 55), 'K': (25, 45),
        'temp': (18, 27), 'humidity': (65, 85), 'ph': (6.0, 7.5), 'rain': (60, 120)
    },
    'chickpea': {
        'N': (35, 50), 'P': (55, 75), 'K': (70, 90),
        'temp': (20, 30), 'humidity': (50, 70), 'ph': (6.0, 7.5), 'rain': (40, 80)
    },
    'kidneybeans': {
        'N': (15, 25), 'P': (55, 75), 'K': (15, 25),
        'temp': (15, 25), 'humidity': (55, 75), 'ph': (5.5, 6.5), 'rain': (50, 100)
    },
    'pigeonpeas': {
        'N': (15, 25), 'P': (55, 75), 'K': (15, 25),
        'temp': (20, 30), 'humidity': (60, 80), 'ph': (6.0, 7.0), 'rain': (50, 120)
    },
    'mothbeans': {
        'N': (15, 30), 'P': (45, 65), 'K': (15, 30),
        'temp': (25, 35), 'humidity': (50, 70), 'ph': (6.5, 8.0), 'rain': (20, 50)
    },
    'mungbean': {
        'N': (15, 25), 'P': (35, 55), 'K': (30, 50),
        'temp': (25, 35), 'humidity': (70, 90), 'ph': (6.0, 7.5), 'rain': (40, 80)
    },
    'blackgram': {
        'N': (35, 50), 'P': (55, 75), 'K': (15, 30),
        'temp': (25, 35), 'humidity': (65, 85), 'ph': (6.0, 7.0), 'rain': (40, 80)
    },
    'lentil': {
        'N': (15, 30), 'P': (55, 75), 'K': (15, 30),
        'temp': (15, 27), 'humidity': (60, 80), 'ph': (6.0, 7.5), 'rain': (25, 60)
    },
    'pomegranate': {
        'N': (15, 25), 'P': (10, 25), 'K': (35, 50),
        'temp': (18, 30), 'humidity': (35, 55), 'ph': (6.5, 7.5), 'rain': (40, 80)
    },
    'banana': {
        'N': (90, 120), 'P': (70, 95), 'K': (40, 60),
        'temp': (25, 32), 'humidity': (75, 95), 'ph': (6.0, 7.5), 'rain': (100, 200)
    },
    'mango': {
        'N': (15, 30), 'P': (20, 40), 'K': (20, 40),
        'temp': (24, 35), 'humidity': (50, 70), 'ph': (5.5, 7.0), 'rain': (50, 120)
    },
    'grapes': {
        'N': (15, 30), 'P': (120, 150), 'K': (180, 220),
        'temp': (15, 28), 'humidity': (60, 80), 'ph': (6.0, 7.5), 'rain': (40, 100)
    },
    'watermelon': {
        'N': (90, 120), 'P': (8, 18), 'K': (30, 50),
        'temp': (24, 32), 'humidity': (65, 85), 'ph': (6.0, 7.0), 'rain': (40, 80)
    },
    'muskmelon': {
        'N': (90, 120), 'P': (15, 30), 'K': (10, 25),
        'temp': (24, 32), 'humidity': (65, 85), 'ph': (6.0, 7.0), 'rain': (20, 50)
    },
    'apple': {
        'N': (15, 30), 'P': (120, 150), 'K': (180, 220),
        'temp': (10, 24), 'humidity': (70, 90), 'ph': (6.0, 7.0), 'rain': (100, 150)
    },
    'orange': {
        'N': (15, 30), 'P': (8, 18), 'K': (8, 18),
        'temp': (20, 32), 'humidity': (70, 90), 'ph': (6.0, 7.5), 'rain': (100, 180)
    },
    'papaya': {
        'N': (45, 65), 'P': (80, 110), 'K': (45, 65),
        'temp': (25, 35), 'humidity': (70, 90), 'ph': (6.0, 7.0), 'rain': (100, 200)
    },
    'coconut': {
        'N': (15, 30), 'P': (120, 150), 'K': (120, 150),
        'temp': (25, 32), 'humidity': (70, 90), 'ph': (5.5, 7.0), 'rain': (100, 250)
    },
    'cotton': {
        'N': (110, 140), 'P': (40, 60), 'K': (40, 60),
        'temp': (21, 30), 'humidity': (60, 80), 'ph': (6.5, 7.5), 'rain': (50, 120)
    },
    'coffee': {
        'N': (90, 120), 'P': (40, 60), 'K': (25, 45),
        'temp': (20, 28), 'humidity': (70, 90), 'ph': (6.0, 7.0), 'rain': (150, 250)
    }
}

def generate_sample(crop, profile):
    """Generate one sample for a crop with some random variation"""
    return {
        'N': np.random.uniform(*profile['N']),
        'P': np.random.uniform(*profile['P']),
        'K': np.random.uniform(*profile['K']),
        'temperature': np.random.uniform(*profile['temp']),
        'humidity': np.random.uniform(*profile['humidity']),
        'ph': np.random.uniform(*profile['ph']),
        'rainfall': np.random.uniform(*profile['rain']),
        'label': crop
    }

def main():
    print("🌾 Generating Sample Crop Recommendation Dataset...")
    print(f"Crops: {len(CROP_PROFILES)}")

    # Generate samples (100 per crop = 2,200 total)
    samples_per_crop = 100
    all_samples = []

    for crop, profile in CROP_PROFILES.items():
        print(f"  Generating {samples_per_crop} samples for {crop}...")
        for _ in range(samples_per_crop):
            sample = generate_sample(crop, profile)
            all_samples.append(sample)

    # Create DataFrame
    df = pd.DataFrame(all_samples)

    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Create output directory
    output_dir = 'datasets/crop_data'
    os.makedirs(output_dir, exist_ok=True)

    # Save
    output_file = f'{output_dir}/crop_sample.csv'
    df.to_csv(output_file, index=False)

    print(f"\n✅ Dataset generated successfully!")
    print(f"📁 Location: {output_file}")
    print(f"📊 Total samples: {len(df)}")
    print(f"🌱 Crops: {df['label'].nunique()}")
    print(f"\n📈 Samples per crop:")
    print(df['label'].value_counts().sort_index())

    print(f"\n📋 First 5 rows:")
    print(df.head())

    print(f"\n🎯 Dataset Statistics:")
    print(df.describe())

    print(f"\n✅ Ready to train! Run: python train_crop_model.py")

if __name__ == '__main__':
    main()
