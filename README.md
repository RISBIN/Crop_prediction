# 🌾 Crop Prediction System

AI-powered agricultural decision support system for crop recommendations using machine learning.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

This Django-based web application uses a **Random Forest machine learning model** to recommend the most suitable crops based on soil and climate parameters. The model achieves **99% accuracy** on the test set with **100% Top-3 accuracy**.

### Features

- 🎯 **Smart Crop Recommendations** - Predicts best crops with confidence scores
- 📊 **Top-3 Suggestions** - Shows top 3 crop recommendations for each query
- 🌐 **Web Interface** - User-friendly Django-based web application
- 🔬 **22 Crop Support** - Trained on real agricultural data
- ☁️ **Cloud Integration** - Supabase PostgreSQL and Storage support
- 📱 **Responsive Design** - Bootstrap 5 UI with mobile support

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Virtual environment (recommended)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/crop-prediction.git
cd Crop_prediction

# Create virtual environment
python -m venv crp-venv

# Activate virtual environment
# Windows:
crp-venv\Scripts\activate
# Linux/Mac:
source crp-venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

## 🧪 Testing the Model

### Use Real Test Data

We provide verified test samples for accurate predictions:

```python
# Example test values (Rice - 95% confidence)
N=90, P=42, K=43
Temperature=21°C, Humidity=82%, pH=6.5, Rainfall=203mm
```

**Test Data Location:**
- `datasets/test_samples/test_samples_real.csv` - 66 verified samples
- `datasets/test_samples/test_samples_real.json` - JSON format

**Run Tests:**
```bash
# Test Django predictor
python scripts/testing/test_django_predictor.py

# Test with user samples
python scripts/testing/test_user_samples.py
```

See [USER_TESTING_GUIDE.md](docs/USER_TESTING_GUIDE.md) for more examples.

## 🎓 Model Training

### Option 1: Use Pre-trained Model (Recommended)

The repository includes a trained Random Forest model in `crop-prediction-models/`:
- `random_forest_model.pkl` - Trained model (99% accuracy)
- `scaler.pkl` - Feature scaler
- `label_encoder.pkl` - Crop encoder
- `metadata.json` - Model info

### Option 2: Train Your Own Model

**On Kaggle (Free GPU):**

1. Upload notebook: `notebooks/crop_prediction_random_forest_kaggle.ipynb`
2. Add dataset: [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
3. Click "Restart & Run All"
4. Download trained models

**Locally:**

```bash
# Generate sample dataset (optional)
python scripts/training/generate_sample_dataset.py

# Train model
python scripts/training/train_crop_model.py

# Test model
python scripts/testing/test_trained_model.py
```

See [TRAINING_GUIDE.md](docs/TRAINING_GUIDE.md) for detailed instructions.

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Test Accuracy | 99.09% |
| Top-3 Accuracy | 100% |
| Training Samples | 2,200 |
| Crops Supported | 22 |

**Supported Crops:**
apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean, muskmelon, orange, papaya, pigeonpeas, pomegranate, rice, watermelon

## 🏗️ Project Structure

```
Crop_prediction/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management
│
├── docs/                        # Documentation
│   ├── TRAINING_GUIDE.md
│   ├── KAGGLE_NOTEBOOK_GUIDE.md
│   ├── DATASET_DOWNLOAD_GUIDE.md
│   └── USER_TESTING_GUIDE.md
│
├── scripts/                     # Utility scripts
│   ├── training/                # Model training
│   │   ├── train_crop_model.py
│   │   ├── generate_sample_dataset.py
│   │   └── extract_test_samples.py
│   └── testing/                 # Testing scripts
│       ├── test_django_predictor.py
│       ├── test_user_samples.py
│       └── test_trained_model.py
│
├── notebooks/                   # Jupyter notebooks
│   ├── crop_prediction_random_forest_kaggle.ipynb
│   └── crop_prediction_training_kaggle.ipynb
│
├── datasets/                    # Data files
│   ├── crop_data/
│   │   └── Crop_recommendation.csv
│   └── test_samples/
│       ├── test_samples_real.csv
│       └── test_samples_real.json
│
├── crop-prediction-models/      # Trained models
│   ├── random_forest_model.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── metadata.json
│
├── apps/                        # Django apps
│   ├── core/                    # Landing pages
│   ├── accounts/                # User management
│   ├── predictions/             # ML predictions
│   └── admin_panel/             # Admin features
│
├── config/                      # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── supabase_storage.py
│
├── static/                      # Static files
├── media/                       # Uploaded files
└── logs/                        # Application logs
```

## 🔧 Configuration

### Environment Variables

Create `.env` file (use `.env.example` as template):

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase (Optional)
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
```

### Database

- **Development:** SQLite (default)
- **Production:** Supabase PostgreSQL

## 📚 Documentation

- [Training Guide](docs/TRAINING_GUIDE.md) - How to train models
- [Kaggle Notebook Guide](docs/KAGGLE_NOTEBOOK_GUIDE.md) - Train on Kaggle
- [Dataset Download Guide](docs/DATASET_DOWNLOAD_GUIDE.md) - Get training data
- [User Testing Guide](docs/USER_TESTING_GUIDE.md) - Test with real samples
- [Claude Code Guide](CLAUDE.md) - For AI assistants

## 🛠️ Tech Stack

**Backend:**
- Django 5.0
- Python 3.11+
- scikit-learn 1.2.2
- joblib

**Frontend:**
- Bootstrap 5
- Django Templates
- Crispy Forms

**Database:**
- SQLite (Development)
- Supabase PostgreSQL (Production)

**Storage:**
- Local filesystem (Development)
- Supabase Storage (Production)

**ML Model:**
- Random Forest Classifier
- 100 estimators, max_depth=20
- StandardScaler normalization
- 7 original features (no engineering)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Dataset: [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset) by Atharva Ingle
- Kaggle community for the dataset
- Django and scikit-learn teams

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check documentation in `docs/`

## 🎯 Future Enhancements

- [ ] Add more crops (expand beyond 22)
- [ ] Implement soil classification with images
- [ ] Add weather API integration
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Export recommendations to PDF

---

**Made with ❤️ for sustainable agriculture**
