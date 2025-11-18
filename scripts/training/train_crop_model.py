"""
Crop Prediction Model Training Script
======================================
Trains a Deep Learning model for crop recommendation
Input: 7 features (N, P, K, temperature, humidity, ph, rainfall)
Output: Crop recommendation with confidence scores
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from pathlib import Path

# ML Libraries
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

# Deep Learning
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.utils import to_categorical

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

class CropModelTrainer:
    """Train crop prediction model from scratch"""

    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.history = None
        self.X_train = None
        self.X_val = None
        self.X_test = None
        self.y_train = None
        self.y_val = None
        self.y_test = None

    def load_data(self):
        """Load dataset from CSV"""
        print("\n📂 Loading dataset...")
        print(f"   Path: {self.dataset_path}")

        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(
                f"Dataset not found at {self.dataset_path}\n"
                "Please download dataset or run: python generate_sample_dataset.py"
            )

        # Load CSV
        df = pd.read_csv(self.dataset_path)
        print(f"✅ Loaded {len(df)} samples")
        print(f"   Columns: {list(df.columns)}")

        # Check required columns
        required_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Extract features and labels
        X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']].values
        y = df['label'].values

        print(f"   Crops: {len(np.unique(y))}")
        print(f"   Features shape: {X.shape}")

        return X, y, df

    def engineer_features(self, X):
        """
        Transform 7 input features into 15 engineered features
        This matches the production model architecture
        """
        print("\n🔧 Engineering features (7 → 15)...")

        N = X[:, 0]
        P = X[:, 1]
        K = X[:, 2]
        temp = X[:, 3]
        humidity = X[:, 4]
        ph = X[:, 5]
        rainfall = X[:, 6]

        # Engineered features
        NPK_sum = N + P + K
        N_P_ratio = N / (P + 0.01)
        N_K_ratio = N / (K + 0.01)
        P_K_ratio = P / (K + 0.01)
        temp_humidity = temp * humidity / 100
        rainfall_humidity = rainfall * humidity / 100

        # Categorical encoding
        temp_cat = np.digitize(temp, bins=[15, 25, 35])  # 0=cold, 1=cool, 2=warm, 3=hot
        rain_cat = np.digitize(rainfall, bins=[100, 200, 300])  # 0=low, 1=med, 2=high, 3=very_high

        # Combine all features
        X_engineered = np.column_stack([
            N, P, K, temp, humidity, ph, rainfall,  # Original 7
            NPK_sum, N_P_ratio, N_K_ratio, P_K_ratio,  # Ratios
            temp_humidity, rainfall_humidity,  # Interactions
            temp_cat, rain_cat  # Categories
        ])

        print(f"✅ Engineered features shape: {X_engineered.shape}")
        return X_engineered

    def preprocess_data(self, X, y):
        """Split and preprocess data"""
        print("\n📊 Preprocessing data...")

        # Engineer features
        X_engineered = self.engineer_features(X)

        # Encode labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        num_classes = len(self.label_encoder.classes_)

        print(f"   Classes: {num_classes}")
        print(f"   Crop names: {list(self.label_encoder.classes_[:5])}...")

        # Split: 80% train, 10% val, 10% test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X_engineered, y_encoded, test_size=0.1, random_state=42, stratify=y_encoded
        )

        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=0.111, random_state=42, stratify=y_temp  # 0.111 of 90% = 10% of total
        )

        print(f"   Train samples: {len(X_train)} ({len(X_train)/len(X)*100:.1f}%)")
        print(f"   Val samples: {len(X_val)} ({len(X_val)/len(X)*100:.1f}%)")
        print(f"   Test samples: {len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")

        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)

        # One-hot encode labels
        y_train_cat = to_categorical(y_train, num_classes)
        y_val_cat = to_categorical(y_val, num_classes)
        y_test_cat = to_categorical(y_test, num_classes)

        # Store for later use
        self.X_train, self.X_val, self.X_test = X_train_scaled, X_val_scaled, X_test_scaled
        self.y_train, self.y_val, self.y_test = y_train, y_val, y_test

        return X_train_scaled, X_val_scaled, X_test_scaled, y_train_cat, y_val_cat, y_test_cat, num_classes

    def build_model(self, num_classes):
        """Build Deep Learning model"""
        print("\n🏗️  Building model architecture...")

        model = Sequential([
            # Input layer (15 features)
            Dense(256, activation='relu', input_shape=(15,)),
            Dropout(0.3),

            # Hidden layer 1
            Dense(128, activation='relu'),
            Dropout(0.3),

            # Hidden layer 2
            Dense(64, activation='relu'),
            Dropout(0.2),

            # Output layer
            Dense(num_classes, activation='softmax')
        ])

        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
        )

        print("✅ Model architecture:")
        model.summary()

        self.model = model
        return model

    def train_model(self, X_train, y_train, X_val, y_val):
        """Train the model"""
        print("\n🎯 Training model...")

        # Create output directory
        os.makedirs('ml_models', exist_ok=True)
        os.makedirs('trained-outputs', exist_ok=True)

        # Callbacks
        callbacks = [
            # Early stopping
            EarlyStopping(
                monitor='val_accuracy',
                patience=15,
                restore_best_weights=True,
                verbose=1
            ),

            # Save best model
            ModelCheckpoint(
                'trained-outputs/best_crop_model.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),

            # Reduce learning rate on plateau
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=0.00001,
                verbose=1
            )
        ]

        # Train
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=100,
            batch_size=32,
            callbacks=callbacks,
            verbose=1
        )

        self.history = history
        print("✅ Training completed!")

        return history

    def evaluate_model(self, X_test, y_test):
        """Evaluate model on test set"""
        print("\n📈 Evaluating model on test set...")

        # Predictions
        y_pred_proba = self.model.predict(X_test, verbose=0)
        y_pred = np.argmax(y_pred_proba, axis=1)

        # Accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"   Test Accuracy: {accuracy*100:.2f}%")

        # Top-3 accuracy
        top3_idx = np.argsort(y_pred_proba, axis=1)[:, -3:]
        top3_accuracy = np.mean([y_test[i] in top3_idx[i] for i in range(len(y_test))])
        print(f"   Top-3 Accuracy: {top3_accuracy*100:.2f}%")

        # Classification report
        print("\n📊 Classification Report:")
        crop_names = self.label_encoder.classes_
        print(classification_report(y_test, y_pred, target_names=crop_names, zero_division=0))

        return accuracy, top3_accuracy

    def save_artifacts(self, accuracy, top3_accuracy):
        """Save model and preprocessing artifacts"""
        print("\n💾 Saving model artifacts...")

        # Save model
        self.model.save('ml_models/best_crop_model.h5')
        print("   ✅ Saved: ml_models/best_crop_model.h5")

        # Save scaler
        joblib.dump(self.scaler, 'ml_models/scaler.pkl')
        print("   ✅ Saved: ml_models/scaler.pkl")

        # Save label encoder
        joblib.dump(self.label_encoder, 'ml_models/label_encoder.pkl')
        print("   ✅ Saved: ml_models/label_encoder.pkl")

        # Save metadata
        metadata = {
            'model_type': 'MLP',
            'model_version': '1.0',
            'training_date': datetime.now().isoformat(),
            'num_features': 15,
            'num_classes': len(self.label_encoder.classes_),
            'feature_names': [
                'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall',
                'NPK_sum', 'N_P_ratio', 'N_K_ratio', 'P_K_ratio',
                'temp_humidity', 'rainfall_humidity',
                'temp_cat_encoded', 'rain_cat_encoded'
            ],
            'class_names': self.label_encoder.classes_.tolist(),
            'test_accuracy': float(accuracy),
            'test_top3_accuracy': float(top3_accuracy),
            'architecture': {
                'input': 15,
                'dense_1': 256,
                'dense_2': 128,
                'dense_3': 64,
                'output': len(self.label_encoder.classes_)
            }
        }

        with open('ml_models/metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        print("   ✅ Saved: ml_models/metadata.json")

        print("\n🎉 All artifacts saved successfully!")

    def run_full_pipeline(self):
        """Run complete training pipeline"""
        print("\n" + "="*60)
        print("🌾 CROP PREDICTION MODEL TRAINING")
        print("="*60)

        # Load data
        X, y, df = self.load_data()

        # Preprocess
        X_train, X_val, X_test, y_train_cat, y_val_cat, y_test_cat, num_classes = self.preprocess_data(X, y)

        # Build model
        self.build_model(num_classes)

        # Train
        self.train_model(X_train, y_train_cat, X_val, y_val_cat)

        # Evaluate
        accuracy, top3_accuracy = self.evaluate_model(X_test, y_test_cat)

        # Save
        self.save_artifacts(accuracy, top3_accuracy)

        print("\n" + "="*60)
        print("✅ TRAINING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📊 Final Results:")
        print(f"   Test Accuracy: {accuracy*100:.2f}%")
        print(f"   Top-3 Accuracy: {top3_accuracy*100:.2f}%")
        print(f"   Crops: {num_classes}")
        print(f"\n🎯 Next Steps:")
        print(f"   1. Test model: python test_deeplearning_model.py")
        print(f"   2. Run Django: python manage.py runserver")
        print(f"   3. Go to: http://127.0.0.1:8000/predictions/crop/")
        print()


def main():
    """Main training function"""

    # Dataset path options (in order of priority)
    dataset_paths = [
        'datasets/crop_data/Crop_recommendation.csv',  # Kaggle dataset
        'datasets/crop_data/crop_sample.csv',  # Generated sample
        'datasets/crop_data/crop_data.csv',  # Alternative name
    ]

    # Find existing dataset
    dataset_path = None
    for path in dataset_paths:
        if os.path.exists(path):
            dataset_path = path
            break

    if dataset_path is None:
        print("\n❌ No dataset found!")
        print("\n📥 Please either:")
        print("   1. Download from Kaggle: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset")
        print("      Place in: datasets/crop_data/Crop_recommendation.csv")
        print("\n   OR")
        print("\n   2. Generate sample dataset:")
        print("      python generate_sample_dataset.py")
        print()
        return

    # Run training
    trainer = CropModelTrainer(dataset_path)
    trainer.run_full_pipeline()


if __name__ == '__main__':
    main()
