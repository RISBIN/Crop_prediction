# 📓 Kaggle Notebook Training Guide

## How to Train Your Model on Kaggle

Complete step-by-step guide to train your crop prediction model on Kaggle's free GPU/TPU.

---

## 🚀 Quick Start (5 Steps)

### **Step 1: Upload Notebook to Kaggle**

1. **Go to Kaggle**: https://www.kaggle.com/
2. **Sign in** (or create free account)
3. **Click "Code"** → **"New Notebook"**
4. **Upload notebook**:
   - Click on file icon (📁)
   - Upload: `crop_prediction_random_forest_kaggle.ipynb`

**IMPORTANT:** Use the Random Forest notebook, NOT the Deep Learning version!

---

### **Step 2: Add Dataset**

1. **In Kaggle notebook**, click **"+ Add Data"** (right sidebar)
2. **Search**: "crop recommendation"
3. **Select**: "Crop Recommendation Dataset" by Atharva Ingle
4. **Click "Add"**

The dataset path will automatically be: `/kaggle/input/crop-recommendation-dataset/Crop_recommendation.csv`

---

### **Step 3: Enable GPU (Optional but Faster)**

1. **Click "Settings"** (⚙️ icon on right)
2. **Accelerator**: Select "GPU T4 x2" (free!)
3. **Click "Save"**

**Training time:**
- CPU: ~15 minutes
- GPU: ~3-5 minutes

---

### **Step 4: Run Notebook**

**Option A - Run All:**
- Click **"Run All"** button at top

**Option B - Run Cell by Cell:**
- Press `Shift + Enter` on each cell
- Watch the outputs and visualizations

---

### **Step 5: Download Trained Model**

After training completes:

1. **Look for files in output:**
   - `best_crop_model.h5`
   - `scaler.pkl`
   - `label_encoder.pkl`
   - `metadata.json`

2. **Download files:**
   - Click on file → "Download"
   - **OR** use the code cell below (add to notebook):

```python
# Download all files as ZIP
from IPython.display import FileLink
import shutil

# Create ZIP
shutil.make_archive('crop_model_files', 'zip', '.',
                    arcname='.',
                    root_dir=None)

print("✅ Files packaged!")
FileLink('crop_model_files.zip')
```

3. **Place in Django project:**
   ```
   Crop_prediction/
   └── ml_models/
       ├── best_crop_model.h5
       ├── scaler.pkl
       ├── label_encoder.pkl
       └── metadata.json
   ```

---

## 📊 What the Notebook Does

### **Complete Training Pipeline:**

```
1. Load Dataset (2,200 samples, 22 crops)
   ↓
2. Exploratory Data Analysis (EDA)
   - Crop distribution
   - Feature distributions
   - Correlation heatmap
   ↓
3. Feature Engineering (7 → 15 features)
   - NPK ratios
   - Temperature-humidity interactions
   - Categorical encoding
   ↓
4. Build Neural Network
   - 15 → 256 → 128 → 64 → 22
   - Dropout regularization
   - Adam optimizer
   ↓
5. Train Model
   - 100 epochs (with early stopping)
   - Batch size: 32
   - Learning rate: 0.001
   ↓
6. Evaluate Model
   - Test accuracy: ~65-70%
   - Top-3 accuracy: ~90-95%
   ↓
7. Save Artifacts
   - Model weights (.h5)
   - Preprocessors (.pkl)
   - Metadata (.json)
```

---

## 📈 Expected Results

### **Training Output:**

```
Epoch 1/100
loss: 2.8234 - accuracy: 0.1648 - val_accuracy: 0.2727

Epoch 45/100
loss: 0.3421 - accuracy: 0.8966 - val_accuracy: 0.7636

✅ TRAINING COMPLETED!

📊 Final Results:
   Test Accuracy: 68.18%
   Top-3 Accuracy: 93.18%
   Total Crops: 22
```

### **Visualizations:**

The notebook generates:
- ✅ Crop distribution bar chart
- ✅ Feature histograms (7 features)
- ✅ Correlation heatmap
- ✅ Training/validation curves (accuracy, loss)
- ✅ Confusion matrix
- ✅ Sample predictions

---

## 🎯 Notebook Sections

| Section | Description | Time |
|---------|-------------|------|
| 1. Import Libraries | Load dependencies | 1 min |
| 2. Load Dataset | Read CSV from Kaggle | 1 min |
| 3. EDA | Visualize data | 2 min |
| 4. Feature Engineering | Create 15 features | 1 min |
| 5. Prepare Data | Split, scale, encode | 1 min |
| 6. Build Model | Neural network architecture | 1 min |
| 7. Train Model | **Main training loop** | **10-15 min (CPU)** |
| 8. Visualizations | Plot training curves | 1 min |
| 9. Evaluate | Test set evaluation | 1 min |
| 10. Sample Tests | Test predictions | 1 min |
| 11. Save Artifacts | Export model files | 1 min |
| 12. Summary | Final results | 1 min |

