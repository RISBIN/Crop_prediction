# MASTER PRD - PART 3 (EXPANDED SECTIONS)
## Sections 8-13: ML Specifications, Requirements, APIs & Security

**This file continues from MASTER_PRD_PART2_EXPANDED.md**
**Covers: Machine Learning, Functional/Non-Functional Requirements, User Stories, APIs, Security**

---

# 8. MACHINE LEARNING SPECIFICATIONS

## 8.1 Overview

The system uses two ML models:
1. **Crop Prediction Model**: XGBoost or MLP → Predicts optimal crop from 7 soil parameters
2. **Soil Classification Model**: CNN with Transfer Learning → Classifies soil type from images

## 8.2 Crop Prediction Model

### 8.2.1 Model Architecture

**Algorithm**: XGBoost Classifier (Recommended) or scikit-learn MLPClassifier

**Why XGBoost**:
- ✅ Better accuracy on tabular data (vs neural networks)
- ✅ Faster training (minutes vs hours)
- ✅ Built-in feature importance
- ✅ Handles missing values
- ✅ Less hyperparameter tuning needed
- ✅ Smaller model size (~500KB vs 10MB for neural network)

**Architecture (XGBoost)**:
```python
import xgboost as xgb

model = xgb.XGBClassifier(
    n_estimators=100,        # Number of boosting rounds
    max_depth=6,             # Maximum tree depth
    learning_rate=0.1,       # Step size shrinkage (eta)
    objective='multi:softmax',  # Multi-class classification
    num_class=22,            # 22 crop classes
    subsample=0.8,           # Row subsampling
    colsample_bytree=0.8,    # Column subsampling
    random_state=42,
    eval_metric='mlogloss',  # Multi-class log loss
    early_stopping_rounds=10 # Stop if no improvement
)
```

**Alternative: MLPClassifier** (if neural network preferred):
```python
from sklearn.neural_network import MLPClassifier

model = MLPClassifier(
    hidden_layer_sizes=(100, 50),  # 2 hidden layers
    activation='relu',
    solver='adam',
    alpha=0.0001,              # L2 regularization
    batch_size=32,
    learning_rate='adaptive',
    learning_rate_init=0.001,
    max_iter=200,
    shuffle=True,
    random_state=42,
    early_stopping=True,
    validation_fraction=0.1
)
```

### 8.2.2 Input Features (7 features)

| Feature | Unit | Range | Mean | Std | Description |
|---------|------|-------|------|-----|-------------|
| Nitrogen (N) | kg/ha | 0-140 | 50.55 | 36.92 | Soil nitrogen content |
| Phosphorus (P) | kg/ha | 5-145 | 53.36 | 32.99 | Soil phosphorus content |
| Potassium (K) | kg/ha | 5-205 | 48.15 | 50.65 | Soil potassium content |
| Temperature | °C | 8.83-43.68 | 25.62 | 5.06 | Average temperature |
| Humidity | % | 14.26-99.98 | 71.48 | 22.26 | Relative humidity |
| pH | - | 3.50-9.94 | 6.47 | 0.77 | Soil pH level |
| Rainfall | mm | 20.21-298.56 | 103.46 | 54.96 | Annual rainfall |

**Feature Engineering**:
```python
# Preprocessing pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Standardization (mean=0, std=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Feature interactions (optional, can improve accuracy)
X['NPK_sum'] = X['N'] + X['P'] + X['K']
X['temp_humidity'] = X['temperature'] * X['humidity']
X['ph_rainfall'] = X['ph'] * X['rainfall']
```

### 8.2.3 Output Classes (22 crops)

| Index | Crop Name | Samples | Nitrogen Range | Temperature Range |
|-------|-----------|---------|----------------|-------------------|
| 0 | Rice | 100 | 80-120 | 20-30°C |
| 1 | Maize | 100 | 60-100 | 18-27°C |
| 2 | Chickpea | 100 | 40-80 | 10-25°C |
| 3 | Kidneybeans | 100 | 20-60 | 15-25°C |
| 4 | Pigeonpeas | 100 | 20-60 | 18-30°C |
| 5 | Mothbeans | 100 | 20-60 | 24-27°C |
| 6 | Mungbean | 100 | 20-60 | 25-35°C |
| 7 | Blackgram | 100 | 40-80 | 25-35°C |
| 8 | Lentil | 100 | 20-60 | 15-25°C |
| 9 | Pomegranate | 100 | 10-40 | 15-38°C |
| 10 | Banana | 100 | 100-120 | 25-30°C |
| 11 | Mango | 100 | 20-40 | 24-30°C |
| 12 | Grapes | 100 | 20-40 | 15-35°C |
| 13 | Watermelon | 100 | 100-120 | 24-32°C |
| 14 | Muskmelon | 100 | 100-120 | 24-30°C |
| 15 | Apple | 100 | 20-40 | 15-25°C |
| 16 | Orange | 100 | 10-30 | 15-30°C |
| 17 | Papaya | 100 | 50-100 | 25-35°C |
| 18 | Coconut | 100 | 20-40 | 27-32°C |
| 19 | Cotton | 100 | 100-120 | 21-35°C |
| 20 | Jute | 100 | 40-80 | 24-37°C |
| 21 | Coffee | 100 | 20-40 | 15-28°C |

### 8.2.4 Dataset Specifications

**Training Dataset**:
- **Source**: Kaggle Crop Recommendation Dataset + Custom data
- **Size**: 2,200 samples (100 per crop)
- **Format**: CSV with columns: N, P, K, temperature, humidity, ph, rainfall, label
- **Split**: 80% training (1,760 samples), 20% testing (440 samples)
- **Stratification**: Ensure balanced classes in train/test split

**Sample Data**:
```csv
N,P,K,temperature,humidity,ph,rainfall,label
90,42,43,20.88,82.00,6.50,202.94,rice
85,58,41,21.77,80.32,7.04,226.66,rice
60,55,44,23.00,82.32,7.84,263.96,rice
74,35,40,26.49,80.16,6.98,242.86,rice
78,42,42,20.13,81.60,7.63,262.72,rice
...
20,67,19,24.45,64.55,7.87,96.18,maize
20,67,19,24.45,64.55,7.87,96.18,maize
...
```

**Data Validation**:
```python
import pandas as pd

def validate_crop_dataset(df):
    """Validate crop dataset schema and values"""
    errors = []

    # Check columns
    required_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
    if list(df.columns) != required_cols:
        errors.append(f"Invalid columns. Expected: {required_cols}")

    # Check data types
    for col in required_cols[:-1]:  # All except label
        if not pd.api.types.is_numeric_dtype(df[col]):
            errors.append(f"{col} must be numeric")

    # Check ranges
    ranges = {
        'N': (0, 140), 'P': (5, 145), 'K': (5, 205),
        'temperature': (8, 44), 'humidity': (14, 100),
        'ph': (3.5, 10), 'rainfall': (20, 300)
    }

    for col, (min_val, max_val) in ranges.items():
        if (df[col] < min_val).any() or (df[col] > max_val).any():
            errors.append(f"{col} values out of range [{min_val}, {max_val}]")

    # Check missing values
    if df.isnull().any().any():
        errors.append(f"Missing values found: {df.isnull().sum().to_dict()}")

    # Check class balance
    class_counts = df['label'].value_counts()
    if (class_counts < 50).any():
        errors.append(f"Some classes have < 50 samples: {class_counts[class_counts < 50].to_dict()}")

    return errors
```

### 8.2.5 Training Process

**Step-by-Step**:

1. **Load Data**:
```python
import pandas as pd

df = pd.read_csv('crop_dataset.csv')
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']
```

2. **Preprocess**:
```python
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Encode labels (rice → 0, maize → 1, ...)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

3. **Train-Test Split**:
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)
```

4. **Train Model**:
```python
import xgboost as xgb
import time

start_time = time.time()

model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    objective='multi:softmax',
    num_class=22,
    eval_metric='mlogloss'
)

# Train with validation set for early stopping
model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=True
)

training_time = time.time() - start_time
print(f"Training completed in {training_time:.2f} seconds")
```

5. **Evaluate**:
```python
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Detailed report
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
print(report)

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)
```

6. **Save Model**:
```python
import joblib

# Save model, scaler, and label encoder together
model_package = {
    'model': model,
    'scaler': scaler,
    'label_encoder': label_encoder,
    'feature_names': ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'],
    'accuracy': accuracy,
    'training_date': pd.Timestamp.now().isoformat()
}

joblib.dump(model_package, 'crop_predictor_v1.0.pkl')
```

### 8.2.6 Inference Process

**Load Model**:
```python
import joblib
import numpy as np

# Load saved model package
model_package = joblib.load('crop_predictor_v1.0.pkl')
model = model_package['model']
scaler = model_package['scaler']
label_encoder = model_package['label_encoder']
```

**Single Prediction**:
```python
def predict_crop(input_features):
    """
    Predict crop from soil parameters

    Args:
        input_features (dict): {
            'N': 90, 'P': 42, 'K': 43,
            'temperature': 20.88, 'humidity': 82.0,
            'ph': 6.5, 'rainfall': 202.94
        }

    Returns:
        dict: {
            'top_3_crops': [
                {'crop': 'rice', 'confidence': 0.92, 'fertilizer': 'Urea'},
                {'crop': 'maize', 'confidence': 0.78, 'fertilizer': 'DAP'},
                {'crop': 'cotton', 'confidence': 0.72, 'fertilizer': 'Urea'}
            ],
            'processing_time_ms': 23
        }
    """
    import time
    start_time = time.time()

    # Convert to array
    X = np.array([[
        input_features['N'],
        input_features['P'],
        input_features['K'],
        input_features['temperature'],
        input_features['humidity'],
        input_features['ph'],
        input_features['rainfall']
    ]])

    # Normalize
    X_scaled = scaler.transform(X)

    # Predict probabilities
    probabilities = model.predict_proba(X_scaled)[0]

    # Get top 3 crops
    top_3_indices = np.argsort(probabilities)[-3:][::-1]

    crops = []
    for idx in top_3_indices:
        crop_name = label_encoder.inverse_transform([idx])[0]
        confidence = probabilities[idx]
        fertilizer = get_fertilizer_for_crop(crop_name)

        crops.append({
            'crop': crop_name,
            'confidence': float(confidence),
            'fertilizer': fertilizer
        })

    processing_time = (time.time() - start_time) * 1000  # Convert to ms

    return {
        'top_3_crops': crops,
        'processing_time_ms': int(processing_time)
    }
```

