# Mini Hospital Management System (HMS)

A comprehensive hospital management web application for doctor availability management and patient appointment booking with Google Calendar integration and serverless email notifications.

## 🎯 Features

### Authentication & User Management
- **Role-based authentication** (Doctor/Patient)
- Secure password hashing
- Session-based authentication
- Separate registration flows for doctors and patients

### Doctor Features
- Personal dashboard with appointment overview
- Create and manage availability time slots
- View all appointments (past, present, future)
- Filter appointments by status
- Google Calendar integration
- Email notifications for new bookings

### Patient Features
- Personal dashboard with booking history
- Search and filter doctors by name/specialization
- View doctor profiles with detailed information
- Book available time slots
- Real-time slot availability
- Google Calendar integration
- Email confirmations for bookings
- Cancel bookings

### Core Functionality
- **Race condition prevention** using database-level locking
- **Google Calendar integration** - automatic event creation
- **Serverless email service** - AWS Lambda-style notifications
- **Slot management** - prevents double booking
- **Real-time availability** - only shows future, unbooked slots

## 🏗️ Architecture

### Technology Stack
- **Backend:** Django 4.2.7
- **Database:** PostgreSQL
- **Authentication:** Django built-in (session-based)
- **Calendar API:** Google Calendar API v3
- **Email Service:** Python serverless function (Serverless Framework)
- **Frontend:** Bootstrap 5, Django Templates

### Project Structure
```
hospital_management/
├── hms_project/                 # Main Django application
│   ├── accounts/                # User authentication
│   ├── doctors/                 # Doctor functionality
│   ├── patients/                # Patient functionality
│   ├── bookings/                # Booking system
│   ├── integrations/            # External services
│   └── templates/               # HTML templates
│
└── email_service/               # Serverless email function
    ├── handler.py               # Lambda function
    ├── serverless.yml           # Serverless config
    └── requirements.txt         # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Node.js 14+ (for serverless)
- Google Cloud account (for Calendar API)
- Gmail account (for email service)

### 1. Database Setup

```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Create database
sudo -u postgres psql
CREATE DATABASE hms_db;
CREATE USER hms_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE hms_db TO hms_user;
\q
```

### 2. Clone and Setup Django Project

```bash
# Create project directory
mkdir hospital_management && cd hospital_management

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Create Django project
django-admin startproject hms_project
cd hms_project

# Install dependencies
pip install Django psycopg2-binary python-decouple google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests pytz

# Create Django apps
python manage.py startapp accounts
python manage.py startapp doctors
python manage.py startapp patients
python manage.py startapp bookings
mkdir integrations
touch integrations/__init__.py
```

### 3. Configure Environment

Create `.env` file in `hms_project/`:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_NAME=hms_db
DATABASE_USER=hms_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Google Calendar API
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/oauth2callback

# Email Service
EMAIL_SERVICE_URL=http://localhost:3000/dev/send-email
```

### 4. Setup Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project
3. Enable **Google Calendar API**
4. Create OAuth 2.0 credentials:
   - Type: Web application
   - Authorized redirect URIs: `http://localhost:8000/oauth2callback`
5. Copy Client ID and Secret to `.env`

### 5. Copy Project Files

Copy all code from the artifacts into respective files:
- `settings.py` → `hms_project/settings.py`
- `models.py` files → respective app directories
- `views.py` files → respective app directories
- `forms.py` files → respective app directories
- `urls.py` files → respective app directories
- Template files → `templates/` directory
- Integration files → `integrations/` directory

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Optional
```

### 7. Setup Serverless Email Service

```bash
# Go to project root
cd ..
mkdir email_service && cd email_service

# Install Serverless Framework
npm install -g serverless
npm init -y
npm install --save-dev serverless-offline serverless-python-requirements

# Create files
touch handler.py serverless.yml .env
```

Create `email_service/.env`:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
FROM_EMAIL=your-email@gmail.com
```

**Gmail App Password Setup:**
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. App passwords → Generate new password
4. Use generated password in `.env`

Copy `handler.py` and `serverless.yml` from artifacts.

### 8. Start Services

**Terminal 1 - Django:**
```bash
cd hms_project
source venv/bin/activate
python manage.py runserver
```

**Terminal 2 - Email Service:**
```bash
cd email_service
serverless offline start
```

### 9. Access the Application

Open browser: `http://localhost:8000`

## 📖 Usage Guide

### For Doctors

1. **Sign Up**
   - Navigate to Doctor Sign Up
   - Fill in personal and professional details
   - Receive welcome email

2. **Set Availability**
   - Login and go to "Manage Availability"
   - Add time slots with date, start time, end time
   - Slots appear to patients immediately

3. **Connect Google Calendar**
   - Click "Connect Google Calendar"
   - Authorize the application
   - Appointments auto-sync to calendar

4. **Manage Appointments**
   - View today's appointments on dashboard
   - Filter by status (Pending/Confirmed/Cancelled)
   - Receive email notifications for new bookings

### For Patients

1. **Sign Up**
   - Navigate to Patient Sign Up
   - Fill in personal details
   - Receive welcome email