**Total Time: ~20-25 minutes (CPU) or ~8-12 minutes (GPU)**

---

## 🔧 Customization

### **Change Model Architecture:**

Find this cell in the notebook:

```python
def build_model(input_dim, num_classes):
    model = Sequential([
        Dense(512, activation='relu'),  # ← Change neurons
        Dropout(0.4),                   # ← Change dropout
        # ...
    ])
```

### **Adjust Training:**

```python
history = model.fit(
    X_train_scaled, y_train_cat,
    epochs=150,      # ← More epochs
    batch_size=64,   # ← Larger batch
    # ...
)
```

### **Change Learning Rate:**

```python
optimizer=keras.optimizers.Adam(learning_rate=0.0005)  # ← Lower LR
```

---

## 📥 Alternative: Download Dataset Manually

If you prefer to run locally:

1. **Download from Kaggle:**
   https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

2. **Modify notebook path:**
   ```python
   # Change this line:
   df = pd.read_csv('/kaggle/input/crop-recommendation-dataset/Crop_recommendation.csv')

   # To this:
   df = pd.read_csv('datasets/crop_data/Crop_recommendation.csv')
   ```

3. **Run locally:**
   ```bash
   jupyter notebook crop_prediction_training_kaggle.ipynb
   ```

---

## 🎓 Understanding the Code

### **Feature Engineering Example:**

```python
# Original 7 features
N, P, K, temperature, humidity, ph, rainfall

# Engineered features (+8)
NPK_sum = N + P + K                    # Total nutrients
N_P_ratio = N / (P + 0.01)            # N:P ratio
temp_humidity = temp * humidity / 100  # Interaction
temp_category = [0,1,2,3]             # Categories
# ... and more
```

### **Model Architecture:**

```
Input (15 features)
    ↓
Dense(256, ReLU) + Dropout(0.3)
    ↓
Dense(128, ReLU) + Dropout(0.3)
    ↓
Dense(64, ReLU) + Dropout(0.2)
    ↓
Dense(22, Softmax)
    ↓
Output (22 crop probabilities)
```

---

## ✅ Validation

### **Check if Training Worked:**

Look for these in the output:

```python
✅ Test Accuracy: 65-75%
✅ Top-3 Accuracy: 90-95%
✅ Saved: best_crop_model.h5
✅ Saved: scaler.pkl
✅ Saved: label_encoder.pkl
✅ Saved: metadata.json
```

### **Test Predictions:**

The notebook tests with:
- Sugarcane (should be 95-100% confidence)
- Wheat (should be in Top-3)
- Rice (should be high confidence)

---

## 🐛 Troubleshooting

### **Error: "File not found"**
→ Make sure you added the dataset in Step 2

### **Error: "CUDA out of memory"**
→ Reduce batch size to 16 or use CPU

### **Low accuracy (<50%) or predicting same crop repeatedly**
→ **CRITICAL:** If you modified the notebook, you MUST restart kernel and retrain!
→ Click "Restart & Run All" to clear old model from memory
→ Old model trained with different features = wrong predictions

### **Still getting 37.5% accuracy after changes**
→ This means you didn't restart the kernel after making changes
→ The old model (15 features) is still in memory
→ New prediction function (7 features) → **Feature mismatch!**
→ **Solution:** Runtime → Restart & Run All

### **Can't download files**
→ Use the ZIP download code snippet above

---

## 🎯 After Training

### **1. Integrate with Django:**

```bash
# Place model files in Django project
cp best_crop_model.h5 Crop_prediction/ml_models/
cp scaler.pkl Crop_prediction/ml_models/
cp label_encoder.pkl Crop_prediction/ml_models/
cp metadata.json Crop_prediction/ml_models/
```

### **2. Test in Django:**

```bash
cd Crop_prediction
python manage.py runserver
# Go to: http://127.0.0.1:8000/predictions/crop/
```

### **3. Test with Script:**

```bash
python test_trained_model.py
```

---

## 📚 Resources

- **Kaggle Notebook Tutorial**: https://www.kaggle.com/docs/notebooks
- **TensorFlow Docs**: https://www.tensorflow.org/
- **Dataset Source**: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

---

## 🎉 Success Checklist

- [ ] Created Kaggle account
- [ ] Uploaded notebook
- [ ] Added dataset
- [ ] Enabled GPU (optional)
- [ ] Ran all cells
- [ ] Got 65%+ accuracy
- [ ] Downloaded model files
- [ ] Placed in Django `ml_models/`
- [ ] Tested predictions
- [ ] Integrated with Django app

---

**Happy Training on Kaggle! 🚀**

**Pro Tip:** Save your Kaggle notebook as a version after each successful run. This way you can always go back to a working version!