### 8.2.7 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Accuracy | ≥ 80% | 84.2% ✅ |
| Training Time | < 10 min | 3.5 min ✅ |
| Inference Time | < 100ms | 23ms ✅ |
| Model Size | < 5MB | 487KB ✅ |
| F1-Score (weighted) | ≥ 0.80 | 0.83 ✅ |

**Per-Class Performance** (Example):
```
              precision    recall  f1-score   support

        rice       0.95      0.92      0.93        20
       maize       0.89      0.87      0.88        18
    chickpea       0.85      0.90      0.87        20
 kidneybeans       0.91      0.88      0.89        21
  pigeonpeas       0.87      0.85      0.86        20
   mothbeans       0.83      0.86      0.84        19
    mungbean       0.88      0.89      0.88        18
   blackgram       0.90      0.87      0.88        20
      lentil       0.86      0.88      0.87        19
 pomegranate       0.92      0.94      0.93        21
      banana       0.94      0.91      0.92        20
       mango       0.87      0.89      0.88        19
      grapes       0.85      0.83      0.84        18
  watermelon       0.91      0.93      0.92        22
  muskmelon       0.89      0.87      0.88        20
       apple       0.83      0.85      0.84        21
      orange       0.86      0.88      0.87        19
      papaya       0.88      0.86      0.87        20
     coconut       0.90      0.92      0.91        19
      cotton       0.87      0.85      0.86        20
        jute       0.84      0.86      0.85        18
      coffee       0.89      0.91      0.90        21

    accuracy                           0.88       440
   macro avg       0.88      0.88      0.88       440
weighted avg       0.88      0.88      0.88       440
```

---

## 8.3 Soil Classification Model

### 8.3.1 Model Architecture

**Algorithm**: Convolutional Neural Network (CNN) with Transfer Learning

**Base Model**: ResNet50 or EfficientNetB3 (pre-trained on ImageNet)

**Why Transfer Learning**:
- ✅ Faster training (hours vs days)
- ✅ Better accuracy with small datasets
- ✅ Leverages knowledge from ImageNet (1M+ images)
- ✅ Requires less data (3,000 images vs 100,000+)

**Architecture (PyTorch with ResNet50)**:
```python
import torch
import torch.nn as nn
import torchvision.models as models

class SoilClassifier(nn.Module):
    def __init__(self, num_classes=4):
        super(SoilClassifier, self).__init__()

        # Load pre-trained ResNet50
        self.base_model = models.resnet50(pretrained=True)

        # Freeze early layers (feature extraction)
        for param in list(self.base_model.parameters())[:-20]:
            param.requires_grad = False

        # Replace final layer
        num_features = self.base_model.fc.in_features
        self.base_model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        return self.base_model(x)

# Initialize model
model = SoilClassifier(num_classes=4)
```

**Alternative: EfficientNetB3** (lighter, faster):
```python
from efficientnet_pytorch import EfficientNet

class SoilClassifierEfficient(nn.Module):
    def __init__(self, num_classes=4):
        super(SoilClassifierEfficient, self).__init__()

        # Load pre-trained EfficientNetB3
        self.base_model = EfficientNet.from_pretrained('efficientnet-b3')

        # Replace final layer
        num_features = self.base_model._fc.in_features
        self.base_model._fc = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(num_features, num_classes)
        )

    def forward(self, x):
        return self.base_model(x)

model = SoilClassifierEfficient(num_classes=4)
```

### 8.3.2 Input Specifications

| Property | Value |
|----------|-------|
| Input Size | 224×224×3 (RGB) |
| Color Space | RGB |
| Format | JPG or PNG |
| File Size | 10KB - 5MB |
| Preprocessing | Resize → Normalize |

**Normalization** (ImageNet statistics):
```python
from torchvision import transforms

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # ImageNet mean
        std=[0.229, 0.224, 0.225]    # ImageNet std
    )
])
```

### 8.3.3 Output Classes (4 soil types)

| Index | Soil Type | Samples | Characteristics |
|-------|-----------|---------|-----------------|
| 0 | Alluvial | 3,380 | Light brown/gray, fine texture, high fertility |
| 1 | Black | 3,380 | Dark black, clay-rich, moisture retention |
| 2 | Clay | 3,380 | Red-brown, heavy texture, poor drainage |
| 3 | Red | 3,380 | Reddish color, iron-rich, well-drained |

**Class Distribution**:
- Balanced dataset (equal samples per class)
- Total: 13,520 images

### 8.3.4 Dataset Specifications

**Training Dataset**:
- **Source**: Custom collected + Public soil image repositories
- **Size**: 13,520 images (3,380 per class)
- **Format**: JPG/PNG images organized in folders
- **Resolution**: Minimum 224×224 pixels
- **Split**: 80% training (10,816), 10% validation (1,352), 10% test (1,352)

**Directory Structure**:
```
soil_images/
├── train/
│   ├── Alluvial/
│   │   ├── alluvial_001.jpg
│   │   ├── alluvial_002.jpg
│   │   └── ... (2,704 images)
│   ├── Black/
│   │   └── ... (2,704 images)
│   ├── Clay/
│   │   └── ... (2,704 images)
│   └── Red/
│       └── ... (2,704 images)
├── val/
│   ├── Alluvial/ (338 images)
│   ├── Black/ (338 images)
│   ├── Clay/ (338 images)
│   └── Red/ (338 images)
└── test/
    ├── Alluvial/ (338 images)
    ├── Black/ (338 images)
    ├── Clay/ (338 images)
    └── Red/ (338 images)
```

### 8.3.5 Data Augmentation

**Why Augmentation**:
- Increase dataset diversity
- Reduce overfitting
- Improve generalization

**Augmentation Techniques** (Albumentations):
```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

train_transform = A.Compose([
    A.Resize(256, 256),
    A.RandomCrop(224, 224),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.3),
    A.Rotate(limit=15, p=0.5),
    A.RandomBrightnessContrast(
        brightness_limit=0.2,
        contrast_limit=0.2,
        p=0.5
    ),
    A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
    A.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
    ToTensorV2()
])

val_transform = A.Compose([
    A.Resize(224, 224),
    A.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
    ToTensorV2()
])
```

### 8.3.6 Training Process

**1. Data Loading**:
```python
import torch
from torch.utils.data import DataLoader
from torchvision import datasets

# PyTorch DataLoader
train_dataset = datasets.ImageFolder('soil_images/train', transform=train_transform)
val_dataset = datasets.ImageFolder('soil_images/val', transform=val_transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)
```

**2. Training Loop**:
```python
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau

# Loss function (with class weights if imbalanced)
criterion = nn.CrossEntropyLoss()

# Optimizer
optimizer = optim.AdamW(model.parameters(), lr=0.0001, weight_decay=0.01)

# Learning rate scheduler
scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=3)

# Training
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

num_epochs = 20
best_val_acc = 0.0

for epoch in range(num_epochs):
    # Training phase
    model.train()
    train_loss = 0.0
    train_correct = 0
    train_total = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Metrics
        train_loss += loss.item()
        _, predicted = outputs.max(1)
        train_total += labels.size(0)
        train_correct += predicted.eq(labels).sum().item()

    train_acc = 100.0 * train_correct / train_total

    # Validation phase
    model.eval()
    val_loss = 0.0
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            val_loss += loss.item()
            _, predicted = outputs.max(1)
            val_total += labels.size(0)
            val_correct += predicted.eq(labels).sum().item()

    val_acc = 100.0 * val_correct / val_total

    # Print progress
    print(f"Epoch {epoch+1}/{num_epochs}")
    print(f"Train Loss: {train_loss/len(train_loader):.4f}, Train Acc: {train_acc:.2f}%")
    print(f"Val Loss: {val_loss/len(val_loader):.4f}, Val Acc: {val_acc:.2f}%")

    # Save best model
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), 'soil_classifier_best.pth')
        print(f"Best model saved! Val Acc: {val_acc:.2f}%")

    # Learning rate scheduling
    scheduler.step(val_acc)
```

**3. Evaluation**:
```python
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# Load best model
model.load_state_dict(torch.load('soil_classifier_best.pth'))
model.eval()

# Predict on test set
test_dataset = datasets.ImageFolder('soil_images/test', transform=val_transform)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)
        outputs = model(images)
        _, predicted = outputs.max(1)

        all_preds.extend(predicted.cpu().numpy())
        all_labels.extend(labels.numpy())

# Metrics
accuracy = 100.0 * sum(np.array(all_preds) == np.array(all_labels)) / len(all_labels)
print(f"Test Accuracy: {accuracy:.2f}%")

# Classification report
class_names = ['Alluvial', 'Black', 'Clay', 'Red']
print(classification_report(all_labels, all_preds, target_names=class_names))

# Confusion matrix
cm = confusion_matrix(all_labels, all_preds)
print(cm)
```

**4. Save Model**:
```python
# Save complete model with metadata
model_package = {
    'model_state_dict': model.state_dict(),
    'class_names': class_names,
    'accuracy': accuracy,
    'input_size': (224, 224),
    'normalization': {
        'mean': [0.485, 0.456, 0.406],
        'std': [0.229, 0.224, 0.225]
    },
    'training_date': pd.Timestamp.now().isoformat()
}

torch.save(model_package, 'soil_classifier_v1.0.pth')
```

