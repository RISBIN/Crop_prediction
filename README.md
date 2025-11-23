# 🌾 Crop Prediction & Soil Classification System

AI-powered agricultural decision support system using Machine Learning and Deep Learning to help farmers make data-driven decisions.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4.0-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

A production-ready Django web application that combines **two powerful AI models** to provide intelligent agricultural recommendations:

1. **Crop Prediction** - Random Forest model (99% accuracy) recommends best crops based on 7 soil/climate parameters
2. **Soil Classification** - PyTorch ResNet18 model (97.37% accuracy) identifies soil type from images

This system helps farmers choose the right crops and understand their soil type without expensive laboratory testing.

## 🎯 Problem Statement & Solution

### Problems Faced by Farmers:
- ❌ **Wrong Crop Selection** - Planting unsuitable crops leads to poor yield and financial loss
- ❌ **Lack of Scientific Data** - Traditional farming relies on experience, not data-driven decisions
- ❌ **Expensive Soil Testing** - Laboratory soil tests cost money and take time
- ❌ **Low Productivity** - Incorrect crop choices result in crop failure

### How This System Helps:
- ✅ **Instant Recommendations** - Get top-3 crop suggestions in seconds
- ✅ **99% Accurate** - ML model trained on 2,200+ agricultural samples
- ✅ **Free Soil Analysis** - Upload soil photo, get type identification instantly
- ✅ **Data-Driven** - Analyzes 7 key parameters for scientific recommendations
- ✅ **Easy to Use** - Simple web interface accessible from any device
- ✅ **Cost-Free** - No need for expensive laboratory testing

## ✨ Key Features

### 🎯 Crop Recommendation System
- **99% Accuracy** - Random Forest model trained on 2,200 samples
- **Top-3 Suggestions** - Get multiple crop alternatives with confidence scores
- **22 Crops Supported** - Rice, Wheat, Cotton, Coffee, and 18 more
- **7 Input Parameters** - N, P, K, temperature, humidity, pH, rainfall
- **Instant Results** - Get recommendations in seconds

### 🌱 Soil Classification System
- **97.37% Accuracy** - PyTorch ResNet18 with transfer learning
- **4 Soil Types** - Black, Clay, Loamy, Sandy
- **Image-Based** - Upload soil photo and get instant classification
- **Confidence Scores** - Shows probability for all 4 soil types
- **Cloud Storage** - Images stored in Supabase S3-compatible storage

### 👥 User Management
- **Custom User Model** - Farmer-specific fields (location, farm size, etc.)
- **User Profiles** - Profile pictures, bio, language preferences
- **Prediction History** - Track all your past predictions
- **Role-Based Access** - Farmer, Researcher, Admin user types

### ☁️ Cloud Integration
- **Supabase PostgreSQL** - Production database with pooler connection
- **Supabase Storage** - S3-compatible image storage with CDN
- **Auto Fallback** - Gracefully falls back to local storage if cloud unavailable
- **Secure** - SSL, CSRF protection, secure cookies in production

## 🚀 Quick Start

### System Requirements

**Minimum Requirements:**
- Python 3.11 or higher
- 4 GB RAM (8 GB recommended for training)
- 2 GB free disk space
- Internet connection (for cloud features)

**Supported Platforms:**
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian, Fedora)

**Supported Browsers:**
- Chrome 90+ (recommended)
- Firefox 88+
- Safari 14+
- Edge 90+

### Prerequisites

- Python 3.11+
- pip (Python package installer)
- Virtual environment (recommended)
- Git (for cloning repository)

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

## 🎬 Quick Demo

### Example 1: Crop Prediction

**Input Parameters:**
```
Nitrogen (N): 90 mg/kg
Phosphorus (P): 42 mg/kg
Potassium (K): 43 mg/kg
Temperature: 21°C
Humidity: 82%
pH: 6.5
Rainfall: 203 mm
```