2. **Find Doctors**
   - Use "Find Doctors" page
   - Search by name or filter by specialization
   - View doctor profiles and ratings

3. **Book Appointment**
   - Select doctor → View available slots
   - Click "Book" on desired slot
   - Add optional notes
   - Receive confirmation email
   - Event added to Google Calendar (if connected)

4. **Manage Bookings**
   - View all bookings on "My Bookings"
   - Cancel if needed (frees up the slot)

## 🔒 Security Features

- **Password Hashing:** Django's built-in PBKDF2 algorithm
- **CSRF Protection:** Enabled for all forms
- **SQL Injection Prevention:** Django ORM parameterized queries
- **Session Security:** Secure cookie settings
- **Role-based Access Control:** Decorator-based authorization
- **Database Transactions:** ACID compliance for bookings

## 🎯 Key Implementation Highlights

### Race Condition Prevention

```python
@transaction.atomic
def create_booking(patient, doctor, availability_slot_id):
    # Lock row to prevent concurrent bookings
    slot = DoctorAvailability.objects.select_for_update().get(
        id=availability_slot_id
    )
    
    if slot.is_booked:
        raise ValidationError("Slot already booked")
    
    # Create booking
    booking = Booking.objects.create(...)
    slot.is_booked = True
    slot.save()
    
    return booking
```

### Google Calendar Integration

```python
def create_calendar_event(user, title, description, start_datetime, start_time, end_time):
    service = get_calendar_service(user)
    event = {
        'summary': title,
        'description': description,
        'start': {'dateTime': start_dt.isoformat()},
        'end': {'dateTime': end_dt.isoformat()},
    }
    return service.events().insert(calendarId='primary', body=event).execute()
```

### Serverless Email Function

```python
def send_email(event, context):
    body = json.loads(event['body'])
    action = body['action']  # SIGNUP_WELCOME or BOOKING_CONFIRMATION
    data = body['data']
    
    # Generate email content
    subject, html = generate_email_content(action, data)
    
    # Send via SMTP
    send_via_smtp(subject, html, data['to_email'])
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Doctor registration with email confirmation
- [ ] Patient registration with email confirmation
- [ ] Doctor can create availability slots
- [ ] Patient can view available slots
- [ ] Patient can book an appointment
- [ ] Email sent on booking
- [ ] Google Calendar event created
- [ ] Slot marked as booked after booking
- [ ] Race condition: Two patients can't book same slot
- [ ] Booking cancellation frees up slot
- [ ] Past slots don't appear as available

### Database Testing

```bash
# Django shell
python manage.py shell

from accounts.models import User
from bookings.models import Booking, DoctorAvailability

# Test queries
User.objects.filter(role='DOCTOR')
Booking.objects.filter(status='CONFIRMED')
DoctorAvailability.objects.filter(is_booked=False, date__gte=timezone.now().date())
```

## 🐛 Debugging

### Common Issues

**Database Connection Error:**
```bash
sudo systemctl status postgresql
psql -U hms_user -d hms_db -h localhost
```

**Email Not Sending:**
- Verify serverless offline is running on port 3000
- Check SMTP credentials
- Review terminal logs

**Google Calendar Error:**
- Verify OAuth credentials
- Check redirect URI matches exactly
- Ensure Calendar API is enabled in Google Cloud Console

**Import Errors:**
```bash
pip install -r requirements.txt
python manage.py migrate
```

## 📊 Database Schema

### Key Models

**User (Custom)**
- username, email, password (hashed)
- role (DOCTOR/PATIENT)
- google_calendar_token (JSON)

**DoctorProfile**
- OneToOne with User
- specialization, qualification, experience_years, consultation_fee

**PatientProfile**
- OneToOne with User
- date_of_birth, blood_group, address, emergency_contact

**DoctorAvailability**
- ForeignKey to Doctor
- date, start_time, end_time
- is_booked (Boolean)
- Unique constraint: (doctor, date, start_time)

**Booking**
- ForeignKey to Patient, Doctor
- OneToOne with DoctorAvailability
- status (PENDING/CONFIRMED/CANCELLED/COMPLETED)
- doctor_event_id, patient_event_id (Google Calendar)

## 🚢 Production Deployment

### Checklist

1. Set `DEBUG=False`
2. Configure `ALLOWED_HOSTS`
3. Use production database (AWS RDS, etc.)
4. Deploy serverless to AWS Lambda
5. Use AWS SES or SendGrid for emails
6. Enable HTTPS
7. Set up proper secret management
8. Configure CORS
9. Set up monitoring and logging
10. Enable backup strategy

### AWS Lambda Deployment

```bash
cd email_service
serverless deploy --stage prod
```

## 📝 Code Quality

- **Clean Code:** Clear naming, single responsibility
- **DRY Principle:** Reusable services and utilities
- **Documentation:** Comprehensive docstrings
- **Error Handling:** Try-catch blocks with logging
- **Validation:** Model-level and form-level
- **Optimization:** Database indexing, query optimization


## 📄 License

This project is created for educational purposes.

## 👨‍💻 Developer
