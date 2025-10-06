# MASTER PRD - PART 2 (EXPANDED SECTIONS)
## Sections 7.2 through 23 - Complete Details

**This file continues from MASTER_PRD_COMPLETE.md at line 1697**
**Append this content after Section 7.1 (Landing Page)**

---

## 7.2 Registration Page

### Purpose
- Allow new users to create accounts
- Collect essential information (name, email, phone, location)
- Enable email verification via Supabase

### Layout (Wireframe)

```
┌─────────────────────────────────────────────────────────────┐
│  [← Back to Home]                        CropSmart Logo      │
└─────────────────────────────────────────────────────────────┘

                    CREATE YOUR ACCOUNT

  ┌────────────────────────────────────────────┐
  │                                              │
  │  Full Name                                   │
  │  [____________________________________]      │
  │                                              │
  │  Email Address                               │
  │  [____________________________________]      │
  │  ✉️  We'll send a verification email        │
  │                                              │
  │  Phone Number                                │
  │  [+91] [_____________________________]       │
  │  📱 For SMS notifications (optional)        │
  │                                              │
  │  Password                                    │
  │  [____________________________________] [👁️]  │
  │  ℹ️  Min 8 characters, include numbers      │
  │  Password Strength: ████████░░ Strong       │
  │                                              │
  │  Confirm Password                            │
  │  [____________________________________]      │
  │                                              │
  │  State                                       │
  │  [Select State ▼]                            │
  │                                              │
  │  District                                    │
  │  [Select District ▼]                         │
  │                                              │
  │  ☑️ I agree to Terms & Privacy Policy       │
  │                                              │
  │  [      Sign Up      ]                       │
  │  (Green button, full width)                  │
  │                                              │
  │  Already have an account? Login              │
  └────────────────────────────────────────────┘
```

### Components

**Form Container**:
- Centered card (max-width: 500px)
- White background, medium shadow
- Padding: 32px
- Border-radius: 8px

**Input Fields**:
- Height: 48px
- Border: 1px solid #CCC
- Focus: 2px solid green border
- Error state: Red border + error icon
- Success state: Green border + checkmark icon

**Phone Input**:
- Country code selector dropdown (+91 India default)
- 10-digit validation
- Optional field (can skip for email-only registration)

**Password Field**:
- Toggle visibility icon (eye)
- Real-time strength indicator:
  - Weak (red): < 8 chars
  - Medium (yellow): 8+ chars
  - Strong (green): 8+ chars + numbers + special chars
- Confirmation field must match

**State/District Dropdowns**:
- Cascading: District options load based on State selection
- Data: Indian states and districts (can be hardcoded or from API)

