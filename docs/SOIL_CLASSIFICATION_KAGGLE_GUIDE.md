# Soil Classification Training on Kaggle Guide

This guide walks you through training the soil classification model on Kaggle using free GPU resources.

## Prerequisites

- Kaggle account (free)
- Basic understanding of Jupyter notebooks
- The notebook file: `notebooks/soil_classification_kaggle.ipynb`

## Dataset Information

**Dataset:** [SOIL TYPES DATASET](https://www.kaggle.com/datasets/jhislainematchouath/soil-types-dataset)
- **Creator:** Jhislaine Matchouathé
- **Total Images:** 1,555
- **Classes:** 4 (Black, clay, Alluvial, Red)
- **Distribution:** ~389 images per class (balanced)
- **Format:** JPG images
- **Size:** 207 MB
- **Structure:** Train/Test split included

**Class Mapping:**
```
Dataset Label → Application Label
Black         → black (Black Soil)
clay          → clay (Clay Soil)
Alluvial      → loamy (Loamy Soil)
Red           → sandy (Sandy Soil)
```

## Step-by-Step Training Process

### Step 1: Upload Notebook to Kaggle

1. Go to [Kaggle Notebooks](https://www.kaggle.com/code)
2. Click **"New Notebook"**
3. Click **"File"** → **"Upload Notebook"**
4. Select `notebooks/soil_classification_kaggle.ipynb`
5. Wait for upload to complete

### Step 2: Add Dataset

1. In the right sidebar, click **"+ Add data"**
2. Search for **"jhislainematchouath soil types"**
3. Select **"SOIL TYPES DATASET"** by Jhislaine Matchouathé
4. Click **"Add"** button

**Verify Dataset Path:**
The dataset should be available at: `/kaggle/input/soil-types-dataset/`

Expected structure:
```
/kaggle/input/soil-types-dataset/
├── Train/
│   ├── Black/       (~300+ images)
│   ├── clay/        (~300+ images)
│   ├── Alluvial/    (~300+ images)
│   └── Red/         (~300+ images)
└── Test/
    ├── Black/       (~80+ images)
    ├── clay/        (~80+ images)
    ├── Alluvial/    (~80+ images)
    └── Red/         (~80+ images)
```

### Step 3: Enable GPU Accelerator

1. Click **"Settings"** (right sidebar)
2. Under **"Accelerator"**, select **"GPU T4 x2"** (or available GPU)
3. Click **"Save"**

**Important:** GPU quota is limited per week. Use wisely!

### Step 4: Configure Training Parameters

The notebook has default settings optimized for the dataset:

```python
IMG_SIZE = 224        # ResNet18 input size
BATCH_SIZE = 32       # Fits in GPU memory
EPOCHS = 25           # ~15-20 minutes training
LEARNING_RATE = 0.001 # Adam optimizer
NUM_CLASSES = 4       # black, clay, loamy, sandy
```

**Optional Adjustments:**
- **Faster training:** Reduce `EPOCHS` to 15-20
- **Better accuracy:** Increase `EPOCHS` to 30-35
- **Memory issues:** Reduce `BATCH_SIZE` to 16

### Step 5: Run Training

1. Click **"Run All"** button (or Ctrl+Enter on each cell)
2. Monitor the output:
   - Dataset loading: ~1-2 minutes
   - Training: ~15-20 minutes (25 epochs with GPU)
   - Evaluation: ~1 minute

**Expected Output:**
```
Dataset loaded successfully!
Total images: 1555
Training samples: 1166 (75%)
Validation samples: 389 (25%)

Class distribution:
  black: 389 images
  clay: 389 images
  loamy: 389 images
  sandy: 388 images

Training on device: cuda
Model: ResNet18 (Transfer Learning)

Epoch 1/25
----------
Train Loss: 1.2345, Train Acc: 0.5234
Val Loss: 0.9876, Val Acc: 0.6543

...

Epoch 25/25
----------
Train Loss: 0.1234, Train Acc: 0.9567
Val Loss: 0.2345, Val Acc: 0.9123

Training completed in 18m 32s
Best validation accuracy: 91.23%
```

### Step 6: Evaluate Results

The notebook will display:

1. **Training/Validation Loss Curves**
   - Should see decreasing loss over epochs
   - Validation loss should track training loss

2. **Training/Validation Accuracy Curves**
   - Should see increasing accuracy
   - Target: 85%+ validation accuracy

3. **Confusion Matrix**
   - Shows per-class performance
   - Diagonal should be bright (correct predictions)

4. **Classification Report**
   ```
                precision    recall  f1-score   support
       black       0.92      0.89      0.90        97
        clay       0.88      0.91      0.89        97
       loamy       0.93      0.91      0.92        97
       sandy       0.90      0.92      0.91        98
   ```

5. **Sample Predictions**
   - Visual grid showing predictions vs actual labels

### Step 7: Download Trained Model

After successful training, the notebook saves:

**Model Files:**
- `soil_classifier_resnet18.pth` - PyTorch model weights
- `soil_metadata.json` - Model configuration

**Download Steps:**
1. Look for output cell showing saved files
2. Click **"Output"** tab (right sidebar)
3. Download both files:
   - `soil_classifier_resnet18.pth`
   - `soil_metadata.json`

**Local Storage:**
```
Crop_prediction/
└── ml_models/
    └── soil_classifier/
        └── v1.0/
            ├── model.pth              ← soil_classifier_resnet18.pth
            └── metadata.json          ← soil_metadata.json
```

### Step 8: Integrate with Django

1. **Create model directory:**
   ```bash
   mkdir -p ml_models/soil_classifier/v1.0
   ```

2. **Copy downloaded files:**
   ```bash
   # Rename and copy model
   cp ~/Downloads/soil_classifier_resnet18.pth ml_models/soil_classifier/v1.0/model.pth
   cp ~/Downloads/soil_metadata.json ml_models/soil_classifier/v1.0/metadata.json
   ```

3. **Update soil_classifier.py:**

   The file `apps/predictions/ml_services/soil_classifier.py` needs to be updated to load the real PyTorch model instead of returning mock predictions.

4. **Test the integration:**
   ```bash
   python manage.py shell
   ```

   ```python
   from apps.predictions.ml_services.soil_classifier import get_soil_classifier

   classifier = get_soil_classifier()
   print(f"Model loaded: {classifier.is_trained}")

   # Test with sample image (once integrated)
   # result = classifier.predict(image_path)
   # print(result)
   ```

## Expected Performance

**Target Metrics:**
- Validation Accuracy: **85-92%**
- Per-class Accuracy: **80%+** for each soil type
- Training Time: **15-20 minutes** (25 epochs with GPU)

**Good Signs:**
- ✅ Validation accuracy > 85%
- ✅ Low gap between training and validation accuracy (<5%)
- ✅ Confusion matrix shows strong diagonal
- ✅ All classes have precision/recall > 0.80

**Warning Signs:**
- ⚠️ Validation accuracy < 75% (may need more epochs)
- ⚠️ Large gap between train/val accuracy (>10% = overfitting)
- ⚠️ One class performs poorly (check dataset balance)

## Troubleshooting

### Issue: GPU Not Available

**Error:** `Training on device: cpu`

**Solution:**
1. Check **Settings** → **Accelerator** → Select GPU
2. Save and rerun the notebook
3. Verify with: `torch.cuda.is_available()` should return `True`

### Issue: Dataset Not Found

**Error:** `FileNotFoundError: /kaggle/input/soil-types/`

**Solution:**
1. Check right sidebar → **Data** section
2. Dataset should show "SOIL TYPES DATASET"
3. If missing, click **"+ Add data"** and search "soil types"

### Issue: Out of Memory

**Error:** `CUDA out of memory`

**Solution:**
1. Reduce `BATCH_SIZE` from 32 to 16
2. Restart kernel: **Run** → **Restart Session**
3. Rerun training

### Issue: Low Accuracy (<75%)

**Possible Causes:**
1. **Not enough epochs:** Increase to 30-35
2. **Learning rate too high:** Try 0.0005
3. **Need more data augmentation:** Already included in notebook

### Issue: Model Not Saving

**Solution:**
1. Check notebook output for save confirmation
2. Look in **Output** tab (right sidebar)
3. Manually save with: `torch.save(model.state_dict(), 'model.pth')`

## Training Tips

### Optimize for Speed

```python
BATCH_SIZE = 32      # Maximum for T4 GPU
EPOCHS = 15-20       # Faster training
```

Training time: ~12-15 minutes

### Optimize for Accuracy

```python
BATCH_SIZE = 16      # More stable training
EPOCHS = 30-35       # Better convergence
LEARNING_RATE = 0.0005  # Fine-tuning
```

Training time: ~25-30 minutes

### Data Augmentation

Already included in the notebook:
- Random horizontal/vertical flips
- Random rotation (±20 degrees)
- Color jitter (brightness, contrast, saturation)

These prevent overfitting and improve generalization.

## Model Architecture

**Base Model:** ResNet18 (pretrained on ImageNet)

**Transfer Learning Strategy:**
1. Load pretrained ResNet18
2. Freeze early convolutional layers (feature extraction)
3. Replace final fully connected layer
4. Train only the new layers

**Custom Classifier:**
```
ResNet18 Features (512)
    ↓
Linear(512 → 512) + ReLU + Dropout(0.5)
    ↓
Linear(512 → 256) + ReLU + Dropout(0.3)
    ↓
Linear(256 → 4)  [black, clay, loamy, sandy]
```

**Why ResNet18?**
- ✅ Lightweight (11M parameters)
- ✅ Fast training (~15 mins)
- ✅ Excellent for image classification
- ✅ Pretrained on ImageNet (transfer learning)

## Next Steps After Training

1. **Download model files** (model.pth, metadata.json)
2. **Copy to project:** `ml_models/soil_classifier/v1.0/`
3. **Update Django integration** (soil_classifier.py)
4. **Test predictions** with sample soil images
5. **Deploy to production** if accuracy is satisfactory

## Additional Resources

**Dataset:**
- [SOIL TYPES DATASET on Kaggle](https://www.kaggle.com/datasets/posthumus/soil-types)

**PyTorch Tutorials:**
- [Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [ResNet Documentation](https://pytorch.org/vision/stable/models.html#resnet)

**Kaggle GPU:**
- Free GPU quota: 30 hours/week
- T4 GPU: 16GB memory
- Check usage: [Kaggle Settings](https://www.kaggle.com/settings)

## Support

**Common Questions:**

**Q: How long does training take?**
A: ~15-20 minutes with GPU (25 epochs), ~2-3 hours with CPU

**Q: What accuracy should I expect?**
A: 85-92% validation accuracy with default settings

**Q: Can I train with more epochs?**
A: Yes! Try 30-35 epochs for potentially better accuracy

**Q: Do I need to download the dataset?**
A: No, Kaggle provides the dataset in the cloud

**Q: How much GPU quota does this use?**
A: ~0.3-0.5 hours out of 30 hours/week free quota

---

**Ready to train?** Upload the notebook and follow the steps above! 🚀
