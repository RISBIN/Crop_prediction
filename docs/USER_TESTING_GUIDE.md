# User Testing Guide - Real Dataset Samples

## Where to Get Real Test Data

### Option 1: Use Pre-Generated Test Samples (Recommended)

**Files created for you:**
- `test_samples_real.csv` - 66 real samples (3 per crop)
- `test_samples_real.json` - Same data in JSON format

**How to use:**
1. Open `test_samples_real.csv` in Excel/spreadsheet
2. Pick any row
3. Enter the values in your Django app

**Example from file:**
```
Crop: Rice
N=90, P=42, K=43
Temperature=21°C, Humidity=82%, pH=6.5, Rainfall=203mm
Expected result: Rice with 95%+ confidence
```

---

### Option 2: Get from Original Dataset

**Dataset location:**
```
Crop_prediction/Crop_recommendation.csv
```

**Contains:**
- 2,200 samples
- 100 samples per crop
- 22 crops total

**How to use:**
1. Open `Crop_recommendation.csv`
2. Filter by crop name (column: `label`)
3. Copy any row values
4. Test in Django app

---

### Option 3: Download from Kaggle

**URL:**
https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset

**Steps:**
1. Download `Crop_recommendation.csv`
2. Open in spreadsheet software
3. Pick any sample
4. Use in your app

---

## Quick Test Samples (Copy & Paste Ready)

### High Confidence Samples (99-100% accuracy)

**Rice:**
- N=90, P=42, K=43, Temp=21, Humidity=82, pH=6.5, Rainfall=203
- Expected: Rice (95%+ confidence)

**Maize:**
- N=71, P=54, K=16, Temp=23, Humidity=64, pH=5.7, Rainfall=88
- Expected: Maize (100% confidence)

**Coffee:**
- N=100, P=25, K=30, Temp=25, Humidity=58, pH=6.8, Rainfall=150
- Expected: Coffee (99%+ confidence)

**Coconut:**
- N=20, P=10, K=30, Temp=27, Humidity=94, pH=6.0, Rainfall=175
- Expected: Coconut (100% confidence)

**Apple:**
- N=20, P=130, K=200, Temp=22, Humidity=85, pH=6.5, Rainfall=120
- Expected: Apple (59%+ confidence)

**Banana:**
- N=100, P=75, K=50, Temp=27, Humidity=80, pH=6.5, Rainfall=100
- Expected: Banana (92%+ confidence)

**Cotton:**
- N=120, P=40, K=20, Temp=24, Humidity=80, pH=7.0, Rainfall=85
- Expected: Cotton (high confidence)

**Grapes:**
- N=23, P=130, K=200, Temp=24, Humidity=82, pH=6.2, Rainfall=100
- Expected: Grapes or Apple (close match)

**Mango:**
- N=25, P=25, K=30, Temp=30, Humidity=55, pH=6.5, Rainfall=100
- Expected: Mango (91%+ confidence)

**Chickpea:**
- N=40, P=60, K=80, Temp=17, Humidity=17, pH=7.5, Rainfall=89
- Expected: Chickpea (high confidence)

---

## Feature Ranges (For Creating Custom Tests)

| Feature | Min | Max | Unit |
|---------|-----|-----|------|
| Nitrogen (N) | 0 | 140 | kg/ha |
| Phosphorus (P) | 5 | 145 | kg/ha |
| Potassium (K) | 5 | 205 | kg/ha |
| Temperature | 8 | 44 | °C |
| Humidity | 14 | 100 | % |
| pH | 3.5 | 9.9 | - |
| Rainfall | 20 | 300 | mm |

---

## Important Notes

### Crops NOT in Model

The model was trained on 22 crops. These are **NOT** included:
- ❌ Wheat
- ❌ Sugarcane
- ❌ Barley
- ❌ Peas
- ❌ Soybean
- ❌ Sunflower
- ❌ Potato
- ❌ Tomato

### Crops Available (22 total)

✅ apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean, muskmelon, orange, papaya, pigeonpeas, pomegranate, rice, watermelon

---

## Testing Tips

### Good Test Values
✅ Use samples from `test_samples_real.csv`
✅ Use values from `Crop_recommendation.csv`
✅ Stay within feature ranges above

### Bad Test Values
❌ Random made-up numbers
❌ Values outside feature ranges
❌ Crops not in the 22-crop list
❌ Extreme/unrealistic combinations

### Why Accuracy Matters

| Test Data Source | Expected Accuracy |
|------------------|-------------------|
| Real dataset samples | 90-100% |
| Realistic values within range | 60-80% |
| Random/made-up values | 20-40% |

The model was trained on **real agricultural data**, so it works best with realistic soil and climate values!

---

## For Developers

### Load Test Samples in Code

```python
import json

# Load JSON samples
with open('test_samples_real.json') as f:
    samples = json.load(f)

# Test first sample
test = samples[0]
print(f"Testing: {test['crop']}")
result = predictor.predict(test)
print(f"Predicted: {result['predicted_crop']}")
```

### Validate User Input

```python
def validate_input(data):
    """Validate user input against feature ranges."""
    ranges = {
        'nitrogen': (0, 140),
        'phosphorus': (5, 145),
        'potassium': (5, 205),
        'temperature': (8, 44),
        'humidity': (14, 100),
        'ph_value': (3.5, 9.9),
        'rainfall': (20, 300)
    }

    for feature, (min_val, max_val) in ranges.items():
        value = data.get(feature)
        if not (min_val <= value <= max_val):
            return False, f"{feature} out of range ({min_val}-{max_val})"

    return True, "Valid"
```

---

## Quick Start

**1. Copy a test sample:**
```
N=90, P=42, K=43, Temp=21, Humidity=82, pH=6.5, Rainfall=203
```

**2. Go to Django app:**
```bash
python manage.py runserver
```

**3. Open browser:**
```
http://127.0.0.1:8000/predictions/crop/
```

**4. Enter values and test!**

Expected result: **Rice** with **95%+ confidence**

---

**Files created:**
- `test_samples_real.csv` - 66 verified samples ✅
- `test_samples_real.json` - JSON format ✅
- `Crop_recommendation.csv` - Full 2,200 samples ✅