**Submit Button**:
- Full width, 48px height
- Green background (#28a745), white text
- Loading spinner during submission
- Disabled until all required fields valid

### Validation Rules

| Field | Rules | Error Message |
|-------|-------|---------------|
| Full Name | Required, min 3 chars, letters only | "Name must be at least 3 characters" |
| Email | Required, valid email format | "Please enter a valid email" |
| Phone | Optional, 10 digits if provided | "Phone must be 10 digits" |
| Password | Min 8 chars, alphanumeric | "Password must be 8+ characters with numbers" |
| Confirm Password | Must match password | "Passwords do not match" |
| State | Required, from dropdown | "Please select your state" |
| District | Required, from dropdown | "Please select your district" |
| Terms checkbox | Must be checked | "You must agree to terms" |

### User Flow

1. User fills registration form
2. On submit:
   - Frontend validates all fields
   - If errors: Display inline error messages
   - If valid: Show loading spinner, disable button
3. Django view calls `supabase.auth.sign_up()`
4. Supabase creates user in `auth.users` table
5. Trigger auto-creates `user_profiles` record
6. Supabase sends verification email
7. Django shows success message: "Registration successful! Check your email to verify."
8. Redirect to login page after 3 seconds

### Edge Cases

- **Email already exists**: Show error "Email already registered. Try logging in."
- **Phone already exists**: Show warning "Phone number in use. Contact support if this is your number."
- **Network error**: Show error "Registration failed. Check your connection and try again."
- **Supabase down**: Queue registration, show "Registration pending. We'll email you when complete."

---

## 7.3 Login Page

### Purpose
- Authenticate existing users
- Redirect to dashboard on success
- Provide password reset option

### Layout (Wireframe)

```
┌─────────────────────────────────────────────────────────────┐
│  [← Back to Home]                        CropSmart Logo      │
└─────────────────────────────────────────────────────────────┘

                      WELCOME BACK
                   Login to continue

  ┌────────────────────────────────────────────┐
  │                                              │
  │  Email or Phone                              │
  │  [____________________________________]      │
  │                                              │
  │  Password                                    │
  │  [____________________________________] [👁️]  │
  │                                              │
  │  ☑️ Remember me        Forgot Password?     │
  │                                              │
  │  [      Login      ]                         │
  │  (Green button, full width)                  │
  │                                              │
  │  ── OR ──                                    │
  │                                              │
  │  [🔵 Continue with Google]                   │
  │  [⚫ Continue with GitHub]                   │
  │                                              │
  │  Don't have an account? Sign Up              │
  └────────────────────────────────────────────┘
```

### Components

**Email/Phone Input**:
- Accepts both email and phone number
- Placeholder: "Email or phone number"
- Auto-detects format (email vs phone)

**Password Input**:
- Type: password (toggle to text with eye icon)
- Placeholder: "Enter your password"

**Remember Me Checkbox**:
- Extends session to 7 days (vs 30 minutes default)
- Stores preference in localStorage

**Forgot Password Link**:
- Opens password reset modal
- User enters email → Supabase sends reset link

**Social Login Buttons**:
- Google: Blue (#4285F4)
- GitHub: Black (#24292E)
- Full width, 48px height
- Icons from respective brand guidelines

### User Flow

1. User enters email/phone + password
2. On submit:
   - Validate inputs (not empty)
   - Show loading spinner
3. Django calls `supabase.auth.sign_in_with_password()`
4. On success:
   - Store `access_token` in Django session
   - Store `user_id` in session
   - Redirect to dashboard
5. On failure:
   - Show error: "Invalid credentials. Please try again."
   - Increment failed login counter (lock after 5 attempts)

### Social Login Flow

1. User clicks "Continue with Google"
2. Redirect to Google OAuth consent screen
3. User approves → Google redirects to `/auth/callback`
4. Django exchanges code for token
5. Supabase creates/updates user
6. Redirect to dashboard

---

## 7.4 User Dashboard

### Purpose
- Welcome users, show personalized greeting
- Provide quick access to main features
- Display recent predictions summary

### Layout (Wireframe)

```
┌─────────────────────────────────────────────────────────────┐
│  CropSmart 🌾    [🏠 Home] [📊 History] [👤 Profile] [Logout]│
└─────────────────────────────────────────────────────────────┘

  Welcome back, Rajesh! 👋
  Your last prediction: Rice (2 days ago)

  QUICK ACTIONS
  ┌──────────────────────┐  ┌──────────────────────┐
  │  🌱 Predict Crop     │  │  🔬 Classify Soil    │
  │                      │  │                      │
  │  Get AI-powered      │  │  Upload soil image   │
  │  recommendations     │  │  for instant ID      │
  │                      │  │                      │
  │  [Start →]           │  │  [Start →]           │
  └──────────────────────┘  └──────────────────────┘

  RECENT PREDICTIONS
  ┌─────────────────────────────────────────────────────┐
  │ 📅 Oct 1, 2025                                      │
  │ Crop: Rice | Soil: Alluvial | Fertilizer: Urea     │
  │ Confidence: 92% ⭐⭐⭐⭐⭐                              │
  │ [View Details]                                      │
  ├─────────────────────────────────────────────────────┤
  │ 📅 Sep 28, 2025                                     │
  │ Crop: Maize | Soil: Black | Fertilizer: DAP        │
  │ Confidence: 87% ⭐⭐⭐⭐                               │
  │ [View Details]                                      │
  └─────────────────────────────────────────────────────┘

  TIPS & INSIGHTS
  ┌─────────────────────────────────────────────────────┐
  │ 💡 Did you know?                                    │
  │ Rice requires high humidity (80-90%) for optimal    │
  │ growth. Check weather forecasts before planting!    │
  └─────────────────────────────────────────────────────┘
```

### Components

**Top Navigation**:
- Logo + app name (left)
- Navigation links: Home, History, Profile (center/right)
- Logout button (far right)
- Active link: Green underline
- Mobile: Hamburger menu (collapse to drawer)

**Welcome Banner**:
- Personalized greeting with user's first name
- Last activity summary (last prediction date/crop)
- Light green background (#E8F5E9)
- Padding: 16px, border-radius: 8px

**Quick Action Cards**:
- 2 columns on desktop, stack on mobile
- Large icon (48px) at top
- Title (H4, bold)
- Description (body, gray)
- CTA button (green outline)
- Hover effect: Scale 1.02, shadow increase

**Recent Predictions**:
- Card-based list (max 5 items)
- Each card shows: Date, crop, soil, fertilizer, confidence
- Star rating visualization (5 stars, filled based on confidence)
- "View Details" button → redirects to prediction results page
- If no predictions: Show empty state with "Make your first prediction" CTA

**Tips Section**:
- Info box with light blue background (#E3F2FD)
- Bulb icon (yellow)
- Rotates daily (random tip from database)
- Examples:
  - Crop-specific tips
  - Seasonal advice
  - Fertilizer application best practices

### Data Sources

- User info: `SELECT * FROM user_profiles WHERE id = {user_id}`
- Recent predictions: `SELECT * FROM predictions WHERE user_id = {user_id} ORDER BY created_at DESC LIMIT 5`
- Tips: Hardcoded array or from database

---

## 7.5 Crop Prediction Form

### Purpose
- Collect 7 soil parameters from user
- Optional: Accept soil image upload
- Validate inputs before submission

### Layout (Wireframe)

```
┌─────────────────────────────────────────────────────────────┐
│  [← Dashboard]  Crop Prediction                              │
└─────────────────────────────────────────────────────────────┘

  ENTER SOIL PARAMETERS

  ┌────────────────────────────────────────────┐
  │                                              │
  │  Nitrogen (N) - kg/ha                        │
  │  [_________] [ℹ️ Range: 0-140]               │
  │                                              │
  │  Phosphorus (P) - kg/ha                      │
  │  [_________] [ℹ️ Range: 5-145]               │
  │                                              │
  │  Potassium (K) - kg/ha                       │
  │  [_________] [ℹ️ Range: 5-205]               │
  │                                              │
  │  Temperature - °C                            │
  │  [_________] [ℹ️ Range: 8-43]                │
  │                                              │
  │  Humidity - %                                │
  │  [_________] [ℹ️ Range: 14-100]              │
  │                                              │
  │  pH Level                                    │
  │  [_________] [ℹ️ Range: 3.5-9.5]             │
  │                                              │
  │  Rainfall - mm                               │
  │  [_________] [ℹ️ Range: 20-300]              │
  │                                              │
  │  Optional: Upload Soil Image                 │
  │  ┌──────────────────────────────────┐       │
  │  │  📷 Click to upload or drag here │       │
  │  │  JPG, PNG - Max 5MB              │       │
  │  └──────────────────────────────────┘       │
  │                                              │
  │  [Save Template] [Clear Form] [Predict Crop→]│
  │                                    (Green)   │
  └────────────────────────────────────────────┘

  NEED HELP?
  📖 How to measure soil parameters | 🎥 Watch tutorial
```

### Components

**Form Fields**:
- Type: `number` with `step="0.01"`
- Width: Full width on mobile, 48% on desktop (2 columns)
- Height: 48px
- Validation: HTML5 `min`, `max` attributes

**Info Icons**:
- Tooltip on hover (Bootstrap tooltip)
- Shows acceptable range
- Click on mobile: Show modal with detailed explanation

**Input Validation** (Real-time):
```javascript
// On blur or change
if (value < min || value > max) {
  input.classList.add('is-invalid');
  showError('Value out of range');
} else if (value === '') {
  input.classList.add('is-invalid');
  showError('This field is required');
} else {
  input.classList.add('is-valid');
  hideError();
}
```

**Image Upload**:
- Drag-and-drop zone (200px height)
- Dashed border (#CCC), green on hover/drag
- Preview thumbnail after upload (150x150px)
- "Remove" button (X icon) on preview
- File validation:
  - Format: Only JPG, PNG
  - Size: Max 5MB
  - Reject if invalid: Show error toast

**Buttons**:
- **Save Template**: Save values to localStorage (reuse later)
- **Clear Form**: Reset all fields to empty
- **Predict Crop**: Primary CTA (disabled if form incomplete)

### Validation Rules

| Field | Min | Max | Validation |
|-------|-----|-----|------------|
| Nitrogen | 0 | 140 | Required, decimal allowed |
| Phosphorus | 5 | 145 | Required, decimal allowed |
| Potassium | 5 | 205 | Required, decimal allowed |
| Temperature | 8 | 43 | Required, decimal allowed |
| Humidity | 14 | 100 | Required, decimal allowed |
| pH | 3.5 | 9.5 | Required, 1 decimal place |
| Rainfall | 20 | 300 | Required, decimal allowed |
| Soil Image | - | 5MB | Optional, JPG/PNG only |

### User Flow

1. User enters all 7 parameters
2. Optionally uploads soil image
3. Real-time validation on each field
4. "Predict Crop" button:
   - Disabled if any required field invalid
   - Enabled when all fields valid
5. On submit:
   - Show loading overlay with spinner
   - Message: "Analyzing soil parameters..."
   - If image: "Classifying soil image..."
6. Submit form to `/predictions/create/` endpoint
7. Django processes:
   - Validates inputs
   - If image: Upload to Supabase Storage
   - If image: Run soil classification
   - Run crop prediction
   - Save to database
8. Redirect to results page

### Help Resources

**"How to measure soil parameters"** link:
- Opens modal with instructions
- Content:
  - Nitrogen: Use soil testing kit or lab
  - Phosphorus: Soil test (Olsen method)
  - Potassium: Soil test (Ammonium acetate method)
  - Temperature: Average temperature during growing season
  - Humidity: Average relative humidity
  - pH: pH meter or testing kit
  - Rainfall: Annual rainfall data (mm)
- Links to buy soil testing kits (affiliate optional)

**"Watch tutorial"** link:
- Embedded YouTube video (5 minutes)
- Shows farmer measuring each parameter
- Subtitles in local languages

---

## 7.6 Prediction Results Page

### Purpose
- Display top 3 crop recommendations with confidence scores
- Show fertilizer recommendations for each crop
- Display soil classification results (if image uploaded)
- Provide actions: Save, Download PDF, Share

### Layout (Wireframe)

```
┌─────────────────────────────────────────────────────────────┐
│  [← New Prediction]  Results                                 │
└─────────────────────────────────────────────────────────────┘

  ✅ PREDICTION COMPLETE!

  TOP RECOMMENDED CROPS

  ┌─────────────────────────────────────────────────────┐
  │  🥇 #1 RICE                                          │
  │                                                       │
  │  Confidence: ████████████████████░░ 92%              │
  │                                                       │
  │  Why this crop?                                      │
  │  • Ideal nitrogen levels (90 kg/ha)                  │
  │  • High humidity (85%) perfect for rice              │
  │  • Suitable pH (6.5) and rainfall (200mm)            │
  │                                                       │
  │  Recommended Fertilizer: Urea                        │
  │  Dosage: 120 kg/ha                                   │
  │  Application: Split doses (50% at planting,          │
  │               30% at tillering, 20% at flowering)    │
  │                                                       │
  │  Estimated Cost: ₹3,000/acre                         │
  │                                                       │
  │  [Learn More About Rice]                             │
  └─────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────┐
  │  🥈 #2 MAIZE                                         │
  │  Confidence: ████████████████░░░░ 78%               │
  │  Fertilizer: DAP | [View Details ▼]                 │
  └─────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────┐
  │  🥉 #3 COTTON                                        │
  │  Confidence: ██████████████░░░░░░ 72%               │
  │  Fertilizer: Urea | [View Details ▼]                │
  └─────────────────────────────────────────────────────┘

  SOIL CLASSIFICATION (If image uploaded)
  ┌─────────────────────────────────────────────────────┐
  │  Detected Soil Type: Alluvial Soil                   │
  │  Confidence: 89%                                     │
  │                                                       │
  │  [Your Image]        [Reference Image]               │
  │  [150x150px]         [150x150px]                     │
  │                                                       │
  │  Characteristics: High fertility, good drainage      │
  └─────────────────────────────────────────────────────┘

  ACTIONS
  [Save to History] [Download PDF] [Share] [New Prediction]

  📌 DISCLAIMER: Recommendations are based on historical data.
  Consult local agricultural experts for best results.
```

### Components

**Success Banner**:
- Green checkmark icon (48px)
- "Prediction Complete!" message (H2)
- Light green background (#E8F5E9)
- Full width, padding: 24px

**Top Recommendation Card (#1)**:
- Always expanded (full details visible)
- Medal icon: 🥇 (gold)
- Crop name: H2, bold, dark gray
- **Confidence Bar**:
  - Animated progress bar (0% → final% on load)
  - Color: Green if >80%, Yellow if 60-80%, Red if <60%
  - Percentage displayed on right
- **"Why this crop?" section**:
  - Bullet list (3-5 points)
  - Explain which parameters favor this crop
- **Fertilizer Details**:
  - Name (bold)
  - Dosage (kg/ha)
  - Application timing (split doses, growth stages)
  - Estimated cost (₹/acre)
- **"Learn More" button**:
  - Opens modal with crop details
  - Content: Ideal conditions, growing tips, market prices

**Alternative Recommendations (#2, #3)**:
- Collapsed by default (summary view)
- Medal icons: 🥈 (silver), 🥉 (bronze)
- Show: Crop name, confidence bar, fertilizer name
- **"View Details" accordion**:
  - Click to expand (smooth animation)
  - Shows same details as #1 when expanded

**Soil Classification Card**:
- Only displayed if image was uploaded
- **Side-by-side images**:
  - Left: User's uploaded image (150x150px)
  - Right: Reference image from database (150x150px)
  - Click to zoom (modal with full-size images)
- **Soil Type**:
  - Name (H3, bold)
  - Confidence percentage
  - Color-coded badge (Alluvial: Green, Black: Dark, Clay: Brown, Red: Red)
- **Characteristics**:
  - Bullet list of soil properties
  - Best crops for this soil type

**Action Buttons**:
- **Save to History**: Already auto-saved, this just confirms with toast
- **Download PDF**: Generate PDF report with all details
  - Library: ReportLab (Python)
  - Content: Input parameters, predictions, fertilizer recommendations, soil classification
  - File name: `prediction_{date}_{user_id}.pdf`
- **Share**: Copy shareable link to clipboard
  - URL: `/predictions/{prediction_id}/public/`
  - Public view (no login required)
  - Toast: "Link copied to clipboard!"
- **New Prediction**: Redirect to prediction form (clear previous inputs)

**Disclaimer**:
- Small text, light gray
- Info icon
- Background: Light yellow (#FFF9E6)
- Border-left: 4px solid warning yellow

### Interactions

**Confidence Bar Animation**:
```javascript
// On page load
animateProgressBar(0, finalConfidence, 1000); // 1 second
```

**Accordion Expand/Collapse**:
```javascript
// Click "View Details"
accordion.addEventListener('click', () => {
  content.classList.toggle('expanded');
  // Smooth height transition (CSS)
});
```

**Download PDF**:
```python
# Django view
from reportlab.pdfgen import canvas

def download_pdf(request, prediction_id):
    # Fetch prediction data
    prediction = supabase.table('predictions').select('*').eq('id', prediction_id).execute()

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="prediction_{prediction_id}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "CropSmart - Prediction Report")
    # ... add all prediction details
    p.showPage()
    p.save()

    return response
```

---

## 7.7 Prediction History Page

### Purpose
- Display all past predictions for logged-in user
- Filter by date range, crop type
- Provide user feedback form (did you plant? actual yield?)
- Export options (CSV, PDF)

### Layout (Wireframe)

```
┌─────────────────────────────────────────────────────────────┐
│  [← Dashboard]  Prediction History                           │
└─────────────────────────────────────────────────────────────┘

  FILTERS
  [Date Range: Last 30 days ▼] [Crop: All ▼] [Apply Filters]

  📊 Total Predictions: 24 | Success Rate: 85%

  ┌─────────────────────────────────────────────────────┐
  │ Oct 1, 2025 | 10:30 AM                               │
  │ ──────────────────────────────────────────────       │
  │ Predicted: Rice (92% confidence)                     │
  │ Soil: Alluvial | Fertilizer: Urea                    │
  │                                                       │
  │ Did you plant this? [Yes] [No]                       │
  │ Actual yield: [___] quintals/acre (optional)         │
  │                                                       │
  │ [View Full Details] [Download PDF]                   │
  └─────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────┐
  │ Sep 28, 2025 | 3:15 PM                               │
  │ ──────────────────────────────────────────────       │
  │ Predicted: Maize (87% confidence)                    │
  │ Soil: Black | Fertilizer: DAP                        │
  │                                                       │
  │ ✅ Planted | Actual yield: 18 quintals/acre          │
  │ 📈 +12% vs expected (system was accurate!)           │
  │                                                       │
  │ [View Full Details] [Download PDF]                   │
  └─────────────────────────────────────────────────────┘

  [Load More...]

  EXPORT OPTIONS
  [Download All as CSV] [Email Report]
```

### Components

**Filters Bar**:
- **Date Range Picker**:
  - Dropdown with presets: Last 7 days, Last 30 days, Last 3 months, Custom
  - Custom: Opens date picker modal (start date, end date)
- **Crop Type Filter**:
  - Multi-select dropdown
  - Options: All (default), Rice, Maize, Cotton, ... (22 crops)
- **Apply Filters Button**:
  - Green, reloads page with query parameters
  - URL: `/history/?date_range=30&crops=rice,maize`

**Summary Stats**:
- **Total Predictions**: Count from database
- **Success Rate**:
  - Formula: (Predictions where user_planted=True AND actual_yield > 0) / Total Predictions with feedback
  - Display: Percentage with icon
  - Color: Green if >70%, Yellow if 50-70%, Red if <50%

**Prediction Cards** (List):
- **Date/Time**: Format: "Oct 1, 2025 | 10:30 AM"
- **Predicted Crop**: Bold, with confidence in parentheses
- **Soil Type & Fertilizer**: Gray text, pipe-separated
- **Feedback Section**:
  - If no feedback:
    - "Did you plant this?" → Yes/No buttons
    - If Yes clicked: Show input for actual yield
    - On submit: Update database, show success toast
  - If feedback provided:
    - ✅ "Planted" badge (green)
    - Actual yield displayed
    - Comparison: System predicted vs actual (show % difference)
    - Accuracy indicator: 📈 (accurate) or 📉 (inaccurate)
- **Actions**:
  - "View Full Details" → Redirect to results page
  - "Download PDF" → Generate PDF for this prediction

**Pagination**:
- **Load More Button**:
  - Initially show 10 predictions
  - Click to load next 10 (AJAX)
  - Infinite scroll (alternative)
- **Scroll to Top Button**:
  - Appears when scrolled > 300px
  - Click to smooth scroll to top

**Export Options**:
- **Download All as CSV**:
  - Generates CSV file with columns: Date, Crop, Confidence, Soil Type, Fertilizer, Planted, Yield
  - Django view:
    ```python
    import csv

    def export_csv(request):
        predictions = fetch_user_predictions(request.user.id)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="predictions.csv"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Crop', 'Confidence', 'Soil Type', 'Fertilizer', 'Planted', 'Yield'])

        for p in predictions:
            writer.writerow([p.created_at, p.top_crop, p.top_confidence, p.soil_type, p.fertilizer, p.user_planted, p.actual_yield])

        return response
    ```

- **Email Report**:
  - Opens modal: "Email prediction report to {user_email}?"
  - Options: Weekly summary, Monthly summary
  - On confirm: Queue email (background task)

### User Flow - Feedback

1. User clicks "Yes" on "Did you plant this?"
2. Update database: `user_planted = True`
3. Show input field: "Actual yield (quintals/acre)"
4. User enters yield (e.g., 18.5)
5. On blur or submit:
   - Update database: `actual_yield = 18.5`
   - Calculate accuracy: Compare with expected yield (from ML model)
   - Show success toast: "Thank you for your feedback!"
   - Reload card to show feedback

---

## 7.8 Admin Dashboard

### Purpose
- System overview for administrators
- Quick access to dataset & model management
- Monitor system health and usage

### Layout (Wireframe)

```
┌─────────────────────────────────────────────────────────────┐
│  CropSmart Admin  [📊 Dashboard] [📁 Datasets] [🤖 Models]  │
│                   [👥 Users] [⚙️ Settings] [Logout]          │
└─────────────────────────────────────────────────────────────┘

  SYSTEM OVERVIEW

  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │ 👥 10,234    │ │ 📊 45,672    │ │ ✅ 99.5%     │
  │ Total Users  │ │ Predictions  │ │ Uptime       │
  └──────────────┘ └──────────────┘ └──────────────┘

  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │ 🎯 84.2%     │ │ 🌱 Rice      │ │ ⏱️ 2.1s      │
  │ MLP Accuracy │ │ Top Crop     │ │ Avg Response │
  └──────────────┘ └──────────────┘ └──────────────┘

  RECENT ACTIVITY
  ┌─────────────────────────────────────────────────────┐
  │ • User "farmer123" created prediction (2 min ago)   │
  │ • Model "MLP_v1.3" deployed (1 hour ago)            │
  │ • Dataset "crops_2025_Q3" uploaded (3 hours ago)    │
  └─────────────────────────────────────────────────────┘

  QUICK ACTIONS
  [Upload Dataset] [Train Model] [View Logs]
```

### Components

**Admin Navigation**:
- Horizontal tabs (brown color scheme vs green for users)
- Icons for each section
- Active tab: Underline + darker background
- Logout button on far right

**Metric Cards** (6 total):
- Grid layout: 3 columns on desktop, 2 on tablet, 1 on mobile
- Each card:
  - Large number (H1, 48px, bold)
  - Label below (body, gray)
  - Icon (48px, top-left)
  - Background: White, shadow on hover
  - Animation: Count up on page load

**Metrics**:
1. **Total Users**: `SELECT COUNT(*) FROM auth.users`
2. **Predictions**: `SELECT COUNT(*) FROM predictions`
3. **Uptime**: Calculate from deployment time (e.g., 99.5%)
4. **MLP Accuracy**: Fetch from latest deployed model
5. **Top Crop**: `SELECT top_crop, COUNT(*) as count FROM predictions GROUP BY top_crop ORDER BY count DESC LIMIT 1`
6. **Avg Response Time**: Average `processing_time_ms` from last 1000 predictions

**Activity Feed**:
- Real-time updates (WebSocket or AJAX polling every 30 seconds)
- List of recent actions:
  - User registrations
  - Predictions created
  - Datasets uploaded
  - Models trained/deployed
  - Admin actions (from `admin_activity_log`)
- Color-coded dots:
  - Green: Success (prediction created, model deployed)
  - Blue: Info (user registered)
  - Yellow: Warning (model training started)
  - Red: Error (training failed)
- Timestamp: Relative time (e.g., "2 min ago", "1 hour ago")

**Quick Action Buttons**:
- Large buttons (60px height)
- Icons + text
- Navigate to:
  - Upload Dataset → `/admin/datasets/upload/`
  - Train Model → `/admin/models/train/`
  - View Logs → `/admin/logs/`

---

## 7.9 Admin - Dataset Upload

### Purpose
- Allow admins to upload training datasets
- Validate dataset schema and preview data
- Store in Supabase Storage with metadata

### Layout (Wireframe)

```
┌─────────────────────────────────────────────────────────────┐
│  [← Admin Dashboard]  Dataset Upload                         │
└─────────────────────────────────────────────────────────────┘

  UPLOAD NEW DATASET

  ┌────────────────────────────────────────────┐
  │                                              │
  │  Dataset Type: (•) Crop Data  ( ) Soil Images│
  │                                              │
  │  Dataset Name: [____________________]        │
  │                                              │
  │  Version: [____] (e.g., 1.0, 2.1)            │
  │                                              │
  │  Upload File:                                │
  │  ┌──────────────────────────────────┐       │
  │  │  📁 Drag & drop CSV or ZIP       │       │
  │  │  (Max 500MB)                     │       │
  │  └──────────────────────────────────┘       │
  │                                              │
  │  [Cancel]  [Upload & Validate]               │
  └────────────────────────────────────────────┘

  EXISTING DATASETS

  Table (sortable columns):
  ┌─────┬───────────────┬────────┬──────┬────────┬────────┐
  │ ID  │ Name          │ Type   │ Ver  │ Samples│ Status │
  ├─────┼───────────────┼────────┼──────┼────────┼────────┤
  │ 001 │ crops_2025_Q3 │ Crop   │ 1.2  │ 2,200  │ Active │
  │     │               │        │      │        │[View]  │
  ├─────┼───────────────┼────────┼──────┼────────┼────────┤
  │ 002 │ soil_images   │ Soil   │ 2.0  │ 13,520 │ Active │
  │     │               │        │      │        │[View]  │
  ├─────┼───────────────┼────────┼──────┼────────┼────────┤
  │ 003 │ crops_2024_Q4 │ Crop   │ 1.1  │ 1,800  │Archived│
  │     │               │        │      │        │[Delete]│
  └─────┴───────────────┴────────┴──────┴────────┴────────┘
```

### Upload Flow

1. **Select Type**: Crop Data (CSV) or Soil Images (ZIP)
2. **Enter Metadata**: Name, Version
3. **Upload File**:
   - Drag-and-drop or click to browse
   - Show file name, size, format
   - Validate:
     - Crop Data: Must be CSV
     - Soil Images: Must be ZIP
     - Size: Max 500MB
4. **Click "Upload & Validate"**:
   - Show loading spinner
   - Upload to Supabase Storage
   - Validate schema

### Validation (Crop Data CSV)

**Expected Schema**:
```
Columns: N, P, K, temperature, humidity, ph, rainfall, label
Rows: 100+ samples per crop (2200+ total)
```

**Validation Checks**:
- ✅ All required columns present
- ✅ No missing values (or <5% missing)
- ✅ Data types correct (numeric for features, string for label)
- ✅ Value ranges:
  - N: 0-140
  - P: 5-145
  - K: 5-205
  - Temperature: 8-43
  - Humidity: 14-100
  - pH: 3.5-9.5
  - Rainfall: 20-300
- ✅ At least 50 samples per crop class
- ✅ 22 unique crop labels

**Validation Report** (saved to database):
```json
{
  "schema_check": "passed",
  "missing_values": {"N": 0, "P": 2, "K": 0, ...},
  "outliers": {"N": 5, "temperature": 1},
  "class_distribution": {"rice": 100, "maize": 98, ...},
  "recommendations": [
    "2 missing values in Phosphorus column - will be imputed with median",
    "5 outliers in Nitrogen (beyond 3 std dev) - review or remove"
  ]
}
```

**Preview**:
- Show first 10 rows in table format
- Summary statistics (mean, std, min, max) for each column
- Class distribution bar chart

5. **Admin Reviews**:
   - If validation passed: Click "Activate" → status = 'active'
   - If issues found: Click "Edit" or "Delete"

### Validation (Soil Images ZIP)

**Expected Structure**:
```
soil_images.zip
├── Alluvial/
│   ├── img001.jpg
│   ├── img002.jpg
│   └── ... (3000+ images)
├── Black/
│   └── ...
├── Clay/
│   └── ...
└── Red/
    └── ...
```

**Validation Checks**:
- ✅ ZIP contains exactly 4 folders (Alluvial, Black, Clay, Red)
- ✅ Each folder has 100+ images
- ✅ All images are JPG or PNG
- ✅ Image dimensions >= 224x224 pixels
- ✅ File sizes reasonable (10KB - 5MB each)

**Preview**:
- Show 5 random images from each class (grid layout)
- Summary: Total images, images per class, average file size

---

## 7.10 Admin - Model Training

### Purpose
- Train ML models on uploaded datasets
- Monitor training progress in real-time
- Evaluate model performance before deployment

### Layout (Wireframe)

```
┌─────────────────────────────────────────────────────────────┐
│  [← Admin Dashboard]  Model Training                         │
└─────────────────────────────────────────────────────────────┘

  TRAIN NEW MODEL

  ┌────────────────────────────────────────────┐
  │                                              │
  │  Model Type: (•) Crop Predictor (MLP)       │
  │              ( ) Soil Classifier (CNN)       │
  │                                              │
  │  Select Dataset: [crops_2025_Q3 ▼]          │
  │                                              │
  │  Hyperparameters:                            │
  │  Epochs: [10]  Batch Size: [32]             │
  │  Learning Rate: [0.001]                      │
  │  Test Split: [20%]                           │
  │                                              │
  │  [Start Training]                            │
  └────────────────────────────────────────────┘

  TRAINING PROGRESS (When active)
  ┌─────────────────────────────────────────────────────┐
  │  Model: MLP_v1.4 | Status: Training...              │
  │                                                       │
  │  Epoch 7/10                                          │
  │  Progress: ████████████████░░░░░░░░░ 70%            │
  │                                                       │
  │  Current Accuracy: 82.3% | Loss: 0.45               │
  │                                                       │
  │  📊 Live Chart: Accuracy & Loss over Epochs         │
  │  [Line chart showing upward accuracy trend]          │
  │                                                       │
  │  Estimated Time Remaining: 8 minutes                 │
  │                                                       │
  │  [Cancel Training]                                   │
  └─────────────────────────────────────────────────────┘

  TRAINED MODELS

  ┌─────┬───────────┬──────┬──────────┬────────┬──────────┐
  │ ID  │ Name      │ Type │ Accuracy │ Status │ Actions  │
  ├─────┼───────────┼──────┼──────────┼────────┼──────────┤
  │ 101 │ MLP_v1.3  │ MLP  │ 84.2%    │ Live   │[Evaluate]│
  │     │           │      │          │ 🟢     │[Rollback]│
  ├─────┼───────────┼──────┼──────────┼────────┼──────────┤
  │ 102 │ CNN_v2.1  │ CNN  │ 88.5%    │ Live   │[Evaluate]│
  │     │           │      │          │ 🟢     │          │
  ├─────┼───────────┼──────┼──────────┼────────┼──────────┤
  │ 103 │ MLP_v1.2  │ MLP  │ 81.7%    │Archived│[Deploy]  │
  │     │           │      │          │        │[Delete]  │
  └─────┴───────────┴──────┴──────────┴────────┴──────────┘
```

### Training Flow (Crop Predictor - XGBoost)

1. **Admin selects**:
   - Model Type: Crop Predictor
   - Dataset: crops_2025_Q3 (version 1.2)
   - Hyperparameters:
     - Epochs: 10 (actually rounds for XGBoost)
     - Batch size: N/A (XGBoost trains on full dataset)
     - Learning rate: 0.1 (eta)
     - Test split: 20%

2. **Click "Start Training"**:
   - Django view calls background task (Celery or threading)
   - Background task:

```python
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import time

def train_crop_predictor(dataset_id, hyperparameters):
    # 1. Download dataset from Supabase Storage
    dataset = supabase.table('datasets').select('*').eq('id', dataset_id).execute()
    file_url = dataset.data[0]['file_url']
    local_path = download_file(file_url, '/tmp/dataset.csv')

    # 2. Load data
    df = pd.read_csv(local_path)

    # 3. Preprocess
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # 4. Train XGBoost
    start_time = time.time()

    model = xgb.XGBClassifier(
        n_estimators=hyperparameters['epochs'] * 10,  # 10 rounds per "epoch"
        max_depth=6,
        learning_rate=hyperparameters['learning_rate'],
        objective='multi:softmax',
        num_class=22,
        random_state=42,
        eval_metric='mlogloss'
    )

    # Train with progress callback
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=True,
        callbacks=[
            lambda env: update_training_progress(env.iteration, env.evaluation_result_list)
        ]
    )

    training_duration = time.time() - start_time

    # 5. Evaluate
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)

    # 6. Save model
    model_filename = f"crop_predictor_v{next_version}.pkl"
    joblib.dump({
        'model': model,
        'scaler': scaler,
        'label_encoder': label_encoder
    }, f'/tmp/{model_filename}')

    # 7. Upload to Supabase Storage
    with open(f'/tmp/{model_filename}', 'rb') as f:
        supabase.storage.from_('ml-models').upload(
            f'crop_predictor/{model_filename}',
            f.read()
        )

    # 8. Save metadata to database
    model_url = f"{settings.SUPABASE_URL}/storage/v1/object/ml-models/crop_predictor/{model_filename}"

    supabase.table('ml_models').insert({
        'name': f'crop_predictor_v{next_version}',
        'type': 'crop_predictor',
        'framework': 'xgboost',
        'version': str(next_version),
        'dataset_id': dataset_id,
        'model_file_url': model_url,
        'model_size_mb': os.path.getsize(f'/tmp/{model_filename}') / (1024 * 1024),
        'hyperparameters': hyperparameters,
        'training_metrics': {
            'accuracy': accuracy,
            'loss': report['weighted avg']['loss'] if 'loss' in report['weighted avg'] else None
        },
        'evaluation_metrics': report,
        'confusion_matrix': cm.tolist(),
        'is_deployed': False,
        'trained_by': admin_user_id,
        'training_duration_seconds': int(training_duration)
    }).execute()

    return {'accuracy': accuracy, 'model_id': ...}
```

3. **Real-time Progress Updates**:
   - WebSocket or AJAX polling (every 2 seconds)
   - Display:
     - Current epoch (e.g., "Epoch 7/10")
     - Progress bar (70%)
     - Current accuracy & loss
     - Live chart (Chart.js line chart, updates per epoch)
     - Estimated time remaining

4. **Training Complete**:
   - Show success modal: "Training complete! Accuracy: 84.2%"
   - Display evaluation metrics:
     - Accuracy, Precision, Recall, F1-Score
     - Confusion matrix (heatmap)
     - Per-class accuracy table
   - Actions:
     - **Deploy Model**: Set is_deployed=True, download to Django
     - **Discard**: Delete model
     - **View Details**: Open evaluation page

### Evaluation Page

**URL**: `/admin/models/{model_id}/evaluate/`

**Content**:
- Model name, version, type, framework
- Training hyperparameters
- Training duration
- Dataset used

**Metrics**:
- Overall accuracy (large display)
- Precision, Recall, F1-Score (weighted average)
- Per-class performance table:

| Crop | Precision | Recall | F1-Score | Support |
|------|-----------|--------|----------|---------|
| Rice | 0.95 | 0.92 | 0.93 | 20 |
| Maize | 0.89 | 0.87 | 0.88 | 18 |
| ... | ... | ... | ... | ... |

**Confusion Matrix**:
- Heatmap (Plotly or matplotlib → base64 image)
- Rows: True labels
- Columns: Predicted labels
- Color: Green (correct), Red (incorrect)

**Deployment Decision**:
- If accuracy >= 80%: Show "Deploy Model" button (green)
- If accuracy < 80%: Show warning "Accuracy below threshold. Consider retraining with different hyperparameters."

---

*[Continuing with remaining sections...]*

Due to the massive length, I'll create this as a comprehensive continuation document. Would you like me to:

1. **Continue creating the full expansion** (will be 100+ more pages covering sections 8-23 in detail)
2. **Create a summary version** of sections 8-23 (20-30 pages, key points only)
3. **Focus on specific sections** you need most (e.g., ML Specifications, Code Examples, Testing)

Which approach would you prefer?