**Expected Output:**
```
Primary Crop: Rice
Confidence: 95.3%

Top-3 Recommendations:
1. Rice      - 95.3% ████████████████████
2. Wheat     - 3.2%  ███
3. Maize     - 1.5%  █
```

### Example 2: Soil Classification

**Input:** Upload a soil image

**Expected Output:**
```
Soil Type: Black Soil
Confidence: 85.7%

All Soil Types:
- Black Soil: 85.7%
- Clay Soil: 10.2%
- Loamy Soil: 3.5%
- Sandy Soil: 0.6%
```

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

## 🌱 Soil Classification (Production Ready!)

### Using Pre-trained Soil Model

The repository includes a trained PyTorch ResNet18 model in `ml_models/soil_classifier/v1.0/`:
- `model.pth` - Trained model (97.37% accuracy)
- `metadata.json` - Model configuration and performance metrics

**Performance:**
- ✅ **Validation Accuracy: 97.37%**
- Training: 911 samples
- Validation: 304 samples
- Model: ResNet18 with Transfer Learning
- Training Time: ~20 minutes (Kaggle GPU)

**Usage:**
1. Upload soil image via web interface at `/predictions/soil/`
2. Model automatically classifies into 4 soil types
3. View confidence scores for all soil types
4. Image stored in Supabase Storage with CDN delivery

**Test Soil Classification:**
```bash
# Test with sample images
python scripts/testing/test_soil_classification.py

# Sample images available at:
# datasets/test_samples/soil_images/
```

### Train Your Own Soil Model (Optional)

**On Kaggle (Free GPU):**

