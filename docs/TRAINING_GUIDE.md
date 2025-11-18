# 🌾 Complete Model Training Guide

## How to Train Your Own Crop Prediction Model

This guide will help you train a Deep Learning model from scratch for crop recommendation.

---

## 📋 Quick Start (3 Steps)

```bash
# Step 1: Generate sample dataset
python generate_sample_dataset.py

# Step 2: Train model (10-15 minutes)
python train_crop_model.py

# Step 3: Test model
python test_trained_model.py
```

That's it! Your model is ready to use.

---

## 📊 Option 1: Use Sample Dataset (Quickest)

### **Generate Synthetic Data:**

```bash
python generate_sample_dataset.py
```

**Output:**
- Location: `datasets/crop_data/crop_sample.csv`
- Samples: 2,200 (100 per crop)
- Crops: 22 crops

**Pros:** Instant, no download needed
**Cons:** Synthetic data, may not reflect real patterns

---

## 📥 Option 2: Use Real Dataset (Recommended)

### **Download from Kaggle:**

1. **Visit:** https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

2. **Download** `Crop_recommendation.csv`

3. **Place in:**
   ```
   Crop_prediction/
   └── datasets/
       └── crop_data/
           └── Crop_recommendation.csv
   ```

4. **Train:**
   ```bash
   python train_crop_model.py
   ```

**Pros:** Real agricultural data, better accuracy
**Cons:** Requires Kaggle account

---

## 🎯 Training Process

### **What Happens During Training:**

```
1. Load Dataset
   ├── Read CSV file
   ├── Validate columns
   └── Split: 80% train, 10% val, 10% test

2. Feature Engineering (7 → 15 features)
   ├── Original: N, P, K, temp, humidity, pH, rainfall
   ├── Ratios: NPK_sum, N_P_ratio, N_K_ratio, P_K_ratio
   ├── Interactions: temp_humidity, rainfall_humidity
   └── Categories: temp_category, rainfall_category

3. Build Neural Network
   ├── Input Layer: 15 features
   ├── Dense Layer 1: 256 neurons (ReLU + Dropout 0.3)
   ├── Dense Layer 2: 128 neurons (ReLU + Dropout 0.3)
   ├── Dense Layer 3: 64 neurons (ReLU + Dropout 0.2)
   └── Output Layer: num_crops neurons (Softmax)

4. Train Model
   ├── Optimizer: Adam (lr=0.001)
   ├── Loss: Categorical Crossentropy
   ├── Metrics: Accuracy, Top-3 Accuracy
   ├── Epochs: Up to 100 (with early stopping)
   └── Batch Size: 32

5. Evaluate on Test Set
   ├── Calculate accuracy
   ├── Calculate top-3 accuracy
   └── Generate classification report

6. Save Artifacts
   ├── best_crop_model.h5 (trained model)
   ├── scaler.pkl (feature scaler)
   ├── label_encoder.pkl (crop encoder)
   └── metadata.json (training info)
```

---

## 📈 Training Output Example

```
📂 Loading dataset...
   Path: datasets/crop_data/Crop_recommendation.csv
✅ Loaded 2200 samples
   Columns: ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
   Crops: 22
   Features shape: (2200, 7)

🔧 Engineering features (7 → 15)...
✅ Engineered features shape: (2200, 15)

📊 Preprocessing data...
   Classes: 22
   Crop names: ['apple', 'banana', 'blackgram', 'chickpea', 'coconut']...
   Train samples: 1760 (80.0%)
   Val samples: 220 (10.0%)
   Test samples: 220 (10.0%)

🏗️  Building model architecture...
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 dense (Dense)               (None, 256)               4096
 dropout (Dropout)           (None, 256)               0
 dense_1 (Dense)             (None, 128)               32896
 dropout_1 (Dropout)         (None, 128)               0
 dense_2 (Dense)             (None, 64)                8256
 dropout_2 (Dropout)         (None, 64)                0
 dense_3 (Dense)             (None, 22)                1430
=================================================================
Total params: 46,678
Trainable params: 46,678
Non-trainable params: 0

🎯 Training model...
Epoch 1/100
55/55 [==============================] - 2s 15ms/step - loss: 2.8234 - accuracy: 0.1648 - top_3_accuracy: 0.3966 - val_loss: 2.4821 - val_accuracy: 0.2727 - val_top_3_accuracy: 0.5636
Epoch 2/100
55/55 [==============================] - 0s 5ms/step - loss: 2.3156 - accuracy: 0.2818 - top_3_accuracy: 0.5727 - val_loss: 2.0342 - val_accuracy: 0.3682 - val_top_3_accuracy: 0.7091
...
Epoch 45/100
55/55 [==============================] - 0s 5ms/step - loss: 0.3421 - accuracy: 0.8966 - top_3_accuracy: 0.9898 - val_loss: 0.8123 - val_accuracy: 0.7636 - val_top_3_accuracy: 0.9455

📈 Evaluating model on test set...
   Test Accuracy: 68.18%
   Top-3 Accuracy: 93.18%

💾 Saving model artifacts...
   ✅ Saved: ml_models/best_crop_model.h5
   ✅ Saved: ml_models/scaler.pkl
   ✅ Saved: ml_models/label_encoder.pkl
   ✅ Saved: ml_models/metadata.json

✅ TRAINING COMPLETED SUCCESSFULLY!

📊 Final Results:
   Test Accuracy: 68.18%
   Top-3 Accuracy: 93.18%
   Crops: 22
```

