# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-powered agricultural decision support system built with Django 5.0, providing crop recommendations and soil classification using machine learning models. The system integrates with Supabase for PostgreSQL database and cloud storage.

**Tech Stack:**
- Backend: Django 5.0 + Python 3.11+
- Database: Supabase PostgreSQL (pooler connection)
- Storage: Supabase Storage (S3-compatible)
- ML: TensorFlow/Keras (101-crop deep learning model), PyTorch (soil classification - pending implementation)
- Frontend: Django Templates + Bootstrap 5 + Crispy Forms

## Development Commands

### Environment Setup
```bash
# Activate virtual environment (Windows)
crp-venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Operations
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell (for testing ML services)
python manage.py shell
```

### Development Server
```bash
# Run development server
python manage.py runserver

# Run on specific host/port
python manage.py runserver 0.0.0.0:8000
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic --noinput
```

### Testing ML Models
```bash
# Test crop prediction model (101 crops)
python test_deeplearning_model.py

# Test with multiple scenarios
python test_multiple_scenarios.py

# Test specific crop predictions
python test_wheat.py
```

### Django Admin
```bash
# Check for issues
python manage.py check

# Show migrations status
python manage.py showmigrations
```

## High-Level Architecture

### App Structure (Django Apps Pattern)

**apps/core/** - Landing pages and shared utilities
- Supabase client singleton (apps/core/utils/supabase_client.py)
- Base templates and static assets

**apps/accounts/** - User management
- Custom user model (CustomUser) with extended fields for farmers
- UserProfile model for additional profile data
- User types: farmer, researcher, admin
- Profile pictures stored in Supabase Storage

**apps/predictions/** - ML prediction services
- CropPrediction model: stores 7 soil parameters + prediction results
- SoilClassification model: stores image uploads + classification results
- PredictionHistory model: tracks all predictions for analytics
- ML services architecture (singleton pattern):
  - crop_predictor.py: 101-crop deep learning model with lazy loading
  - soil_classifier.py: PyTorch CNN (currently mock implementation)

**apps/admin_panel/** - Admin features for dataset and model management

**config/** - Django settings and custom storage backends
- Supabase storage backend (config/supabase_storage.py) for image uploads
- Database configuration switches between SQLite (dev) and PostgreSQL (production)

### ML Model Architecture

**Crop Prediction (Production Ready):**
- Location: ml_models/ directory
- Files: best_crop_model.h5, scaler.pkl, label_encoder.pkl, metadata.json
- Model: Deep Learning MLP (256→128→64 neurons, 15 engineered features)
- Input: 7 parameters (N, P, K, temperature, humidity, pH, rainfall)
- Feature engineering: Creates 15 features including NPK ratios, interactions, categorical encodings
- Output: 101 crop classes with Top-3 recommendations
- Accuracy: ~64% (top-3: 90%)
- Implementation: Lazy loading pattern - model loads on first prediction to improve startup time

**Soil Classification (Mock):**
- Planned: PyTorch CNN for 4 soil types (Black, Clay, Loamy, Sandy)
- Current: Mock predictions in soil_classifier.py
- Storage: Images uploaded to Supabase Storage 'soil-images' bucket

### Database & Storage Integration

**Supabase PostgreSQL:**
- Connection via pooler (aws-1-ap-southeast-1.pooler.supabase.com:6543)
- User format: postgres.yvpumpbwujslztnnloqv for pooler connections
- SSL required in production
- Falls back to SQLite if SUPABASE_DB_HOST not set

**Supabase Storage:**
- Custom Django storage backend: config/supabase_storage.py
- Two buckets: 'soil-images' and 'profile-pictures' (both public)
- Graceful fallback to local storage if Supabase unavailable
- CDN delivery for uploaded images

### Key Design Patterns

**Singleton Pattern for ML Services:**
- get_crop_predictor() and get_soil_classifier() return singleton instances
- Prevents multiple model loads in memory
- Models are loaded lazily on first use

**Lazy Loading for Performance:**
- ML libraries (TensorFlow, joblib) only imported when prediction requested
- Improves Django startup time significantly

**Custom Storage Backends:**
- SupabaseStorage base class with methods: _save, _open, exists, url, delete, size
- SoilImageStorage and ProfilePictureStorage extend for specific buckets
- Automatic fallback handling for connection failures

### Environment Configuration

**Required .env variables:**
- SECRET_KEY: Django secret key
- DEBUG: True/False
- ALLOWED_HOSTS: Comma-separated list
- SUPABASE_URL: Project URL
- SUPABASE_KEY: Anon key
- SUPABASE_SERVICE_KEY: Service role key
- SUPABASE_DB_PASSWORD: Database password
- SUPABASE_DB_HOST: Pooler host
- SUPABASE_DB_PORT: Default 6543
- CROP_MODEL_PATH: Optional, defaults to ml_models/crop_predictor/v1.0/model.pkl
- SOIL_MODEL_PATH: Optional, defaults to ml_models/soil_classifier/v1.0/model.pth

### URL Structure

- `/` - Core app (landing, about, contact)
- `/accounts/` - Registration, login, profile
- `/predictions/` - Crop prediction, soil classification, history
- `/admin-panel/` - Dataset upload, model training, analytics
- `/admin/` - Django admin interface

## Important Implementation Notes

### When Working with ML Models

**Crop Predictor (apps/predictions/ml_services/crop_predictor.py:99):**
- Feature engineering must match training: _engineer_features() creates 15 features from 7 inputs
- Temperature categories: <15 cold, 15-25 cool, 25-35 warm, >35 hot
- Rainfall categories: <100 low, 100-200 medium, 200-300 high, >300 very_high
- Returns dict with predicted_crop, confidence_score, top_3_crops, num_total_crops
- Fallback to _mock_prediction() if model fails to load

**Soil Classifier (apps/predictions/ml_services/soil_classifier.py:28):**
- Currently returns mock predictions
- When implementing: resize images to 224x224, normalize, convert to tensor
- Expected output: soil_type, confidence_score, all_predictions (dict of 4 soil types)

### When Working with Supabase Storage

Storage uploads automatically handle:
- Unique filename generation with timestamps
- Content-type detection from file extensions
- Graceful fallback to local storage on failure
- Public URL generation for CDN delivery

Error handling is built-in - check console for "[WARNING]" messages if uploads fail.

### When Adding New Predictions

1. Create model in apps/predictions/models.py
2. Add form in apps/predictions/forms.py
3. Create view in apps/predictions/views.py
4. Add PredictionHistory entry for analytics
5. Create templates in apps/predictions/templates/predictions/

### Database Migrations

The project uses Supabase PostgreSQL in production. When creating migrations:
- Test with SQLite first (no SUPABASE_DB_HOST in .env)
- Then test with Supabase connection
- Migrations auto-create tables in Supabase PostgreSQL

## Testing Workflow

**Quick ML Model Test:**
```bash
# Test in Django shell
python manage.py shell

# Import and test
from apps.predictions.ml_services.crop_predictor import get_crop_predictor
predictor = get_crop_predictor()
result = predictor.predict({
    'nitrogen': 120, 'phosphorus': 60, 'potassium': 80,
    'temperature': 28, 'humidity': 75, 'ph_value': 6.8, 'rainfall': 2000
})
print(result['predicted_crop'], result['confidence_percent'])
```

**Test Cases:**
- Sugarcane: N=120, P=60, K=80, Temp=28, Humidity=75, pH=6.8, Rainfall=2000 (should be ~100%)
- Wheat: N=80, P=40, K=40, Temp=18, Humidity=65, pH=6.8, Rainfall=600 (should be in Top-3)
- Rice: N=90, P=42, K=43, Temp=21, Humidity=82, pH=6.5, Rainfall=203 (high confidence)

## Common Issues

**Model Not Loading:**
- Check ml_models/ directory contains: best_crop_model.h5, scaler.pkl, label_encoder.pkl
- Verify TensorFlow installed: pip install tensorflow
- Look for "[ERROR]" messages in console
- System falls back to mock predictions if model unavailable

**Supabase Connection:**
- SQLite is used if SUPABASE_DB_HOST not in .env
- Check pooler format for production: postgres.{project_id} as user
- Storage gracefully falls back to local media/ directory

**Static Files Not Loading:**
- Run: python manage.py collectstatic --noinput
- Check STATIC_ROOT in config/settings.py
- WhiteNoise middleware handles static files in production

**Import Errors:**
- Ensure virtual environment activated: crp-venv\Scripts\activate (Windows)
- Reinstall requirements: pip install -r requirements.txt

## Production Deployment

**Checklist:**
- Set DEBUG=False in .env
- Configure ALLOWED_HOSTS
- Run collectstatic
- Set up Supabase buckets: 'soil-images' and 'profile-pictures' (public)
- Run migrations on Supabase PostgreSQL
- Use gunicorn: `gunicorn config.wsgi:application --bind 0.0.0.0:8000`

**Security Settings:**
- Production automatically enables: SSL redirect, secure cookies, HSTS, XSS filter
- Configured in config/settings.py:211-220