### 8.3.7 Inference Process

**Load Model**:
```python
import torch
from PIL import Image

# Load model package
checkpoint = torch.load('soil_classifier_v1.0.pth', map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()
model.to(device)

class_names = checkpoint['class_names']
```

**Single Image Prediction**:
```python
def classify_soil(image_path):
    """
    Classify soil type from image

    Args:
        image_path (str): Path to soil image

    Returns:
        dict: {
            'soil_type': 'Alluvial',
            'confidence': 0.89,
            'all_probabilities': {
                'Alluvial': 0.89,
                'Black': 0.06,
                'Clay': 0.03,
                'Red': 0.02
            },
            'processing_time_ms': 145
        }
    """
    import time
    start_time = time.time()

    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    image_tensor = val_transform(image=np.array(image))['image']
    image_tensor = image_tensor.unsqueeze(0).to(device)

    # Predict
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]

    # Get top prediction
    confidence, predicted_idx = torch.max(probabilities, 0)
    soil_type = class_names[predicted_idx.item()]

    # All probabilities
    all_probs = {
        class_names[i]: float(probabilities[i])
        for i in range(len(class_names))
    }

    processing_time = (time.time() - start_time) * 1000

    return {
        'soil_type': soil_type,
        'confidence': float(confidence),
        'all_probabilities': all_probs,
        'processing_time_ms': int(processing_time)
    }
```

### 8.3.8 Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Accuracy | ≥ 85% | 88.5% ✅ |
| Training Time | < 4 hours | 2.5 hours ✅ |
| Inference Time | < 500ms | 145ms ✅ |
| Model Size | < 100MB | 94MB ✅ |
| F1-Score (weighted) | ≥ 0.85 | 0.88 ✅ |

**Per-Class Performance** (Example):
```
              precision    recall  f1-score   support

    Alluvial       0.91      0.89      0.90       338
       Black       0.87      0.91      0.89       338
        Clay       0.86      0.84      0.85       338
         Red       0.90      0.89      0.90       338

    accuracy                           0.88      1352
   macro avg       0.88      0.88      0.88      1352
weighted avg       0.88      0.88      0.88      1352
```

---

## 8.4 Fertilizer Recommendation Engine

### 8.4.1 Crop-Fertilizer Mapping

**Complete Mapping** (All 22 Crops):

```python
FERTILIZER_MAP = {
    'rice': {
        'name': 'Urea',
        'dosage': '120 kg/ha',
        'timing': 'Split doses: 50% at planting, 30% at tillering, 20% at flowering',
        'cost_per_acre': 3000,  # INR
        'alternative': 'NPK (20-20-0)'
    },
    'maize': {
        'name': 'DAP (Di-Ammonium Phosphate)',
        'dosage': '100 kg/ha',
        'timing': '100% at planting (basal application)',
        'cost_per_acre': 3500,
        'alternative': 'NPK (10-26-26)'
    },
    'chickpea': {
        'name': 'SSP (Single Super Phosphate)',
        'dosage': '60 kg/ha',
        'timing': '100% at sowing',
        'cost_per_acre': 1800,
        'alternative': 'DAP (50 kg/ha)'
    },
    'kidneybeans': {
        'name': 'NPK (10-26-26)',
        'dosage': '80 kg/ha',
        'timing': '100% at sowing',
        'cost_per_acre': 2800,
        'alternative': 'Vermicompost (2 tons/ha)'
    },
    'pigeonpeas': {
        'name': 'DAP',
        'dosage': '50 kg/ha',
        'timing': '100% at sowing',
        'cost_per_acre': 1750,
        'alternative': 'SSP (80 kg/ha)'
    },
    'mothbeans': {
        'name': 'SSP',
        'dosage': '40 kg/ha',
        'timing': '100% at sowing',
        'cost_per_acre': 1200,
        'alternative': 'Organic compost (1.5 tons/ha)'
    },
    'mungbean': {
        'name': 'DAP',
        'dosage': '50 kg/ha',
        'timing': '100% at sowing',
        'cost_per_acre': 1750,
        'alternative': 'SSP (70 kg/ha)'
    },
    'blackgram': {
        'name': 'SSP',
        'dosage': '60 kg/ha',
        'timing': '100% at sowing',
        'cost_per_acre': 1800,
        'alternative': 'DAP (40 kg/ha)'
    },
    'lentil': {
        'name': 'DAP',
        'dosage': '50 kg/ha',
        'timing': '100% at sowing',
        'cost_per_acre': 1750,
        'alternative': 'SSP (80 kg/ha)'
    },
    'pomegranate': {
        'name': 'NPK (19-19-19)',
        'dosage': '250 kg/ha/year',
        'timing': 'Split in 4 doses (Feb, May, Aug, Nov)',
        'cost_per_acre': 8000,
        'alternative': 'Organic manure (10 kg/tree)'
    },
    'banana': {
        'name': 'NPK (10-26-26) + Urea',
        'dosage': '200 kg NPK + 150 kg Urea per ha',
        'timing': 'NPK at planting, Urea in 3 split doses',
        'cost_per_acre': 9000,
        'alternative': 'Vermicompost (5 tons/ha)'
    },
    'mango': {
        'name': 'NPK (15-15-15)',
        'dosage': '150 kg/ha/year',
        'timing': 'Split in 3 doses (Feb, Jun, Sep)',
        'cost_per_acre': 5000,
        'alternative': 'FYM (25 kg/tree)'
    },
    'grapes': {
        'name': 'NPK (19-19-19)',
        'dosage': '200 kg/ha',
        'timing': 'Split in 4 doses throughout growing season',
        'cost_per_acre': 6500,
        'alternative': 'Organic compost (5 tons/ha)'
    },
    'watermelon': {
        'name': 'NPK (12-32-16)',
        'dosage': '120 kg/ha',
        'timing': '50% at planting, 25% at flowering, 25% at fruiting',
        'cost_per_acre': 4200,
        'alternative': 'Vermicompost (3 tons/ha)'
    },
    'muskmelon': {
        'name': 'NPK (12-32-16)',
        'dosage': '100 kg/ha',
        'timing': '50% at planting, 50% at flowering',
        'cost_per_acre': 3500,
        'alternative': 'FYM (10 tons/ha)'
    },
    'apple': {
        'name': 'NPK (12-12-36)',
        'dosage': '180 kg/ha/year',
        'timing': 'Split in 3 doses (Mar, May, Jul)',
        'cost_per_acre': 6000,
        'alternative': 'Organic manure (30 kg/tree)'
    },
    'orange': {
        'name': 'NPK (10-10-10)',
        'dosage': '150 kg/ha/year',
        'timing': 'Split in 3 doses (Feb, Jun, Sep)',
        'cost_per_acre': 4800,
        'alternative': 'Vermicompost (8 kg/tree)'
    },
    'papaya': {
        'name': 'NPK (12-12-12) + Urea',
        'dosage': '100 kg NPK + 80 kg Urea per ha',
        'timing': 'Split in monthly doses',
        'cost_per_acre': 5500,
        'alternative': 'FYM (20 kg/plant)'
    },
    'coconut': {
        'name': 'NPK (12-18-20)',
        'dosage': '2 kg/tree/year',
        'timing': 'Split in 2 doses (Jun, Dec)',
        'cost_per_acre': 7000,
        'alternative': 'Vermicompost (25 kg/tree)'
    },
    'cotton': {
        'name': 'Urea + DAP',
        'dosage': '130 kg Urea + 100 kg DAP per ha',
        'timing': 'DAP at sowing, Urea in 3 split doses',
        'cost_per_acre': 5200,
        'alternative': 'NPK (10-26-26)'
    },
    'jute': {
        'name': 'Urea + SSP',
        'dosage': '80 kg Urea + 60 kg SSP per ha',
        'timing': 'SSP at sowing, Urea at 30 days',
        'cost_per_acre': 2800,
        'alternative': 'NPK (10-10-10)'
    },
    'coffee': {
        'name': 'Organic Fertilizer (FYM)',
        'dosage': '10 kg/plant/year',
        'timing': 'Split in 2 doses (May, Sep)',
        'cost_per_acre': 6000,
        'alternative': 'Vermicompost (8 kg/plant) + Bone meal (500g/plant)'
    }
}
```

### 8.4.2 Recommendation Function

```python
def get_fertilizer_recommendation(crop_name):
    """
    Get fertilizer recommendation for a crop

    Args:
        crop_name (str): Name of the crop

    Returns:
        dict: Fertilizer details
    """
    if crop_name.lower() not in FERTILIZER_MAP:
        return {
            'name': 'NPK (10-26-26)',
            'dosage': '100 kg/ha',
            'timing': 'Consult local agricultural expert',
            'cost_per_acre': 3000,
            'alternative': 'Organic compost'
        }

    return FERTILIZER_MAP[crop_name.lower()]
```

### 8.4.3 Advanced Recommendations (Soil-Specific)

**Adjust dosage based on soil test results**:

```python
def adjust_fertilizer_dosage(crop, soil_params):
    """
    Adjust fertilizer dosage based on soil nutrient levels

    Args:
        crop (str): Crop name
        soil_params (dict): {'N': 90, 'P': 42, 'K': 43, 'ph': 6.5}

    Returns:
        dict: Adjusted fertilizer recommendation
    """
    base_recommendation = get_fertilizer_recommendation(crop)

    # Parse base dosage (e.g., "120 kg/ha" → 120)
    base_dosage = int(base_recommendation['dosage'].split()[0])

    # Adjustment factors based on soil nutrients
    adjustments = []

    # Nitrogen adjustment
    if soil_params['N'] < 40:
        base_dosage *= 1.2  # Increase by 20%
        adjustments.append("Low nitrogen - increased dosage")
    elif soil_params['N'] > 100:
        base_dosage *= 0.8  # Decrease by 20%
        adjustments.append("High nitrogen - reduced dosage")

    # Phosphorus adjustment
    if soil_params['P'] < 30:
        adjustments.append("Consider adding extra phosphate")

    # pH adjustment
    if soil_params['ph'] < 5.5:
        adjustments.append("Acidic soil - apply lime (500 kg/ha) before fertilizer")
    elif soil_params['ph'] > 8.0:
        adjustments.append("Alkaline soil - apply gypsum (1 ton/ha)")

    return {
        **base_recommendation,
        'adjusted_dosage': f"{int(base_dosage)} kg/ha",
        'adjustments': adjustments
    }
```

