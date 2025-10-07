#!/usr/bin/env python
"""
Create Django tables in Supabase using the Supabase client
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

def create_tables_in_supabase():
    """Create tables in Supabase programmatically"""

    print("=" * 70)
    print("MIGRATING DJANGO TABLES TO SUPABASE")
    print("=" * 70)

    url = os.getenv('SUPABASE_URL')
    service_key = os.getenv('SUPABASE_SERVICE_KEY')

    supabase = create_client(url, service_key)

    print(f"\n✓ Connected to: {url}")

    # SQL to create tables based on Django models
    create_tables_sql = """
-- Create user profiles table (matches accounts_customuser + accounts_userprofile)
CREATE TABLE IF NOT EXISTS public.user_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    user_type VARCHAR(20) DEFAULT 'farmer',
    phone_number VARCHAR(15),
    location VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(50) DEFAULT 'India',
    farm_size DECIMAL(10, 2),
    bio TEXT,
    profile_picture VARCHAR(100),
    preferred_language VARCHAR(10) DEFAULT 'en',
    email_notifications BOOLEAN DEFAULT TRUE,
    sms_notifications BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    date_joined TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create crop predictions table
CREATE TABLE IF NOT EXISTS public.crop_predictions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    nitrogen FLOAT NOT NULL,
    phosphorus FLOAT NOT NULL,
    potassium FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    ph_value FLOAT NOT NULL,
    rainfall FLOAT NOT NULL,
    predicted_crop VARCHAR(100) NOT NULL,
    confidence_score FLOAT,
    top_3_crops JSONB DEFAULT '[]'::jsonb,
    location VARCHAR(200),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create soil classifications table
CREATE TABLE IF NOT EXISTS public.soil_classifications (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    soil_image VARCHAR(100) NOT NULL,
    soil_type VARCHAR(20) NOT NULL,
    confidence_score FLOAT NOT NULL,
    all_predictions JSONB DEFAULT '{}'::jsonb,
    location VARCHAR(200),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create fertilizer recommendations table
CREATE TABLE IF NOT EXISTS public.fertilizer_recommendations (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    crop_prediction_id BIGINT,
    crop_name VARCHAR(100) NOT NULL,
    nitrogen FLOAT NOT NULL,
    phosphorus FLOAT NOT NULL,
    potassium FLOAT NOT NULL,
    soil_type VARCHAR(20) NOT NULL,
    recommended_fertilizer VARCHAR(200) NOT NULL,
    application_rate VARCHAR(200),
    application_timing TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create prediction history table
CREATE TABLE IF NOT EXISTS public.prediction_history (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    prediction_type VARCHAR(50) NOT NULL,
    result_summary TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_crop_predictions_user_id ON public.crop_predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_soil_classifications_user_id ON public.soil_classifications(user_id);
CREATE INDEX IF NOT EXISTS idx_fertilizer_recommendations_user_id ON public.fertilizer_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_prediction_history_user_id ON public.prediction_history(user_id);

-- Enable RLS on all tables
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.crop_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.soil_classifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fertilizer_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.prediction_history ENABLE ROW LEVEL SECURITY;

-- RLS Policies for user_profiles
CREATE POLICY "Users can view own profile" ON public.user_profiles
    FOR SELECT USING (id = current_setting('app.current_user_id')::BIGINT);

CREATE POLICY "Users can update own profile" ON public.user_profiles
    FOR UPDATE USING (id = current_setting('app.current_user_id')::BIGINT);

-- RLS Policies for predictions
CREATE POLICY "Users can view own predictions" ON public.crop_predictions
    FOR SELECT USING (user_id = current_setting('app.current_user_id')::BIGINT);

CREATE POLICY "Users can insert predictions" ON public.crop_predictions
    FOR INSERT WITH CHECK (user_id = current_setting('app.current_user_id')::BIGINT);

-- RLS Policies for soil classifications
CREATE POLICY "Users can view own soil data" ON public.soil_classifications
    FOR SELECT USING (user_id = current_setting('app.current_user_id')::BIGINT);

CREATE POLICY "Users can insert soil data" ON public.soil_classifications
    FOR INSERT WITH CHECK (user_id = current_setting('app.current_user_id')::BIGINT);

-- RLS Policies for fertilizer recommendations
CREATE POLICY "Users can view own fertilizer data" ON public.fertilizer_recommendations
    FOR SELECT USING (user_id = current_setting('app.current_user_id')::BIGINT);

CREATE POLICY "Users can insert fertilizer data" ON public.fertilizer_recommendations
    FOR INSERT WITH CHECK (user_id = current_setting('app.current_user_id')::BIGINT);

-- RLS Policies for prediction history
CREATE POLICY "Users can view own history" ON public.prediction_history
    FOR SELECT USING (user_id = current_setting('app.current_user_id')::BIGINT);

CREATE POLICY "Users can insert history" ON public.prediction_history
    FOR INSERT WITH CHECK (user_id = current_setting('app.current_user_id')::BIGINT);
"""

    # Save SQL to file
    with open('supabase_django_migration.sql', 'w') as f:
        f.write(create_tables_sql)

    print("\n✓ SQL migration file created: supabase_django_migration.sql")

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("\n1. Go to Supabase Dashboard:")
    print("   https://supabase.com/dashboard/project/pmdrcyjklpcrdleiwkws/sql")
    print("\n2. Click 'New Query'")
    print("\n3. Copy contents of 'supabase_django_migration.sql'")
    print("\n4. Paste and click 'RUN'")
    print("\n5. Verify tables in Database > Tables")

    print("\n" + "=" * 70)

    return True

if __name__ == "__main__":
    create_tables_in_supabase()
