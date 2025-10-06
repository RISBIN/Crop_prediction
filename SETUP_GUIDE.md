# Complete Setup Guide - Crop Prediction Application

**Step-by-Step Instructions to Get the Application Running**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Supabase Configuration](#supabase-configuration)
4. [Django Setup](#django-setup)
5. [ML Models Setup](#ml-models-setup)
6. [First Run](#first-run)
7. [Creating First Admin User](#creating-first-admin-user)
8. [Verification](#verification)

---

## 1. Prerequisites

### Install Python 3.11+

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

**macOS:**
```bash
brew install python@3.11
```

**Windows:**
- Download from https://www.python.org/downloads/
- Check "Add Python to PATH" during installation

### Verify Installation
```bash
python3.11 --version
# Should show: Python 3.11.x
```

---

## 2. Environment Setup

### Step 2.1: Navigate to Project Directory
```bash
cd /home/user/Desktop/Crop_Prediction/crop_prediction_app
```

### Step 2.2: Create Virtual Environment
```bash
python3.11 -m venv venv
```

### Step 2.3: Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 2.4: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected time**: 5-10 minutes

**Troubleshooting:**
- If `psycopg2-binary` fails on macOS: `brew install postgresql`
- If `torch` is slow: Use `pip install torch --index-url https://download.pytorch.org/whl/cpu` for CPU-only version

---

## 3. Supabase Configuration

### Step 3.1: Create Supabase Project

1. Go to https://supabase.com
2. Click "New Project"
3. Fill in:
   - **Name**: crop-prediction
   - **Database Password**: (generate strong password - SAVE IT!)
   - **Region**: Southeast Asia (Singapore) or closest
   - **Plan**: Free

### Step 3.2: Get API Credentials

1. In Supabase Dashboard → Settings → API
2. Copy these values:

```
Project URL: https://xxxxxxxxxxxxx.supabase.co
anon public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 3.3: Configure Environment File

```bash
# Copy template
cp .env.example .env

# Edit .env
nano .env  # or use your favorite editor
```

**Update these values in `.env`:**
```bash
# Generate Django secret key
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Supabase credentials (from Step 3.2)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Database (extract from Supabase Settings → Database)
SUPABASE_DB_PASSWORD=your-database-password
SUPABASE_DB_HOST=db.your-project-id.supabase.co
```

### Step 3.4: Setup Database Schema

**Run SQL in Supabase SQL Editor** (Settings → SQL Editor → New Query):

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Profiles Table
CREATE TABLE public.user_profiles (
    id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    phone TEXT,
    state TEXT,
    district TEXT,
    role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Predictions Table
CREATE TABLE public.predictions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.user_profiles(id) ON DELETE CASCADE NOT NULL,
    nitrogen DECIMAL(6,2) NOT NULL,
    phosphorus DECIMAL(6,2) NOT NULL,
    potassium DECIMAL(6,2) NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    humidity DECIMAL(5,2) NOT NULL,
    ph DECIMAL(4,2) NOT NULL,
    rainfall DECIMAL(7,2) NOT NULL,
    soil_image_url TEXT,
    soil_type TEXT,
    predicted_crops JSONB NOT NULL,
    top_crop TEXT NOT NULL,
    top_crop_probability DECIMAL(5,2) DEFAULT 0.0,
    fertilizer_name TEXT NOT NULL,
    fertilizer_dosage TEXT NOT NULL,
    fertilizer_timing TEXT NOT NULL,
    fertilizer_cost DECIMAL(10,2) NOT NULL,
    model_version TEXT DEFAULT '1.0',
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    user_feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Enable Row-Level Security
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.predictions ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view their own profile"
    ON public.user_profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can view their own predictions"
    ON public.predictions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own predictions"
    ON public.predictions FOR INSERT
    WITH CHECK (auth.uid() = user_id);
```

### Step 3.5: Create Storage Buckets

**In Supabase Dashboard → Storage:**

1. Create bucket: **soil-images**
   - Public: Yes
   - Allowed MIME types: `image/jpeg, image/png`
   - Max file size: 5 MB

2. Create bucket: **datasets** (admin only)
   - Public: No
   - Allowed MIME types: `text/csv, application/zip`

3. Create bucket: **ml-models** (admin only)
   - Public: No
   - Allowed MIME types: `application/octet-stream`

### Step 3.6: Enable Email Authentication

**Supabase Dashboard → Authentication → Providers:**
- Enable **Email** provider
- Disable "Confirm email" for development (enable in production)

---

## 4. Django Setup

### Step 4.1: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4.2: Create Django Superuser

```bash
python manage.py createsuperuser

# Enter:
# Username: admin
# Email: your-email@example.com
# Password: (strong password)
```

### Step 4.3: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## 5. ML Models Setup

You have two options:

### **Option A: Download Pre-trained Models** (Recommended for Quick Start)

```bash
# Download from project repository or cloud storage
# Place files in:
# - ml_models/crop_predictor/v1.0/model.pkl
# - ml_models/soil_classifier/v1.0/model.pth
```

### **Option B: Train Models from Scratch**

#### Crop Prediction Model

```bash
# 1. Prepare dataset (CSV with columns: N, P, K, temperature, humidity, ph, rainfall, label)
# Place in: datasets/crop_data/train.csv

# 2. Run training script
python scripts/train_crop_model.py

# Expected output:
# - Training accuracy: >84%
# - Model saved to: ml_models/crop_predictor/v1.0/model.pkl
```

#### Soil Classification Model

```bash
# 1. Prepare image dataset
# Directory structure:
# datasets/soil_images/train/
#   ├── Black/
#   ├── Clay/
#   ├── Loamy/
#   └── Sandy/

# 2. Run training script
python scripts/train_soil_model.py

# Expected output:
# - Training accuracy: >88%
# - Model saved to: ml_models/soil_classifier/v1.0/model.pth
```

---

## 6. First Run

### Step 6.1: Start Development Server

```bash
python manage.py runserver
```

**Expected output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 02, 2025 - 12:00:00
Django version 5.0.1, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Step 6.2: Access Application

Open browser: **http://127.0.0.1:8000/**

You should see the landing page with:
- Hero section
- Feature cards (Crop Prediction, Soil Classification, Fertilizer Recommendations)
- Login/Sign Up buttons

---

## 7. Creating First Admin User

### Step 7.1: Register User via Application

1. Go to http://127.0.0.1:8000/accounts/register/
2. Fill in registration form
3. Click "Sign Up"
4. Check email for verification (if enabled)

### Step 7.2: Promote to Admin

**In Supabase Dashboard → SQL Editor:**

```sql
-- Update user role to admin
UPDATE public.user_profiles
SET role = 'admin'
WHERE email = 'your-email@example.com';
```

### Step 7.3: Verify Admin Access

1. Login to application
2. Navigate to: http://127.0.0.1:8000/admin-panel/
3. You should see admin dashboard with:
   - System metrics
   - Dataset upload
   - Model training

---

## 8. Verification

### ✅ Checklist

**Environment:**
- [ ] Python 3.11+ installed
- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list | grep Django` shows Django 5.0.1)

**Supabase:**
- [ ] Project created
- [ ] API credentials in `.env`
- [ ] Database tables created (check Supabase → Database → Tables)
- [ ] Storage buckets created (soil-images, datasets, ml-models)
- [ ] Email authentication enabled

**Django:**
- [ ] Migrations applied (`python manage.py showmigrations`)
- [ ] Superuser created
- [ ] Static files collected

**ML Models:**
- [ ] Crop prediction model exists at `ml_models/crop_predictor/v1.0/model.pkl`
- [ ] Soil classification model exists at `ml_models/soil_classifier/v1.0/model.pth`

**Application:**
- [ ] Development server runs without errors
- [ ] Landing page loads at http://127.0.0.1:8000/
- [ ] Registration works
- [ ] Login works
- [ ] Admin panel accessible

### 🧪 Test Prediction

1. Login as user
2. Go to "Predict Crop"
3. Enter test values:
   - Nitrogen: 90
   - Phosphorus: 42
   - Potassium: 43
   - Temperature: 20.8
   - Humidity: 82
   - pH: 6.5
   - Rainfall: 202.9
4. Click "Predict Crop"
5. Should see: **Rice** as top recommendation (92%+ confidence)

---

## 🎉 Success!

Your Crop Prediction Application is now ready!

**Next Steps:**
1. Explore the application features
2. Upload your own datasets
3. Train custom models
4. Customize UI/templates
5. Deploy to production

---

## 🐛 Common Issues

### Issue: `ModuleNotFoundError: No module named 'supabase'`
**Solution:**
```bash
pip install supabase==2.3.0
```

### Issue: Database connection error
**Solution:**
- Check `SUPABASE_URL` and `SUPABASE_DB_PASSWORD` in `.env`
- Verify database is active in Supabase dashboard

### Issue: Static files not loading
**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Issue: ML model not found
**Solution:**
- Train models using scripts OR download pre-trained models
- Verify file paths in `config/settings.py`

---

**Need Help?** Check `/DOCS/MASTER_PRD_FINAL.md` for complete documentation.