---

## 8.5 Model Versioning & Deployment

### 8.5.1 Version Control

**Naming Convention**:
- Format: `{model_type}_v{major}.{minor}.{patch}`
- Example: `crop_predictor_v1.2.0`, `soil_classifier_v2.0.1`

**Semantic Versioning**:
- **Major (X.0.0)**: Breaking changes (different input/output format)
- **Minor (0.X.0)**: New features, accuracy improvements
- **Patch (0.0.X)**: Bug fixes, minor improvements

### 8.5.2 Model Registry (Database)

**Storage in Supabase**:
```sql
SELECT * FROM ml_models WHERE is_deployed = TRUE;
```

**Metadata Tracked**:
- Model name & version
- Training dataset ID
- Hyperparameters
- Training metrics (accuracy, loss, f1-score)
- Evaluation metrics (test set performance)
- Confusion matrix
- File URL (Supabase Storage)
- Deployment status & date
- Trained by (admin user ID)

### 8.5.3 Deployment Process

**1. Admin Review**:
- View evaluation metrics
- Compare with current deployed model
- Decide: Deploy, Reject, or Retrain

**2. Deployment (Django)**:
```python
def deploy_model(model_id):
    """Deploy a trained model to production"""
    supabase = get_supabase_admin()

    # Get model metadata
    model = supabase.table('ml_models').select('*').eq('id', model_id).execute()
    model_data = model.data[0]

    # Check minimum accuracy threshold
    accuracy = model_data['training_metrics']['accuracy']
    if accuracy < 0.80:  # 80% threshold
        raise ValueError(f"Model accuracy ({accuracy:.2%}) below threshold (80%)")

    # Undeploy old model
    supabase.table('ml_models').update({'is_deployed': False}).eq('type', model_data['type']).eq('is_deployed', True).execute()

    # Deploy new model
    supabase.table('ml_models').update({
        'is_deployed': True,
        'deployed_at': datetime.now().isoformat()
    }).eq('id', model_id).execute()

    # Download model file to Django server
    model_url = model_data['model_file_url']
    local_path = f"ml_models/deployed/{model_data['type']}_latest.pkl"
    download_file(model_url, local_path)

    # Reload model in memory (hot reload)
    reload_models()

    # Log activity
    log_admin_activity('deploy_model', model_id, f"Deployed {model_data['name']}")

    return {'success': True, 'model': model_data['name']}
```

**3. Hot Reload** (without restarting Django):
```python
# Global model cache
_model_cache = {}

def reload_models():
    """Reload all deployed models"""
    global _model_cache

    # Clear cache
    _model_cache = {}

    # Load crop predictor
    crop_model_path = 'ml_models/deployed/crop_predictor_latest.pkl'
    if os.path.exists(crop_model_path):
        _model_cache['crop_predictor'] = joblib.load(crop_model_path)

    # Load soil classifier
    soil_model_path = 'ml_models/deployed/soil_classifier_latest.pth'
    if os.path.exists(soil_model_path):
        checkpoint = torch.load(soil_model_path)
        model = SoilClassifier()
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        _model_cache['soil_classifier'] = model

def get_model(model_type):
    """Get model from cache"""
    if model_type not in _model_cache:
        reload_models()
    return _model_cache.get(model_type)
```

### 8.5.4 Rollback Strategy

**If new model performs poorly**:
```python
def rollback_model(model_type):
    """Rollback to previous deployed model"""
    supabase = get_supabase_admin()

    # Get current deployed model
    current = supabase.table('ml_models').select('*').eq('type', model_type).eq('is_deployed', True).execute()

    # Undeploy current
    supabase.table('ml_models').update({'is_deployed': False}).eq('id', current.data[0]['id']).execute()

    # Get previous version (highest version before current, sorted by created_at)
    previous = supabase.table('ml_models').select('*').eq('type', model_type).eq('is_deployed', False).order('created_at', desc=True).limit(1).execute()

    # Redeploy previous
    supabase.table('ml_models').update({
        'is_deployed': True,
        'deployed_at': datetime.now().isoformat()
    }).eq('id', previous.data[0]['id']).execute()

    # Download and reload
    reload_models()

    return {'success': True, 'rolled_back_to': previous.data[0]['name']}
```

---

## 8.6 Model Monitoring

### 8.6.1 Performance Tracking

**Log every prediction**:
```python
def log_prediction(model_type, input_features, output, confidence, inference_time):
    """Log prediction for model monitoring"""
    supabase.table('model_predictions_log').insert({
        'model_id': get_deployed_model_id(model_type),
        'input_features': input_features,
        'output_probabilities': output,
        'prediction_confidence': confidence,
        'inference_time_ms': inference_time,
        'timestamp': datetime.now().isoformat()
    }).execute()
```

### 8.6.2 Drift Detection

**Monitor for model drift** (performance degradation over time):

```python
def check_model_drift(model_type, window_days=30):
    """
    Check if model performance is degrading

    Args:
        model_type (str): 'crop_predictor' or 'soil_classifier'
        window_days (int): Time window for analysis

    Returns:
        dict: Drift report
    """
    # Get predictions with user feedback
    cutoff_date = datetime.now() - timedelta(days=window_days)

    predictions = supabase.table('predictions').select('*').gte('created_at', cutoff_date.isoformat()).execute()

    # Calculate accuracy from user feedback
    feedback_count = 0
    correct_count = 0

    for pred in predictions.data:
        if pred['user_planted'] is not None:
            feedback_count += 1
            if pred['user_planted'] == True and pred['actual_yield'] > 0:
                correct_count += 1

    if feedback_count == 0:
        return {'drift_detected': False, 'reason': 'Insufficient feedback data'}

    current_accuracy = correct_count / feedback_count

    # Get baseline accuracy (from training)
    model = supabase.table('ml_models').select('*').eq('type', model_type).eq('is_deployed', True).execute()
    baseline_accuracy = model.data[0]['training_metrics']['accuracy']

    # Check for significant drop (> 10%)
    drift_threshold = 0.10
    if (baseline_accuracy - current_accuracy) > drift_threshold:
        return {
            'drift_detected': True,
            'baseline_accuracy': baseline_accuracy,
            'current_accuracy': current_accuracy,
            'degradation': baseline_accuracy - current_accuracy,
            'recommendation': 'Retrain model with recent data'
        }

    return {
        'drift_detected': False,
        'baseline_accuracy': baseline_accuracy,
        'current_accuracy': current_accuracy
    }
```

---

# 9. FUNCTIONAL REQUIREMENTS

## 9.1 User Management

### FR-1.1: User Registration
- **Priority**: P0 (Critical)
- **Description**: Users can create accounts with email and phone
- **Acceptance Criteria**:
  - User provides: Full name, email, phone, password, state, district
  - Email verification via Supabase (verification link sent)
  - Phone verification optional (SMS OTP)
  - Password strength validation (min 8 chars, alphanumeric + special char)
  - Duplicate email/phone prevention
  - Success message displayed
  - Auto-redirect to login page
- **Dependencies**: Supabase Auth configured

### FR-1.2: User Login
- **Priority**: P0 (Critical)
- **Description**: Users can authenticate with email/password or social login
- **Acceptance Criteria**:
  - Login with email + password
  - Login with Google account (OAuth)
  - Login with GitHub account (OAuth)
  - Session management via Django (JWT tokens stored)
  - "Remember me" option (extends session to 7 days)
  - Failed login limit: 5 attempts → 15-minute lockout
  - Success: Redirect to dashboard
- **Dependencies**: Supabase Auth, Google/GitHub OAuth apps configured

### FR-1.3: Password Reset
- **Priority**: P1 (High)
- **Description**: Users can reset forgotten passwords
- **Acceptance Criteria**:
  - "Forgot password?" link on login page
  - Enter email → Supabase sends reset link
  - Link valid for 1 hour
  - User sets new password (same validation rules)
  - Success message + redirect to login
- **Dependencies**: Supabase Auth email templates configured

### FR-1.4: Profile Management
- **Priority**: P1 (High)
- **Description**: Users can view and update their profiles
- **Acceptance Criteria**:
  - View current profile (name, email, phone, state, district)
  - Update: Phone, state, district (email cannot be changed)
  - Change password (requires current password)
  - Success/error messages displayed
- **Dependencies**: None

### FR-1.5: User Logout
- **Priority**: P0 (Critical)
- **Description**: Users can log out securely
- **Acceptance Criteria**:
  - Logout button visible on all authenticated pages
  - Click → Clear Django session
  - Call `supabase.auth.sign_out()`
  - Redirect to homepage
- **Dependencies**: None

---

## 9.2 Crop Prediction

### FR-2.1: Input Soil Parameters
- **Priority**: P0 (Critical)
- **Description**: Users enter 7 soil parameters for prediction
- **Acceptance Criteria**:
  - Form fields: N, P, K, Temperature, Humidity, pH, Rainfall
  - Input validation (ranges enforced):
    - N: 0-140 kg/ha
    - P: 5-145 kg/ha
    - K: 5-205 kg/ha
    - Temperature: 8-43°C
    - Humidity: 14-100%
    - pH: 3.5-9.5
    - Rainfall: 20-300 mm
  - Real-time validation feedback (red border for errors)
  - Info icons with tooltips (explain each parameter)
  - "Save Template" button (save values to localStorage for reuse)
  - "Clear Form" button
