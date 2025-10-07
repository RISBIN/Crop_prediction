# Crop Prediction Application

**AI-Powered Crop Recommendation & Soil Classification System**

Built with Django 5.0 + Supabase + XGBoost + PyTorch

---

## 📋 Project Overview

This application helps farmers make data-driven crop selection decisions using:
- **Crop Prediction**: 7 soil parameters → 22 crop recommendations (XGBoost)
- **Soil Classification**: Image upload → 4 soil types (PyTorch CNN)
- **Fertilizer Recommendations**: Crop-specific NPK guidance
- **Prediction History**: Track and export predictions

**Target Accuracy**: >84% (Crop Prediction), >88% (Soil Classification)

---

## 🛠️ Technology Stack

- **Frontend**: Django Templates + Bootstrap 5
- **Backend**: Django 5.0 + Python 3.11+
- **Database**: Supabase PostgreSQL 16+
- **Storage**: Supabase Storage (S3-compatible)
- **Auth**: Supabase Auth
- **ML**: XGBoost 2.0 (Crop) + PyTorch 2.1 (Soil)

---

## 📁 Project Structure

```
crop_prediction_app/
├── manage.py
├── requirements.txt
├── .env (create from .env.example)
├── .gitignore
├── config/                    # Django settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                      # Django applications
│   ├── core/                  # Landing page, base templates
│   ├── accounts/              # User auth, registration, profile
│   ├── predictions/           # Crop prediction, ML models
│   └── admin_panel/           # Dataset & model management
├── ml_models/                 # Trained ML models
│   ├── crop_predictor/v1.0/
│   └── soil_classifier/v1.0/
├── datasets/                  # Training datasets
│   ├── crop_data/
│   └── soil_images/
├── media/                     # User uploads
├── staticfiles/               # Collected static files
├── logs/                      # Application logs
├── scripts/                   # Utility scripts
└── templates/                 # Base templates
```

---

## 🚀 Quick Start

### **Step 1: Prerequisites**

- Python 3.11+ installed
- Git installed
- Supabase account (free tier): https://supabase.com

### **Step 2: Clone & Setup**

```bash
cd /home/user/Desktop/Crop_Prediction/crop_prediction_app

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### **Step 3: Configure Environment**

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required environment variables:**
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon key
- `SUPABASE_SERVICE_KEY` - Your Supabase service role key
- `SECRET_KEY` - Django secret key (generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)

### **Step 4: Setup Supabase Database**

**Option 1: Via Supabase Dashboard (Recommended)**
1. Go to [Supabase SQL Editor](https://supabase.com/dashboard)
2. Navigate to your project → SQL Editor
3. Copy contents from `supabase_django_migration.sql`
4. Paste and click **RUN**

**Option 2: Via Command Line**
```bash
python migrate_to_supabase.py
# Follow the instructions to copy SQL to Supabase Dashboard
```

This creates:
- 5 main tables (user_profiles, crop_predictions, soil_classifications, fertilizer_recommendations, prediction_history)
- Row-Level Security policies
- Indexes for performance
- Storage buckets (soil-images, datasets, ml-models) - Already created

### **Step 5: Run Migrations**

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for Django admin
python manage.py createsuperuser
```

### **Step 6: Collect Static Files**

```bash
python manage.py collectstatic --noinput
```

### **Step 7: Run Development Server**

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 📊 Training ML Models

### **Crop Prediction Model (XGBoost)**

```bash
# Place dataset in datasets/crop_data/train.csv
# Expected columns: N, P, K, temperature, humidity, ph, rainfall, label

python scripts/train_crop_model.py
```

**Expected output:**
- Model saved to: `ml_models/crop_predictor/v1.0/model.pkl`
- Accuracy: >84%

### **Soil Classification Model (PyTorch CNN)**

```bash
# Place images in datasets/soil_images/train/{Black,Clay,Loamy,Sandy}/

python scripts/train_soil_model.py
```

