# Quick Start Guide - Crop Prediction System

## 🚀 Getting Started (Already Set Up!)

The application is already running! Here's how to use it:

## 📍 Access URLs

### Main Application
- **Home Page:** http://127.0.0.1:8000/
- **Register:** http://127.0.0.1:8000/accounts/register/
- **Login:** http://127.0.0.1:8000/accounts/login/

### Admin Panel
- **URL:** http://127.0.0.1:8000/admin/
- **Username:** `admin`
- **Password:** `admin123`

## 🎯 Test the Application

### Step 1: Create a User Account
1. Go to http://127.0.0.1:8000/accounts/register/
2. Fill in the registration form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123`
   - User Type: Farmer
   - (Optional) Add location, phone, farm size
3. Click "Register"

### Step 2: Login
1. Go to http://127.0.0.1:8000/accounts/login/
2. Enter credentials:
   - Username: `testuser`
   - Password: `testpass123`
3. Click "Login"

### Step 3: Make a Crop Prediction
1. Click "Dashboard" or go to http://127.0.0.1:8000/dashboard/
2. Click "Start Prediction" under "Crop Prediction"
3. Fill in sample data:
   ```
   Nitrogen (N): 90
   Phosphorus (P): 42
   Potassium (K): 43
   Temperature: 20.5
   Humidity: 80
   pH Value: 6.5
   Rainfall: 200
   Location: Maharashtra (optional)
   ```
4. Click "Predict Best Crop"
5. View your results!

### Step 4: Classify Soil (Optional)
1. From dashboard, click "Classify Soil"
2. Upload any soil image (JPG/PNG)
3. Add location (optional)
4. Click "Classify Soil Type"
5. View classification results

### Step 5: Check History
1. Go to http://127.0.0.1:8000/predictions/history/
2. See all your past predictions
3. Click "View" to see detailed results

## 🔧 Development Commands

### Start Server (if stopped)
```bash
cd /home/user/Desktop/Crop_Prediction/crop_prediction_app
source crop_venv/bin/activate
python manage.py runserver
```

### Create Superuser (if needed)
```bash
python manage.py createsuperuser
```

### Run Migrations (if models change)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

## 📊 Sample Test Data

### Crop Prediction Examples:

**For Rice:**
- N: 80, P: 40, K: 40
- Temp: 25, Humidity: 80, pH: 6.5, Rainfall: 200

**For Wheat:**
- N: 50, P: 30, K: 30
- Temp: 20, Humidity: 60, pH: 6.8, Rainfall: 60

**For Cotton:**
- N: 120, P: 40, K: 60
- Temp: 28, Humidity: 70, pH: 7.0, Rainfall: 100

## 🗂️ File Locations

- **Database:** `db.sqlite3`
- **Media Files:** `media/` (uploaded soil images)
- **Static Files:** `static/`
- **Templates:** `apps/*/templates/`
- **ML Models:** `ml_models/` (to be added)

## 🐛 Troubleshooting

### Server won't start?
```bash
# Kill any existing processes
pkill -f "manage.py runserver"

# Restart server
python manage.py runserver
```

### Database errors?
```bash
# Reset database (WARNING: Deletes all data)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Import errors?
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 📱 Mobile Testing

The UI is fully responsive! Test on mobile by:
1. Find your local IP: `ip addr show | grep inet`
2. Update ALLOWED_HOSTS in .env: `ALLOWED_HOSTS=localhost,127.0.0.1,192.168.x.x`
3. Access from mobile: `http://192.168.x.x:8000/`

## 🎨 Customization

### Change Theme Colors
Edit `templates/base.html`, line 14-18:
```css
:root {
    --primary-color: #2d5016;    /* Main green */
    --secondary-color: #8b6914;   /* Brown */
    --accent-color: #daa520;      /* Gold */
}
```

### Add New Crops
Edit `apps/predictions/ml_services/crop_predictor.py`, line 16-20

### Change Soil Types
Edit `apps/predictions/models.py`, line 53-58

## 📈 Next Steps

1. **Integrate Real ML Models:**
   - Train XGBoost model on crop dataset
   - Train CNN model on soil images
   - Replace mock predictions in `ml_services/`

2. **Add Features:**
   - Fertilizer recommendations
   - Weather API integration
   - PDF report generation
   - Multi-language support

3. **Production Deployment:**
   - Set up PostgreSQL/Supabase
   - Configure environment variables
   - Set DEBUG=False
   - Add security headers
   - Deploy to cloud platform

## 🆘 Need Help?

- Check `IMPLEMENTATION_STATUS.md` for detailed feature list
- See `README.md` for full documentation
- Review code in `apps/` directories
- Check Django logs in console

---

**Enjoy your Crop Prediction System!** 🌾