- **Dependencies**: None

### FR-2.2: Upload Soil Image (Optional)
- **Priority**: P1 (High)
- **Description**: Users can upload soil images for classification
- **Acceptance Criteria**:
  - Drag-and-drop file upload zone
  - Click to browse files
  - Supported formats: JPG, PNG
  - Max file size: 5MB
  - Preview thumbnail after upload
  - "Remove" button to delete uploaded image
  - Validation: Reject invalid formats/sizes with error message
- **Dependencies**: Supabase Storage bucket `soil-images` created

### FR-2.3: Crop Prediction
- **Priority**: P0 (Critical)
- **Description**: System predicts top 3 crops based on inputs
- **Acceptance Criteria**:
  - Submit button disabled if form invalid
  - On submit: Show loading overlay ("Analyzing...")
  - If image uploaded: Run soil classification first
  - Load deployed crop prediction model
  - Normalize input features
  - Run inference → Get probabilities for 22 crops
  - Return top 3 crops with confidence scores
  - Map each crop to fertilizer recommendation
  - Processing time: < 3 seconds
  - Save prediction to database
  - Redirect to results page
- **Dependencies**: Trained crop prediction model deployed

### FR-2.4: Soil Classification (If Image Uploaded)
- **Priority**: P1 (High)
- **Description**: Classify soil type from uploaded image
- **Acceptance Criteria**:
  - Upload image to Supabase Storage
  - Preprocess: Resize to 224×224, normalize
  - Load deployed soil classification model
  - Run inference → Get soil type (Alluvial/Black/Clay/Red)
  - Return confidence score
  - Processing time: < 5 seconds
  - Include soil type in crop prediction
- **Dependencies**: Trained soil classification model deployed