1. Upload notebook: `notebooks/soil_classification_kaggle.ipynb`
2. Add dataset: [SOIL TYPES DATASET](https://www.kaggle.com/datasets/posthumus/soil-types)
3. Enable GPU accelerator
4. Click "Run All" (~20 minutes)
5. Download trained model (model.pth)

See [SOIL_CLASSIFICATION_KAGGLE_GUIDE.md](docs/SOIL_CLASSIFICATION_KAGGLE_GUIDE.md) for step-by-step instructions.

## 📊 Model Performance

### Crop Prediction Model (Random Forest)

| Metric | Value |
|--------|-------|
| Algorithm | Random Forest (100 trees) |
| Test Accuracy | 99.09% |
| Top-3 Accuracy | 100% |
| Training Samples | 2,200 |
| Test Samples | 66 verified |
| Features | 7 (N, P, K, temp, humidity, pH, rainfall) |
| Crops Supported | 22 |
| Model Size | 3.1 MB |

**Supported Crops:**
Rice, Maize, Wheat, Cotton, Coffee, Sugarcane, Banana, Mango, Apple, Orange, Grapes, Coconut, Watermelon, Muskmelon, Pomegranate, Chickpea, Kidneybeans, Lentil, Blackgram, Mungbean, Pigeonpeas, Mothbeans

### Soil Classification Model (PyTorch ResNet18)

| Metric | Value |
|--------|-------|
| Algorithm | ResNet18 + Transfer Learning |
| Validation Accuracy | 97.37% |
| Training Samples | 911 |
| Validation Samples | 304 |
| Input Size | 224×224 pixels |
| Soil Types | 4 (Black, Clay, Loamy, Sandy) |
| Model Size | 45 MB |
| Framework | PyTorch |

**Soil Types:**
- **Black Soil** - Clay-rich, high water retention, ideal for cotton
- **Clay Soil** - Heavy, sticky when wet, good water holding capacity
- **Loamy Soil** - Best for agriculture, balanced mixture of sand/silt/clay
- **Sandy Soil** - Light, fast draining, good for root vegetables

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
│   ├── crop_prediction_training_kaggle.ipynb
│   └── soil_classification_kaggle.ipynb
│
├── datasets/                    # Data files
│   ├── crop_data/
│   │   └── Crop_recommendation.csv  # 2,200 training samples
│   └── test_samples/
│       ├── test_samples_real.csv    # 66 verified crop samples
│       ├── test_samples_real.json   # JSON format
│       └── soil_images/             # 4 soil test images
│           ├── Alluvial_9.jpg       # Loamy soil
│           ├── Black_9.jpg          # Black soil
│           ├── Copy of clay-soil.jpg# Clay soil
│           └── images202.jpg        # Sandy soil
│
├── crop-prediction-models/      # Trained crop models
│   ├── random_forest_model.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── metadata.json
│
├── ml_models/                   # ML model storage
│   └── soil_classifier/
│       └── v1.0/
│           ├── model.pth        # PyTorch model (train on Kaggle)
│           └── metadata.json    # Model config
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

**Project Documentation:**
- [College Explanation](college_explanation.md) - Short project explanation for presentations
- [Complete Project Documentation](project_exp.md) - Detailed project documentation

**Crop Prediction:**
- [Training Guide](docs/TRAINING_GUIDE.md) - How to train models
- [Kaggle Notebook Guide](docs/KAGGLE_NOTEBOOK_GUIDE.md) - Train on Kaggle
- [Dataset Download Guide](docs/DATASET_DOWNLOAD_GUIDE.md) - Get training data
- [User Testing Guide](docs/USER_TESTING_GUIDE.md) - Test with real samples

**Soil Classification:**
- [Soil Classification Kaggle Guide](docs/SOIL_CLASSIFICATION_KAGGLE_GUIDE.md) - Train soil model
- [Soil Classification Status](docs/SOIL_CLASSIFICATION_STATUS.md) - Implementation details

**For Developers:**
- [Claude Code Guide](CLAUDE.md) - For AI assistants
- [Organization Summary](ORGANIZATION_SUMMARY.md) - Project structure overview

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 5.0.1
- **Language:** Python 3.11+
- **ML Libraries:**
  - scikit-learn 1.4.0 (Random Forest)
  - PyTorch 2.0+ (Deep Learning)
  - torchvision (Image processing)
  - NumPy 1.26.3, Pandas 2.1.4
  - joblib 1.3.2 (Model serialization)
- **Image Processing:** Pillow 10.1.0, OpenCV, albumentations

### Frontend
- **CSS Framework:** Bootstrap 5
- **Templates:** Django Templates
- **Forms:** django-crispy-forms 2.3+, crispy-bootstrap5
- **UI:** Responsive design with mobile support

### Database & Storage
- **Development:** SQLite3 (default)
- **Production:** Supabase PostgreSQL (pooler connection)
- **Image Storage:**
  - Supabase Storage (S3-compatible)
  - Custom Django storage backend
  - Auto-fallback to local filesystem
- **Buckets:** soil-images, profile-pictures (public)

### Cloud Services
- **Supabase PostgreSQL** - Managed PostgreSQL database
- **Supabase Storage** - S3-compatible object storage with CDN
- **Custom Storage Backend** - Graceful fallback mechanism

### Production & Deployment
- **Server:** Gunicorn 21.2.0
- **Static Files:** WhiteNoise 6.6.0
- **Security:** SSL redirect, secure cookies, CSRF protection, HSTS
- **Environment:** python-dotenv for configuration

### Machine Learning Models

**Crop Prediction:**
- Algorithm: Random Forest Classifier
- Estimators: 100 trees
- Max Depth: 20
- Features: 7 (N, P, K, temperature, humidity, pH, rainfall)
- Normalization: StandardScaler
- Accuracy: 99.09%
- Model Size: 3.1 MB

**Soil Classification:**
- Architecture: ResNet18 with Transfer Learning
- Input: 224×224 RGB images
- Normalization: ImageNet statistics
- Custom FC Layers: 512→256→4
- Dropout: 0.5, 0.3
- Accuracy: 97.37%
- Model Size: 45 MB
- Framework: PyTorch

### Development Tools
- **Testing:** pytest, pytest-django, pytest-cov
- **Code Quality:** black, flake8
- **Version Control:** Git
- **Notebooks:** Jupyter for model training

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

Developed as a **Final Year MCA Project**

## 🙏 Acknowledgments

**Datasets:**
- [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset) by Atharva Ingle - 2,200 samples
- [Soil Types Dataset](https://www.kaggle.com/datasets/posthumus/soil-types) by Posthumus - 1,215 images

**Technologies:**
- Django and Python communities
- scikit-learn and PyTorch teams
- Supabase for cloud infrastructure
- Kaggle for free GPU training
- Bootstrap team for UI framework

**Special Thanks:**
- Kaggle community for datasets and notebooks
- Agricultural researchers for domain knowledge
- Open source contributors

## 📞 Support

**For Issues and Questions:**
- 📧 Open an issue on GitHub
- 📖 Check documentation in `docs/` folder
- 💬 Read [College Explanation](college_explanation.md) for quick overview
- 📚 See [Complete Documentation](project_exp.md) for details

**Resources:**
- [Django Documentation](https://docs.djangoproject.com/)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Supabase Documentation](https://supabase.com/docs)

## 🎯 Future Enhancements

### Completed ✅
- [x] Crop prediction with Random Forest (99% accuracy)
- [x] Soil classification with ResNet18 (97.37% accuracy)
- [x] User authentication and profiles
- [x] Prediction history tracking
- [x] Supabase cloud integration
- [x] Responsive Bootstrap UI

### Planned 📋
- [ ] **Fertilizer Recommendations** - NPK requirements based on crop and soil
- [ ] **Weather API Integration** - Real-time weather data for better predictions
- [ ] **Disease Detection** - Plant disease identification from leaf images
- [ ] **Market Price Prediction** - Crop price forecasting using time series
- [ ] **Mobile App** - Android/iOS native applications
- [ ] **Multi-Language Support** - Hindi, Tamil, Telugu, Kannada
- [ ] **Chatbot Assistant** - AI-powered farmer query resolution
- [ ] **Export to PDF** - Download prediction reports
- [ ] **Analytics Dashboard** - Charts and insights for admin
- [ ] **SMS/Email Notifications** - Alerts for crop recommendations
- [ ] **Expand Crop Database** - Support 100+ crops
- [ ] **Community Forum** - Farmers can share experiences
- [ ] **REST API** - API endpoints for third-party integrations

## 📈 Project Statistics

- **Total Code:** 2,000+ lines of Python
- **Database Models:** 6 models
- **ML Models:** 2 production-ready models
- **Accuracy:** 99% (crop) + 97.37% (soil)
- **Training Samples:** 3,115 total (2,200 crop + 915 soil)
- **Test Coverage:** 66 verified crop samples + 4 soil test images
- **Model Storage:** ~48 MB total

## 🏆 Key Achievements

✅ Successfully integrated 2 ML models in Django
✅ Achieved 99% and 97.37% accuracy respectively
✅ Implemented custom Supabase storage backend
✅ Built production-ready cloud architecture
✅ Created comprehensive documentation
✅ Singleton + lazy loading for performance
✅ Graceful fallback mechanisms

## 📸 Screenshots

**Crop Prediction Form**
- Enter 7 soil/climate parameters
- Get instant recommendations

**Crop Result Page**
- Top-3 crop suggestions with confidence bars
- Detailed input parameter display

**Soil Classification**
- Upload soil image
- View probabilities for all 4 soil types
- Image stored in cloud storage

**User Dashboard**
- View recent predictions
- Access profile settings
- Track prediction history

## 👨‍💻 For Developers

### Quick Commands
```bash
# Start development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python scripts/testing/test_django_predictor.py

# Collect static files
python manage.py collectstatic
```

### API Endpoints
```
/                           - Homepage
/accounts/register/         - User registration
/accounts/login/            - User login
/predictions/crop/          - Crop prediction form
/predictions/soil/          - Soil classification form
/predictions/history/       - Prediction history
/admin/                     - Django admin panel
```

### Environment Setup
See `.env.example` for required environment variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `SUPABASE_DB_PASSWORD` - Database password

---

**Made with ❤️ for sustainable agriculture and data-driven farming**