---

## 🧪 Testing Your Model

### **Run test script:**

```bash
python test_trained_model.py
```

**Output:**

```
🧪 TESTING TRAINED CROP PREDICTION MODEL

📦 Loading model...
✅ Model loaded successfully
   Total crops: 22

🧪 Running 8 test cases...

======================================================================
🌾 Test Case: Sugarcane
======================================================================

📊 Input Parameters:
   N=120, P=60, K=80
   Temp=28°C, Humidity=75%
   pH=6.8, Rainfall=2000mm

🎯 Prediction Results:
   Predicted Crop: Sugarcane
   Confidence: 98.5%

🏆 Top-3 Recommendations:
   1. Sugarcane       ██████████████████████████████████████████████████ 98.5%
   2. Coffee          ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  1.2%
   3. Rice            ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  0.2%

✅ CORRECT! Predicted 'Sugarcane' (expected 'Sugarcane')

...

📊 TEST SUMMARY
   Total tests: 8
   Exact matches: 6/8 (75.0%)
   Top-3 matches: 8/8 (100.0%)

✅ Good! All expected crops in Top-3
```

---

## 🎓 Understanding the Model

### **Input Features (7):**

| Feature | Description | Example Range |
|---------|-------------|---------------|
| N | Nitrogen content | 0-140 kg/ha |
| P | Phosphorus content | 5-145 kg/ha |
| K | Potassium content | 5-205 kg/ha |
| temperature | Average temperature | 8-45°C |
| humidity | Relative humidity | 14-100% |
| ph | Soil pH value | 3.5-9.9 |
| rainfall | Annual rainfall | 20-300 mm |

### **Engineered Features (+8):**

1. **NPK_sum**: Total nutrients (N+P+K)
2. **N_P_ratio**: Nitrogen to Phosphorus ratio
3. **N_K_ratio**: Nitrogen to Potassium ratio
4. **P_K_ratio**: Phosphorus to Potassium ratio
5. **temp_humidity**: Temperature-humidity interaction
6. **rainfall_humidity**: Rainfall-humidity interaction
7. **temp_category**: Temperature category (0-3)
8. **rainfall_category**: Rainfall category (0-3)

### **Model Architecture:**

```
15 features → 256 neurons → 128 neurons → 64 neurons → 22 crops
```

- **Total Parameters:** ~47,000
- **Activation:** ReLU (hidden), Softmax (output)
- **Regularization:** Dropout (30%, 30%, 20%)

---

## 📦 Output Files

After training, you'll find these files:

```
ml_models/
├── best_crop_model.h5       # Trained neural network (~2 MB)
├── scaler.pkl                # Feature scaler (~10 KB)
├── label_encoder.pkl         # Crop name encoder (~5 KB)
└── metadata.json             # Training metadata (~2 KB)
```

**These files are automatically used by Django!**

---

## 🔧 Customization

### **Train with More Crops:**

Expand your dataset to include more crops (50, 101, etc.)

### **Adjust Model Architecture:**

Edit `train_crop_model.py`:

```python
model = Sequential([
    Dense(512, activation='relu'),  # Increase neurons
    Dropout(0.3),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(num_classes, activation='softmax')
])
```

### **Tune Hyperparameters:**

```python
# Learning rate
optimizer=keras.optimizers.Adam(learning_rate=0.0005)  # Lower = slower but more precise

# Batch size
epochs=100,
batch_size=64,  # Larger = faster but less precise
```

---

## ❓ FAQ

### **Q: How long does training take?**
A: 10-15 minutes on CPU for 2,200 samples

### **Q: Can I use my own dataset?**
A: Yes! Just ensure it has the required columns: N, P, K, temperature, humidity, ph, rainfall, label

### **Q: What accuracy should I expect?**
A: 60-70% exact match, 85-95% top-3 match (depends on dataset quality)

### **Q: Can I train with GPU?**
A: Yes! TensorFlow will automatically use GPU if available (training will be 10x faster)

### **Q: How do I retrain the model?**
A: Just run `python train_crop_model.py` again

---

## 🚀 Next Steps

1. ✅ **Train your model**
2. ✅ **Test it**: `python test_trained_model.py`
3. ✅ **Run Django**: `python manage.py runserver`
4. ✅ **Make predictions**: http://127.0.0.1:8000/predictions/crop/

---

## 📚 Additional Resources

- **TensorFlow Docs**: https://www.tensorflow.org/
- **Scikit-learn Preprocessing**: https://scikit-learn.org/stable/modules/preprocessing.html
- **Kaggle Datasets**: https://www.kaggle.com/datasets

---

**Happy Training! 🌾**