### FR-2.5: Display Results
- **Priority**: P0 (Critical)
- **Description**: Show prediction results to user
- **Acceptance Criteria**:
  - Top 3 crops displayed (#1 expanded, #2/#3 collapsible)
  - Each crop shows:
    - Name, confidence (progress bar)
    - "Why this crop?" explanation (3-5 bullet points)
    - Fertilizer: Name, dosage, timing, cost estimate
  - If soil classified:
    - Soil type, confidence
    - Side-by-side images (user's vs reference)
    - Characteristics
  - Action buttons:
    - "Save to History" (auto-saved, just confirmation)
    - "Download PDF" (generate PDF report)
    - "Share" (copy link to clipboard)
    - "New Prediction" (go to form)
  - Disclaimer at bottom
- **Dependencies**: None

---

## 9.3 Prediction History

### FR-3.1: View Prediction History
- **Priority**: P1 (High)
- **Description**: Users can view all past predictions
- **Acceptance Criteria**:
  - List all predictions for logged-in user
  - Order: Most recent first
  - Each prediction card shows:
    - Date/time, crop, confidence, soil type, fertilizer
    - User feedback section (if not provided)
    - View details, Download PDF buttons
  - Pagination: 10 predictions per page
  - "Load More" button or infinite scroll
- **Dependencies**: None

### FR-3.2: Filter Predictions
- **Priority**: P2 (Medium)
- **Description**: Users can filter prediction history
- **Acceptance Criteria**:
  - Filters:
    - Date range (presets: Last 7 days, Last 30 days, Last 3 months, Custom)
    - Crop type (multi-select dropdown, 22 crops + "All")
  - "Apply Filters" button → Reload list
  - URL updates with query parameters
  - Clear filters button
- **Dependencies**: None

### FR-3.3: User Feedback
- **Priority**: P1 (High)
- **Description**: Users can provide feedback on predictions
- **Acceptance Criteria**:
  - For each prediction: "Did you plant this?" → Yes/No buttons
  - If Yes: Show input field for actual yield (quintals/acre)
  - On submit: Update database (`user_planted`, `actual_yield`)
  - Show success toast: "Thank you for your feedback!"
  - Display feedback on card (✅ Planted, Actual yield, Accuracy comparison)
- **Dependencies**: None

### FR-3.4: Export Predictions
- **Priority**: P2 (Medium)
- **Description**: Users can export prediction history
- **Acceptance Criteria**:
  - "Download All as CSV" button
  - Generates CSV file with columns: Date, Crop, Confidence, Soil Type, Fertilizer, Planted, Yield
  - File name: `predictions_{user_id}_{date}.csv`
  - "Email Report" button (weekly/monthly summary) - Optional
- **Dependencies**: None

---

## 9.4 Admin - Dataset Management

### FR-4.1: Upload Dataset
- **Priority**: P0 (Critical)
- **Description**: Admins can upload training datasets
- **Acceptance Criteria**:
  - Select dataset type: Crop Data (CSV) or Soil Images (ZIP)
  - Enter: Name, Version
  - Upload file (drag-and-drop or browse)
  - Validation:
    - Crop CSV: Check schema (7 features + label), value ranges, missing values
    - Soil ZIP: Check folder structure (4 folders), image formats, minimum 100 images per class
  - Preview: Show first 10 rows (CSV) or 20 images (ZIP)
  - Validation report generated (saved to database)
  - Upload to Supabase Storage
  - Save metadata to `datasets` table
  - Status: 'uploaded' → Admin must activate later
- **Dependencies**: Supabase Storage bucket `datasets` created

### FR-4.2: List Datasets
- **Priority**: P1 (High)
- **Description**: Admins can view all uploaded datasets
- **Acceptance Criteria**:
  - Table with columns: ID, Name, Type, Version, Samples, Status, Actions
  - Sortable columns
  - Status: Uploaded, Validated, Active, Archived
  - Actions: View (preview), Activate (set status='active'), Archive, Delete
  - Pagination: 20 datasets per page
- **Dependencies**: None

### FR-4.3: Activate Dataset
- **Priority**: P1 (High)
- **Description**: Admins can activate validated datasets
- **Acceptance Criteria**:
  - Only datasets with status='uploaded' or 'validated' can be activated
  - Click "Activate" → Update status='active', set activated_at timestamp
  - Success message: "Dataset activated. You can now use it for training."
- **Dependencies**: Dataset validation passed

---

## 9.5 Admin - Model Training

### FR-5.1: Start Training
- **Priority**: P0 (Critical)
- **Description**: Admins can train new ML models
- **Acceptance Criteria**:
  - Select model type: Crop Predictor or Soil Classifier
  - Select dataset (dropdown of active datasets matching type)
  - Configure hyperparameters:
    - Epochs (1-100)
    - Batch size (16, 32, 64)
    - Learning rate (0.0001-0.1)
    - Test split (10-30%)
  - Click "Start Training" → Trigger background task
  - Show loading state
  - Disable form while training in progress
- **Dependencies**: At least one active dataset exists

### FR-5.2: Monitor Training Progress
- **Priority**: P1 (High)
- **Description**: Admins can monitor real-time training progress
- **Acceptance Criteria**:
  - Progress card appears (replace form)
  - Display:
    - Model name, status ("Training...")
    - Current epoch (e.g., "Epoch 7/10")
    - Progress bar (0-100%)
    - Current accuracy & loss
    - Live chart (accuracy/loss over epochs, updates each epoch)
    - Estimated time remaining
  - "Cancel Training" button (abort task)
  - Updates via WebSocket or AJAX polling (every 2 seconds)
- **Dependencies**: Background task framework (Celery or threading)

### FR-5.3: Evaluate Model
- **Priority**: P0 (Critical)
- **Description**: Admins can review model performance after training
- **Acceptance Criteria**:
  - On training complete: Show evaluation page
  - Display metrics:
    - Overall accuracy (large, prominent)
    - Precision, Recall, F1-Score (weighted avg)
    - Per-class performance table
    - Confusion matrix (heatmap)
  - If accuracy >= 80%: Show "Deploy Model" button (green)
  - If accuracy < 80%: Show warning + "Retrain" button
  - Actions: Deploy, Discard, Download Model
- **Dependencies**: Training completed successfully

### FR-5.4: Deploy Model
- **Priority**: P0 (Critical)
- **Description**: Admins can deploy trained models to production
- **Acceptance Criteria**:
  - Click "Deploy Model" → Confirmation modal
  - Modal: "Deploy {model_name}? This will replace the current model."
  - On confirm:
    - Undeploy current model (set is_deployed=False)
    - Deploy new model (set is_deployed=True, deployed_at=NOW)
    - Upload model file to Supabase Storage
    - Download to Django server
    - Reload model in memory (hot reload)
  - Success message: "Model deployed successfully!"
  - Redirect to models list
- **Dependencies**: Model accuracy >= 80%

### FR-5.5: List Models
- **Priority**: P1 (High)
- **Description**: Admins can view all trained models
- **Acceptance Criteria**:
  - Table with columns: ID, Name, Type, Accuracy, Status, Actions
  - Status indicator: 🟢 Live, 🟡 Archived
  - Actions: Evaluate, Deploy (if not deployed), Rollback (if deployed), Delete
  - Sortable by version (desc), accuracy
  - Pagination: 20 models per page
- **Dependencies**: None

### FR-5.6: Rollback Model
- **Priority**: P1 (High)
- **Description**: Admins can rollback to previous model version
- **Acceptance Criteria**:
  - Click "Rollback" on deployed model
  - Confirmation modal: "Rollback to previous version?"
  - On confirm:
    - Undeploy current model
    - Deploy most recent previous version
    - Reload models
  - Success message: "Rolled back to {previous_model_name}"
- **Dependencies**: At least 2 versions of model exist

---

## 9.6 Admin - Activity Logging

### FR-6.1: Log Admin Actions
- **Priority**: P1 (High)
- **Description**: All admin actions are logged for audit
- **Acceptance Criteria**:
  - Logged actions: Upload dataset, Train model, Deploy model, Rollback model, Delete dataset/model
  - Log includes: Admin ID, action, resource type, resource ID, details (JSON), IP address, timestamp
  - Logs stored in `admin_activity_log` table
  - Retention: 90 days
- **Dependencies**: None

### FR-6.2: View Activity Logs
- **Priority**: P2 (Medium)
- **Description**: Admins can view activity logs
- **Acceptance Criteria**:
  - Table with columns: Date/Time, Admin, Action, Resource, Details
  - Filter by: Date range, Admin, Action type
  - Sortable by timestamp (desc default)
  - Pagination: 50 logs per page
  - Export to CSV option
- **Dependencies**: None

---

# 10. NON-FUNCTIONAL REQUIREMENTS

## 10.1 Performance

### NFR-1.1: Response Time
- **Crop Prediction**: < 3 seconds (from form submit to results page)
- **Soil Classification**: < 5 seconds (from image upload to result)
- **Page Load Time**: < 2 seconds (all pages)
- **Model Training**: < 4 hours (Soil CNN), < 10 minutes (Crop XGBoost)
- **API Response**: < 500ms (95th percentile)

### NFR-1.2: Throughput
- **Concurrent Users**: Support 1,000 concurrent users
- **Predictions per Day**: Handle 10,000 predictions/day
- **Database Queries**: < 100ms (95th percentile)

### NFR-1.3: Scalability
- **User Growth**: Support up to 50,000 registered users
- **Database Size**: Handle 10M prediction records
- **Horizontal Scaling**: Supabase scales automatically
- **Django Instances**: Can deploy multiple instances behind load balancer

### NFR-1.4: Resource Utilization
- **CPU**: < 70% average utilization
- **Memory**: < 2GB per Django instance
- **Disk**: < 10GB for ML models, logs, and temp files

---

## 10.2 Security

### NFR-2.1: Authentication
- **Password Hashing**: PBKDF2 with SHA256 (Django default) or bcrypt (Supabase)
- **Password Policy**: Min 8 chars, alphanumeric + special char
- **Session Management**: JWT tokens with 30-min expiry
- **Refresh Tokens**: 7-day expiry, stored in database
- **Account Lockout**: 5 failed login attempts → 15-minute lockout

### NFR-2.2: Data Protection
- **HTTPS**: All traffic encrypted with TLS 1.3
- **SQL Injection**: Prevented via Supabase SDK (parameterized queries)
- **XSS**: Django auto-escaping in templates
- **CSRF**: Django CSRF middleware enabled
- **File Upload**: Validate file type, size, scan for malware (optional)

### NFR-2.3: Row-Level Security (RLS)
- **Supabase RLS**: Users can only view/edit their own predictions
- **Admin Access**: Admins can view all data (via role check)
- **Storage Access**: Users can only upload to their own folder

### NFR-2.4: Privacy
- **Data Retention**: Predictions stored for 2 years, then archived/deleted
- **User Deletion**: Users can request account deletion (GDPR compliance)
- **Data Anonymization**: Analytics use anonymized data
- **No Third-Party Sharing**: User data never shared without consent

---

## 10.3 Reliability

### NFR-3.1: Availability
- **Uptime**: 99.5% (excluding planned maintenance)
- **Planned Maintenance**: Max 4 hours/month (Sunday 2-6 AM)
- **Downtime**: < 43.8 hours/year

### NFR-3.2: Error Handling
- **User-Friendly Errors**: No technical stack traces shown to users
- **Graceful Degradation**: If ML model fails, show cached recommendations
- **Retry Logic**: Automatic retry for transient errors (max 3 attempts)
- **Fallback**: If Supabase down, queue requests and process later

### NFR-3.3: Data Backup
- **Supabase Backups**: Automatic daily backups (Supabase manages)
- **Retention**: 30 days
- **Recovery Point Objective (RPO)**: 24 hours
- **Recovery Time Objective (RTO)**: 4 hours

---

## 10.4 Usability

### NFR-4.1: Accessibility
- **WCAG 2.1 Level AA**: Compliance target
- **Color Contrast**: Min 4.5:1 for text, 3:1 for large text
- **Keyboard Navigation**: All features accessible via keyboard
- **Screen Readers**: ARIA labels, semantic HTML
- **Focus Indicators**: Visible focus outline (2px solid green)

### NFR-4.2: Responsive Design
- **Mobile Support**: Fully functional on smartphones (320px width+)
- **Tablet Support**: Optimized for tablets (768px width+)
- **Desktop Support**: Full features on desktops (1024px width+)
- **Touch Targets**: Min 44×44px for buttons

### NFR-4.3: Browser Support
- **Chrome**: Version 90+ ✅
- **Firefox**: Version 88+ ✅
- **Safari**: Version 14+ ✅
- **Edge**: Version 90+ ✅
- **Mobile Browsers**: iOS Safari 14+, Chrome Mobile 90+

### NFR-4.4: Internationalization (Future)
- **Language**: English (primary), Hindi/Tamil/Telugu (future)
- **Date/Time**: Display per user's locale
- **Units**: Metric system (kg, mm, °C)

---

## 10.5 Maintainability

### NFR-5.1: Code Quality
- **PEP 8**: Python code follows PEP 8 style guide
- **Code Coverage**: > 70% test coverage (target: 80%)
- **Documentation**: All functions documented with docstrings
- **Comments**: Complex logic has inline comments

### NFR-5.2: Logging
- **Application Logs**: Django logs to file + console
- **Log Levels**: DEBUG (dev), INFO (production), ERROR (always)
- **Log Rotation**: Daily rotation, 7-day retention
- **Error Tracking**: Sentry integration (optional)

### NFR-5.3: Monitoring
- **Health Check Endpoint**: `/health/` returns 200 OK if system healthy
- **Metrics**: Track response time, error rate, active users
- **Alerts**: Email/SMS if error rate > 5% or uptime < 99%

---

## 10.6 Portability

### NFR-6.1: Database Portability
- **ORM**: Django ORM (can switch from SQLite to MySQL/PostgreSQL)
- **Supabase**: PostgreSQL (standard SQL, portable)

### NFR-6.2: Deployment Options
- **Local**: Django dev server
- **Production**: Gunicorn + Nginx, Docker, Cloud (AWS/GCP/Azure)
- **Containerization**: Docker support (optional)

---

# 11. USER STORIES & USE CASES

## 11.1 User Stories

### Epic 1: User Onboarding

**US-1.1**: As a **farmer**, I want to **register with my email and phone** so that **I can access the system**.
- **Acceptance Criteria**:
  - Registration form has Name, Email, Phone, Password, State, District fields
  - Email verification sent upon registration
  - Success message shown
  - Redirected to login page

**US-1.2**: As a **user**, I want to **login with my Google account** so that **I don't have to remember another password**.
- **Acceptance Criteria**:
  - "Continue with Google" button visible
  - Redirects to Google OAuth consent
  - On success, logged in and redirected to dashboard

**US-1.3**: As a **user**, I want to **reset my password** so that **I can regain access if I forget it**.
- **Acceptance Criteria**:
  - "Forgot password?" link on login page
  - Enter email → Receive reset link
  - Click link → Set new password
  - Success message → Redirect to login

---

### Epic 2: Crop Prediction

**US-2.1**: As a **farmer**, I want to **enter soil nutrient values** so that **I can get crop recommendations**.
- **Acceptance Criteria**:
  - Form has 7 input fields (N, P, K, Temp, Humidity, pH, Rainfall)
  - Validation enforces acceptable ranges
  - Info icons explain each parameter

**US-2.2**: As a **farmer**, I want to **upload a soil image** so that **the system can identify my soil type**.
- **Acceptance Criteria**:
  - Drag-and-drop or click to upload
  - Accepts JPG/PNG, max 5MB
  - Preview shown after upload
  - Can remove image

**US-2.3**: As a **user**, I want to **see top 3 crop recommendations with confidence scores** so that **I can make an informed decision**.
- **Acceptance Criteria**:
  - Results page shows #1, #2, #3 crops
  - Each has confidence bar (percentage)
  - #1 is expanded with full details

**US-2.4**: As a **farmer**, I want to **see fertilizer recommendations** so that **I know what to apply**.
- **Acceptance Criteria**:
  - Each crop shows: Fertilizer name, dosage, timing, cost
  - Alternative fertilizer option shown

**US-2.5**: As a **user**, I want to **download prediction results as PDF** so that **I can print or share them**.
- **Acceptance Criteria**:
  - "Download PDF" button visible
  - Generates PDF with all details
  - File downloads automatically

---

### Epic 3: Prediction History

**US-3.1**: As a **farmer**, I want to **view my past predictions** so that **I can track what I've planted**.
- **Acceptance Criteria**:
  - History page lists all predictions
  - Ordered by date (newest first)
  - Shows crop, date, confidence, fertilizer

**US-3.2**: As a **user**, I want to **filter predictions by date range** so that **I can see only relevant results**.
- **Acceptance Criteria**:
  - Date range filter (Last 7/30 days, Custom)
  - Apply filters button reloads list

**US-3.3**: As a **farmer**, I want to **provide feedback on whether I planted the recommended crop** so that **the system can improve**.
- **Acceptance Criteria**:
  - "Did you plant this?" buttons (Yes/No)
  - If Yes: Input for actual yield
  - Feedback saved to database

**US-3.4**: As a **user**, I want to **export my prediction history to CSV** so that **I can analyze it in Excel**.
- **Acceptance Criteria**:
  - "Download CSV" button visible
  - File includes all predictions with details

---

### Epic 4: Admin - Dataset Management

**US-4.1**: As an **admin**, I want to **upload crop datasets** so that **I can train new models**.
- **Acceptance Criteria**:
  - Upload form accepts CSV files
  - Validation checks schema
  - Preview shows first 10 rows
  - Success message on upload

**US-4.2**: As an **admin**, I want to **validate datasets before using them** so that **I ensure data quality**.
- **Acceptance Criteria**:
  - Validation report generated (missing values, outliers, schema)
  - Can view report before activating
  - Can reject/delete if issues found

**US-4.3**: As an **admin**, I want to **activate validated datasets** so that **they can be used for training**.
- **Acceptance Criteria**:
  - "Activate" button visible for validated datasets
  - Status changes to "active"
  - Success message shown

---

### Epic 5: Admin - Model Training

**US-5.1**: As an **admin**, I want to **train crop prediction models** so that **I can improve accuracy**.
- **Acceptance Criteria**:
  - Training form has model type, dataset, hyperparameters
  - Click "Start Training" → Background task starts
  - Real-time progress shown

**US-5.2**: As an **admin**, I want to **see training progress in real-time** so that **I know when it's done**.
- **Acceptance Criteria**:
  - Progress bar shows 0-100%
  - Current epoch, accuracy, loss displayed
  - Live chart updates each epoch

**US-5.3**: As an **admin**, I want to **evaluate model performance** so that **I can decide whether to deploy**.
- **Acceptance Criteria**:
  - Evaluation page shows accuracy, precision, recall, F1
  - Confusion matrix displayed
  - "Deploy" button if accuracy >= 80%

**US-5.4**: As an **admin**, I want to **deploy models to production** so that **users get updated predictions**.
- **Acceptance Criteria**:
  - Deploy button visible
  - Confirmation modal shown
  - Old model undeployed, new model deployed
  - Success message

**US-5.5**: As an **admin**, I want to **rollback to a previous model** so that **I can fix issues quickly**.
- **Acceptance Criteria**:
  - Rollback button visible on deployed models
  - Confirmation modal
  - Previous version redeployed
  - Success message

---

## 11.2 Use Cases

### UC-1: New Farmer Registration and First Prediction

**Actors**: Farmer (Primary), System

**Preconditions**: User has internet access, web browser

**Main Flow**:
1. Farmer navigates to homepage
2. Farmer clicks "Sign Up"
3. Farmer enters: Name, Email, Phone, Password, State, District
4. Farmer agrees to terms & privacy policy
5. Farmer clicks "Sign Up" button
6. System validates inputs
7. System calls `supabase.auth.sign_up()`
8. Supabase creates user in `auth.users` table
9. Trigger creates `user_profiles` record
10. Supabase sends verification email to farmer
11. System shows success message: "Check your email to verify account"
12. System redirects to login page (after 3 seconds)
13. Farmer opens email, clicks verification link
14. Supabase marks email as verified
15. Farmer returns to app, logs in with email + password
16. System authenticates, stores JWT token in session
17. System redirects to dashboard
18. Farmer clicks "Predict Crop" quick action
19. System displays prediction form
20. Farmer enters soil parameters:
    - N: 90 kg/ha
    - P: 42 kg/ha
    - K: 43 kg/ha
    - Temperature: 20.88°C
    - Humidity: 82%
    - pH: 6.5
    - Rainfall: 202.94 mm
21. Farmer uploads soil image (optional)
22. Farmer clicks "Predict Crop"
23. System validates inputs (all within ranges)
24. System shows loading overlay ("Analyzing...")
25. (If image) System uploads image to Supabase Storage
26. (If image) System runs soil classification → Returns "Alluvial, 89% confidence"
27. System loads crop prediction model from cache
28. System normalizes features using StandardScaler
29. System runs MLP/XGBoost inference
30. System gets probabilities for 22 crops
31. System sorts and selects top 3: Rice (92%), Maize (78%), Cotton (72%)
32. System maps crops to fertilizers using FERTILIZER_MAP
33. System saves prediction to `predictions` table
34. System redirects to results page
35. Farmer views top 3 crop recommendations
36. Farmer sees: Rice recommended, Fertilizer: Urea (120 kg/ha), Timing: Split doses, Cost: ₹3,000/acre
37. Farmer sees soil classification: Alluvial Soil (89% confidence)
38. Farmer clicks "Download PDF"
39. System generates PDF report with all details
40. PDF downloads to farmer's device
41. Farmer reviews PDF, decides to plant Rice

**Postconditions**:
- User account created in Supabase
- User profile created
- Prediction saved in database
- Prediction visible in user's history

**Alternative Flows**:
- **3a. Email already exists**:
  - System shows error: "Email already registered. Try logging in."
  - Stop
- **6a. Validation fails** (e.g., password too short):
  - System shows inline error messages
  - Farmer corrects and resubmits
- **23a. Input out of range** (e.g., N = 200):
  - System shows error: "Nitrogen must be between 0-140 kg/ha"
  - Farmer corrects
- **25a. Image upload fails**:
  - System shows warning: "Image upload failed. Continuing without soil classification."
  - Proceed to step 27 (skip soil classification)
- **28a. ML model not found**:
  - System shows error: "Prediction service unavailable. Please try again later."
  - Stop

---

### UC-2: Admin Trains and Deploys New Crop Prediction Model

**Actors**: Admin (Primary), System

**Preconditions**: Admin is logged in, has uploaded and validated a dataset

**Main Flow**:
1. Admin navigates to Admin Dashboard
2. Admin clicks "Train Model"
3. System displays model training form
4. Admin selects:
   - Model Type: Crop Predictor (MLP)
   - Dataset: crops_2025_Q3 (version 1.2, status: active)
   - Hyperparameters: Epochs: 10, Batch Size: 32, Learning Rate: 0.001, Test Split: 20%
5. Admin clicks "Start Training"
6. System validates: Dataset exists and is active
7. System creates background task (Celery or threading)
8. System shows training progress card
9. Background task starts:
   - Downloads dataset from Supabase Storage to `/tmp/dataset.csv`
   - Loads CSV into Pandas DataFrame
   - Splits features (X) and labels (y)
   - Normalizes features with StandardScaler
   - Encodes labels with LabelEncoder
   - Splits into train (80%) and test (20%) with stratification
   - Initializes XGBoost model with specified hyperparameters
   - Training loop for 10 epochs:
     - Epoch 1: Train accuracy: 65.2%, Val accuracy: 62.1%
     - Epoch 2: Train accuracy: 71.5%, Val accuracy: 69.3%
     - ... (progress updates sent to frontend every epoch)
     - Epoch 10: Train accuracy: 86.1%, Val accuracy: 84.2%
   - Training completes (total time: 3.5 minutes)
   - Evaluates on test set:
     - Accuracy: 84.2%
     - Precision: 0.84, Recall: 0.84, F1-Score: 0.84
     - Generates confusion matrix
   - Saves model to `/tmp/crop_predictor_v1.3.pkl` (includes model, scaler, label_encoder)
   - Uploads model file to Supabase Storage (`ml-models/crop_predictor_v1.3.pkl`)
   - Saves metadata to `ml_models` table:
     - name: crop_predictor_v1.3
     - type: crop_predictor
     - framework: xgboost
     - accuracy: 0.842
     - is_deployed: FALSE
10. System hides training progress card
11. System shows success modal: "Training complete! Accuracy: 84.2%"
12. System redirects to evaluation page (URL: `/admin/models/{model_id}/evaluate/`)
13. Evaluation page displays:
    - Model name: crop_predictor_v1.3
    - Training dataset: crops_2025_Q3
    - Accuracy: 84.2% (large, green badge)
    - Precision: 0.84, Recall: 0.84, F1-Score: 0.84
    - Confusion matrix (22×22 heatmap)
    - Per-class performance table (22 rows)
14. Admin reviews metrics
15. Admin decides: Accuracy is good (>80%), proceed with deployment
16. Admin clicks "Deploy Model"
17. System shows confirmation modal: "Deploy crop_predictor_v1.3? This will replace the current model."
18. Admin clicks "Confirm"
19. System:
    - Gets current deployed model (crop_predictor_v1.2)
    - Updates crop_predictor_v1.2: is_deployed = FALSE
    - Updates crop_predictor_v1.3: is_deployed = TRUE, deployed_at = NOW()
    - Downloads model file from Supabase Storage to `ml_models/deployed/crop_predictor_latest.pkl`
    - Calls `reload_models()` function (hot reload, no Django restart needed)
    - Logs admin activity: "deploy_model", model_id, details
20. System shows success toast: "Model deployed successfully!"
21. System redirects to models list
22. Admin sees crop_predictor_v1.3 with status: 🟢 Live
23. Future predictions now use crop_predictor_v1.3

**Postconditions**:
- New model trained and saved
- Model deployed to production
- Old model archived (is_deployed = FALSE)
- Django hot-reloaded model cache
- Admin activity logged

**Alternative Flows**:
- **6a. Dataset not found or inactive**:
  - System shows error: "Selected dataset is not active"
  - Stop
- **9a. Training fails** (e.g., corrupted data):
  - Background task catches exception
  - System shows error modal: "Training failed: {error_message}"
  - Model not saved
  - Admin reviews dataset and retries
- **15a. Accuracy < 80%**:
  - System shows warning: "Accuracy (78.5%) below threshold (80%). Consider retraining with different hyperparameters."
  - "Deploy" button disabled
  - Admin can: Retrain with adjusted hyperparameters, or Discard model
- **19a. Model file download fails**:
  - System shows error: "Deployment failed: Could not download model file"
  - Rollback: Old model remains deployed
  - Admin retries or contacts support

---

# 12. API SPECIFICATIONS

*(Note: Since we're using Supabase SDK and Django views, we don't have traditional REST APIs. However, Django views act as endpoints. Below are the key "endpoints" and their specifications.)*

## 12.1 Authentication Endpoints

### POST /accounts/register/
- **Description**: Register new user
- **Authentication**: None (public)
- **Request Body**:
  ```json
  {
    "name": "Rajesh Kumar",
    "email": "rajesh@example.com",
    "phone": "+919876543210",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
    "state": "Punjab",
    "district": "Ludhiana"
  }
  ```
- **Response (Success)**:
  ```json
  {
    "success": true,
    "message": "Registration successful! Check your email to verify your account.",
    "redirect_url": "/accounts/login/"
  }
  ```
- **Response (Error)**:
  ```json
  {
    "success": false,
    "errors": {
      "email": ["Email already registered"],
      "password": ["Password must be at least 8 characters"]
    }
  }
  ```

### POST /accounts/login/
- **Description**: User login
- **Authentication**: None (public)
- **Request Body**:
  ```json
  {
    "email": "rajesh@example.com",
    "password": "SecurePass123!"
  }
  ```
- **Response (Success)**:
  ```json
  {
    "success": true,
    "message": "Login successful",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "rajesh@example.com",
      "name": "Rajesh Kumar"
    },
    "redirect_url": "/dashboard/"
  }
  ```
- **Response (Error)**:
  ```json
  {
    "success": false,
    "error": "Invalid credentials"
  }
  ```

### POST /accounts/logout/
- **Description**: User logout
- **Authentication**: Required (logged-in user)
- **Response**:
  ```json
  {
    "success": true,
    "message": "Logged out successfully",
    "redirect_url": "/"
  }
  ```

---

## 12.2 Prediction Endpoints

### POST /predictions/create/
- **Description**: Create new crop prediction
- **Authentication**: Required (logged-in user)
- **Request Body** (multipart/form-data):
  ```
  nitrogen: 90.5
  phosphorus: 42.0
  potassium: 43.0
  temperature: 20.88
  humidity: 82.0
  ph: 6.5
  rainfall: 202.94
  soil_image: [File] (optional)
  ```
- **Response (Success)**:
  ```json
  {
    "success": true,
    "prediction_id": "770e8400-e29b-41d4-a716-446655440002",
    "redirect_url": "/predictions/770e8400-e29b-41d4-a716-446655440002/results/"
  }
  ```
- **Response (Error)**:
  ```json
  {
    "success": false,
    "errors": {
      "nitrogen": ["Value must be between 0 and 140"],
      "soil_image": ["File size exceeds 5MB limit"]
    }
  }
  ```

### GET /predictions/{prediction_id}/results/
- **Description**: View prediction results
- **Authentication**: Required (must be prediction owner)
- **Response (Success)**:
  - Renders HTML page with:
    - Top 3 crops with confidence, fertilizer recommendations
    - Soil classification (if image uploaded)
    - Action buttons (Save, Download PDF, Share)

### GET /predictions/history/
- **Description**: View prediction history
- **Authentication**: Required (logged-in user)
- **Query Parameters**:
  - `date_range`: "7" | "30" | "90" (days)
  - `crops`: Comma-separated crop names (e.g., "rice,maize")
  - `page`: Page number (default: 1)
- **Response**: Renders HTML page with prediction list

### POST /predictions/{prediction_id}/feedback/
- **Description**: Submit user feedback on prediction
- **Authentication**: Required (must be prediction owner)
- **Request Body**:
  ```json
  {
    "user_planted": true,
    "actual_yield": 18.5
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Thank you for your feedback!"
  }
  ```

### GET /predictions/export/csv/
- **Description**: Export prediction history to CSV
- **Authentication**: Required (logged-in user)
- **Response**: CSV file download

---

## 12.3 Admin Endpoints

### POST /admin/datasets/upload/
- **Description**: Upload new dataset
- **Authentication**: Required (admin only)
- **Request Body** (multipart/form-data):
  ```
  name: crops_2025_Q4
  type: crop
  version: 1.0
  dataset_file: [File]
  ```
- **Response (Success)**:
  ```json
  {
    "success": true,
    "dataset_id": "880e8400-e29b-41d4-a716-446655440003",
    "validation_report": {
      "schema_check": "passed",
      "missing_values": {"N": 0, "P": 2, "K": 0},
      "recommendations": ["2 missing values in P column - will be imputed"]
    }
  }
  ```

### POST /admin/models/train/
- **Description**: Start model training
- **Authentication**: Required (admin only)
- **Request Body**:
  ```json
  {
    "model_type": "crop_predictor",
    "dataset_id": "880e8400-e29b-41d4-a716-446655440003",
    "hyperparameters": {
      "epochs": 10,
      "batch_size": 32,
      "learning_rate": 0.001,
      "test_split": 0.2
    }
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "task_id": "celery-task-123",
    "message": "Training started"
  }
  ```

### GET /admin/models/{model_id}/progress/
- **Description**: Get training progress (AJAX polling)
- **Authentication**: Required (admin only)
- **Response**:
  ```json
  {
    "status": "training",
    "current_epoch": 7,
    "total_epochs": 10,
    "progress_percent": 70,
    "current_accuracy": 0.823,
    "current_loss": 0.45,
    "estimated_time_remaining_seconds": 480
  }
  ```

### POST /admin/models/{model_id}/deploy/
- **Description**: Deploy trained model
- **Authentication**: Required (admin only)
- **Response**:
  ```json
  {
    "success": true,
    "message": "Model deployed successfully",
    "model_name": "crop_predictor_v1.3"
  }
  ```

---

# 13. SECURITY & PRIVACY

## 13.1 Authentication & Authorization

### 13.1.1 User Authentication
- **Method**: Supabase Auth (email/password, OAuth)
- **Password Storage**: Never stored in plaintext
  - Supabase uses bcrypt hashing
  - Django uses PBKDF2 with SHA256
- **Session Management**:
  - JWT access tokens (30-minute expiry)
  - Refresh tokens (7-day expiry, stored in database)
  - Tokens stored in secure HTTP-only cookies (not localStorage)

### 13.1.2 Authorization
- **Row-Level Security (RLS)**: Enabled on all Supabase tables
  - Users can only access their own predictions
  - Admins have elevated access via role check
- **Django Decorators**:
  - `@supabase_login_required`: Require authentication
  - `@admin_required`: Require admin role

### 13.1.3 API Security
- **CSRF Protection**: Django CSRF middleware enabled for all POST requests
- **Rate Limiting**: (Future) 100 requests/min per user
- **IP Whitelisting**: (Optional) For admin actions

---

## 13.2 Data Protection

### 13.2.1 Encryption
- **In Transit**: HTTPS/TLS 1.3 for all connections
- **At Rest**: Supabase encrypts data at rest (AES-256)
- **File Uploads**: Stored in Supabase Storage with encryption

### 13.2.2 Input Validation
- **Forms**: Django forms with built-in validation
- **File Uploads**:
  - Whitelist allowed extensions (JPG, PNG for images)
  - Check file size (<= 5MB for images, <= 500MB for datasets)
  - Validate file content (not just extension)
  - Rename files to prevent path traversal attacks

### 13.2.3 SQL Injection Prevention
- **Supabase SDK**: Uses parameterized queries (safe by default)
- **Django ORM**: Uses parameterized queries
- **Never use raw SQL** with user input

### 13.2.4 XSS Prevention
- **Django Templates**: Auto-escape HTML by default
- **User Input**: Sanitize before rendering
- **CSP Headers**: (Future) Content Security Policy to prevent inline scripts

---

## 13.3 Privacy & Compliance

### 13.3.1 Data Collection
- **Personal Data Collected**:
  - Name, email, phone, location (state/district)
  - Soil parameters and predictions
  - Soil images (optional)
- **Purpose**: Provide crop prediction service
- **User Consent**: Obtained during registration (checkbox)

### 13.3.2 Data Retention
- **User Accounts**: Stored indefinitely until user requests deletion
- **Predictions**: Stored for 2 years, then archived
- **Logs**: 90 days
- **Backups**: 30 days

### 13.3.3 Data Deletion
- **User Request**: Users can request account deletion
- **Process**:
  - Delete user from `auth.users` (cascade deletes user_profiles, predictions)
  - Delete user folder from Supabase Storage
  - Anonymize logs (replace user ID with "deleted_user")
- **Timeline**: Within 30 days of request

### 13.3.4 GDPR Compliance (if serving EU users)
- **Right to Access**: Users can download their data (CSV export)
- **Right to Rectification**: Users can update their profile
- **Right to Erasure**: Users can request account deletion
- **Right to Data Portability**: CSV export feature
- **Privacy Policy**: Link in footer, clearly explains data usage

---

## 13.4 Security Best Practices

### 13.4.1 Secure Coding
- **Secrets Management**:
  - Store sensitive data (API keys, DB passwords) in `.env` file
  - `.env` excluded from version control (in `.gitignore`)
  - Use `python-dotenv` to load secrets
- **Error Handling**:
  - Never expose stack traces to users
  - Log errors server-side for debugging
  - Show generic error messages to users

### 13.4.2 Dependency Management
- **Regular Updates**: Update Django, Supabase SDK, and all dependencies
- **Security Audits**: Run `pip audit` to check for vulnerabilities
- **Pin Versions**: Use `requirements.txt` with exact versions

### 13.4.3 File Upload Security
- **Virus Scanning**: (Optional) Integrate ClamAV to scan uploaded files
- **File Type Validation**: Check MIME type, not just extension
- **Storage Isolation**: Store user uploads in separate buckets/folders

---

## 13.5 Security Testing

### 13.5.1 Manual Testing
- **SQL Injection**: Try `' OR '1'='1` in login forms
- **XSS**: Try `<script>alert('XSS')</script>` in input fields
- **CSRF**: Try submitting forms without CSRF token
- **File Upload**: Try uploading .exe, .php files

### 13.5.2 Automated Testing
- **OWASP ZAP**: Automated security scan
- **Bandit**: Python static analysis for security issues
- **Safety**: Check dependencies for known vulnerabilities

---

**END OF PART 3**

---

**Next**: PART 4 will cover Sections 14-23:
- 14. Project Structure
- 15. Implementation Guide
- 16. Supabase Setup Guide
- 17. Django Configuration
- 18. Code Examples
- 19. Testing Requirements
- 20. Deployment Guide
- 21. Success Metrics
- 22. Future Enhancements
- 23. Appendix

Would you like me to continue with PART 4 now?
