# 📥 Dataset Download Guide

## Option 1: Manual Download (Easiest - Recommended)

### **Kaggle Crop Recommendation Dataset**

**Dataset Info:**
- Rows: 2,200
- Crops: 22 (rice, maize, wheat, chickpea, etc.)
- Features: N, P, K, temperature, humidity, ph, rainfall
- Size: ~150 KB

**Download Steps:**

1. **Go to Kaggle:**
   https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

2. **Download the dataset:**
   - Click "Download" button (you may need to create free Kaggle account)
   - You'll get `archive.zip` or `Crop_recommendation.csv`

3. **Place in project:**
   ```
   Crop_prediction/
   └── datasets/
       └── crop_data/
           └── Crop_recommendation.csv  ← Put here
   ```

4. **Create the directory if needed:**
   ```bash
   mkdir datasets\crop_data
   ```

---

## Option 2: Using Kaggle API (Advanced)

### **Install Kaggle CLI:**
```bash
pip install kaggle
```

### **Setup Kaggle API Key:**

1. Go to: https://www.kaggle.com/settings
2. Scroll to "API" section
3. Click "Create New API Token"
4. Download `kaggle.json`
5. Place it in: `C:\Users\<your-username>\.kaggle\kaggle.json`

### **Download Dataset:**
```bash
# Create directory
mkdir datasets\crop_data

# Download dataset
kaggle datasets download -d atharvaingle/crop-recommendation-dataset

# Unzip
unzip crop-recommendation-dataset.zip -d datasets/crop_data/
```

---

## Option 3: Use Sample Dataset (For Testing)

If you can't download from Kaggle, I'll generate a sample dataset with synthetic data.

**Run:**
```bash
python generate_sample_dataset.py
```

This creates `datasets/crop_data/crop_sample.csv` with 1,000 rows for testing.

---

## Dataset Format Required

Your CSV must have these columns:
```
N,P,K,temperature,humidity,ph,rainfall,label
```

**Example:**
```csv
N,P,K,temperature,humidity,ph,rainfall,label
90,42,43,20.87,82.00,6.50,202.93,rice
85,58,41,21.77,80.31,7.03,226.65,rice
60,55,44,23.00,82.32,7.84,263.96,rice
```

---

## ✅ After Download

Once you have the CSV file:
1. Place in: `datasets/crop_data/Crop_recommendation.csv`
2. Run: `python train_crop_model.py`
3. Wait 10-15 minutes for training
4. Your model will be ready!

---

**Next Step:** Download the dataset, then run the training script!