**Expected output:**
- Model saved to: `ml_models/soil_classifier/v1.0/model.pth`
- Accuracy: >88%

---

## 🔐 First-Time Setup Checklist

- [ ] Create Supabase project
- [ ] Get API credentials (URL, anon key, service key)
- [ ] Configure `.env` file
- [ ] Run `python scripts/setup_supabase.py`
- [ ] Run Django migrations
- [ ] Train ML models OR download pre-trained models
- [ ] Create first admin user (via Supabase SQL: `UPDATE user_profiles SET role='admin' WHERE email='your-email@example.com'`)
- [ ] Start development server

---

## 📝 Key Features

### **User Features:**
- ✅ Registration & Login (Supabase Auth)
- ✅ Crop Prediction Form (7 soil parameters)
- ✅ Soil Image Upload & Classification
- ✅ Top 3 Crop Recommendations
- ✅ Fertilizer Recommendations
- ✅ Prediction History with Filters
- ✅ Export to PDF/CSV
- ✅ User Feedback System

### **Admin Features:**
- ✅ Upload Training Datasets (CSV/ZIP)
- ✅ Train ML Models (XGBoost/PyTorch)
- ✅ Monitor Training Progress
- ✅ Evaluate Model Performance
- ✅ Deploy Models
- ✅ View Analytics & Logs

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# View coverage report
open htmlcov/index.html
```

---

## 📦 Deployment

### **Local Development**
```bash
python manage.py runserver
```

### **Production (Gunicorn + Nginx)**
```bash
# Update .env: DEBUG=False
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

**Deployment Options:**
- PythonAnywhere (easiest for Django)
- Railway
- Heroku
- AWS EC2
- Google Cloud Run

---

## 📖 API Documentation

### **Prediction API**
- `POST /predictions/create/` - Create new prediction
- `GET /predictions/{id}/` - Get prediction results
- `GET /predictions/history/` - List user's predictions
- `POST /predictions/{id}/feedback/` - Submit user feedback

### **Admin API**
- `POST /admin-panel/datasets/upload/` - Upload dataset
- `POST /admin-panel/models/train/` - Start training
- `GET /admin-panel/models/{id}/status/` - Get training progress
- `POST /admin-panel/models/{id}/deploy/` - Deploy model

---

## 🐛 Troubleshooting

### **Database Connection Error**
```
Solution: Check SUPABASE_URL and database credentials in .env
```

### **Model Not Found**
```
Solution: Train models using scripts/train_*.py or download pre-trained models
```

### **Import Error: supabase**
```
Solution: pip install supabase==2.3.0
```

### **Static Files Not Loading**
```
Solution: python manage.py collectstatic --noinput
```

---

## 📞 Support

- **Documentation**: `/DOCS/MASTER_PRD_FINAL.md`
- **Django Docs**: https://docs.djangoproject.com/
- **Supabase Docs**: https://supabase.com/docs

---

## 📄 License

This project is proprietary software for agricultural use.

---

## 🎯 Roadmap

- [x] Phase 1: Project Setup
- [x] Phase 2: Core App Development
- [x] Phase 3: ML Model Integration
- [ ] Phase 4: Production Deployment
- [ ] Phase 5: Mobile App (React Native)

---

**Version**: 1.0
**Last Updated**: October 7, 2025
**Status**: Development Ready ✅

---

## 🗃️ Database Setup

The application uses **SQLite** for local development and **Supabase PostgreSQL** for production.

### Local Development (SQLite)
- Database: `db.sqlite3`
- Tables auto-created via Django migrations
- Perfect for testing and development

### Production (Supabase)
- Execute `supabase_django_migration.sql` in Supabase Dashboard
- Provides scalability, real-time features, and cloud storage
- Row-Level Security for data protection

### Files
- `supabase_django_migration.sql` - SQL schema for Supabase
- `migrate_to_supabase.py` - Helper script to generate migration SQL
