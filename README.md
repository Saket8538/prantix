# PrantiX - Online Learning Platform

![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Created](https://img.shields.io/badge/Created-October%202025-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## 📚 Overview

**PrantiX** is a comprehensive, modern online learning platform built with **Django** that enables educators and learners to create, manage, and access high-quality courses. The platform features an intuitive user interface, flexible payment processing, coupon management, and secure course access control.

**Live Site:** https://prantix.live

### Key Features
- 🎓 **Course Management** - Create and manage comprehensive online courses
- 💳 **Multiple Payment Methods** - Razorpay integration for online payments, manual payment verification
- 🎫 **Coupon System** - Flexible percentage and fixed discount coupons with time-based validity
- 👥 **User Management** - Registration, login, and role-based access control
- 📹 **Video Content** - Integrated video lectures with preview and enrollment-based access
- 📧 **Email Notifications** - Automated payment confirmations and course enrollment emails
- 📱 **Responsive Design** - Mobile-first, Bootstrap 5-based modern UI
- ☁️ **Cloud Deployment** - Azure App Service deployment ready
- 🔐 **Security** - CSRF protection, secure payments, SSL/TLS support

---

## 🏗️ Project Architecture

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 4.2 |
| **Database** | SQLite (Development) / PostgreSQL (Production - Azure) |
| **Web Server** | Gunicorn |
| **Frontend** | HTML5, Bootstrap 5, JavaScript |
| **Payment Gateway** | Razorpay |
| **Cloud Platform** | Microsoft Azure App Service |
| **Static File Serving** | WhiteNoise |
| **Email Service** | SMTP (Gmail/Office365 compatible) |

### Project Structure

```
prantix/
├── prantix/                      # Main project configuration
│   ├── settings.py              # Django settings for development
│   ├── deployment.py            # Azure deployment-specific settings
│   ├── urls.py                  # Root URL routing
│   ├── wsgi.py                  # WSGI application entry point
│   └── asgi.py                  # ASGI application entry point
│
├── courses/                      # Main application
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── course.py           # Course model and properties
│   │   ├── video.py            # Video model
│   │   ├── user_course.py      # User enrollment model
│   │   ├── payment.py          # Payment records
│   │   └── manual_payment.py   # Manual payment verification
│   │
│   ├── views/                  # View logic
│   │   ├── __init__.py
│   │   ├── homepage.py         # Landing page view
│   │   ├── auth.py             # Authentication views (login, signup, logout)
│   │   ├── courses.py          # Course listing and course page views
│   │   ├── checkout.py         # Payment checkout logic
│   │   ├── manual_payment.py   # Manual payment form and validation
│   │   └── newsletter.py       # Newsletter subscription
│   │
│   ├── static/                 # Static files
│   │   ├── courses/
│   │   │   ├── css/           # Stylesheets
│   │   │   └── js/
│   │   │       └── modern-ui.js  # Interactive UI enhancements
│   │
│   ├── templates/              # HTML templates
│   │   ├── courses/
│   │   │   ├── base.html       # Base template with navbar/footer
│   │   │   ├── homepage.html   # Landing page
│   │   │   ├── signup.html     # Registration form
│   │   │   ├── login.html      # Login form
│   │   │   ├── courses_list.html    # All courses listing
│   │   │   ├── course_page.html     # Individual course with video
│   │   │   ├── my_courses.html      # Student's enrolled courses
│   │   │   ├── payment_page.html    # Payment form with coupon support
│   │   │   ├── checkout.html        # Razorpay checkout
│   │   │   └── static_pages/
│   │   │       ├── about.html
│   │   │       ├── careers.html
│   │   │       ├── privacy.html
│   │   │       └── terms.html
│   │   └── emails/             # Email templates
│   │       ├── newsletter_welcome.html
│   │       ├── user_payment_confirmed.html
│   │       ├── user_payment_rejected.html
│   │       ├── user_payment_submitted.html
│   │       └── admin_payment_notification.html
│   │
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   └── email_utils.py      # Email sending utilities
│   │
│   ├── admin.py                # Django admin customization
│   ├── apps.py                 # App configuration
│   ├── urls.py                 # App URL routing
│   └── forms.py                # Django forms
│
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management script
├── startup.sh                   # Azure App Service startup script
└── README.md                    # This file

```

---

## 🗄️ Database Models

### Core Models

#### **Course**
Main model for course information and metadata.

```python
- name (CharField): Course title
- slug (CharField): URL-friendly identifier [UNIQUE]
- description (CharField): Short course description
- price (IntegerField): Course price in rupees
- discount (IntegerField): Discount percentage (0-100)
- active (BooleanField): Course visibility status
- thumbnail (ImageField): Course cover image
- resource (FileField): Course resource file
- length (IntegerField): Course duration in minutes
- date (DateTimeField): Creation timestamp
```

**Related Models:**
- `Tag` - Course tags/categories
- `Prerequisite` - Course prerequisites
- `Learning` - Learning outcomes
- `Video` - Lecture videos

#### **Video**
Video lectures within a course.

```python
- title (CharField): Video title
- course (ForeignKey): Parent course
- serial_number (IntegerField): Lecture sequence number
- video_id (CharField): YouTube/Platform video ID
- is_preview (BooleanField): Preview availability
```

#### **UserCourse**
Tracks user enrollments in courses.

```python
- user (ForeignKey): Student user
- course (ForeignKey): Enrolled course
- date (DateTimeField): Enrollment timestamp
```

#### **Payment**
Records online payment transactions via Razorpay.

```python
- order_id (CharField): Razorpay order ID
- payment_id (CharField): Razorpay payment ID
- user (ForeignKey): Paying user
- course (ForeignKey): Purchased course
- user_course (ForeignKey): Enrollment reference
- status (BooleanField): Payment success status
- date (DateTimeField): Payment timestamp
```

#### **ManualPayment**
Records manual payment submissions for verification.

```python
- transaction_id (CharField): User's transaction ID
- amount (DecimalField): Paid amount in rupees
- original_amount (DecimalField): Price before coupon discount
- coupon_discount (DecimalField): Discount amount applied
- mobile_number (CharField): User contact number
- transaction_date (DateField): Payment date
- screenshot (ImageField): Payment proof screenshot
- user (ForeignKey): Submitting user
- course (ForeignKey): Associated course
- coupon_used (ForeignKey): Applied coupon code
- status (CharField): Payment status [pending/confirmed/rejected]
- admin_remarks (TextField): Admin verification notes
```

#### **CouponCode**
Discount coupon management system.

```python
- code (CharField): Coupon code [UNIQUE, AUTO-UPPERCASE]
- course (ForeignKey): Applicable course
- discount_type (CharField): Type [percentage/fixed]
- discount_value (IntegerField): Discount amount
- max_uses (IntegerField): Maximum redemptions allowed
- used_count (IntegerField): Current redemptions
- valid_from (DateTimeField): Activation time (IST)
- valid_to (DateTimeField): Expiration time (IST)
- active (BooleanField): Activation status
- created_date (DateTimeField): Creation timestamp

Methods:
- is_valid(): Check if coupon is currently valid
- calculate_discount(price): Calculate discount amount
- apply_discount(price): Get final price after discount
```

---

## 🔧 Installation & Setup

### Prerequisites
- **Python:** 3.8 or higher
- **pip:** Package manager
- **Virtual Environment:** venv or virtualenv (recommended)
- **Git:** Version control

### Local Development Setup

#### 1. **Clone the Repository**
```bash
git clone https://github.com/Saket8538/prantix.git
cd prantix
```

#### 2. **Create Virtual Environment**
```bash
# On Windows
python -m venv env
env\Scripts\activate

# On macOS/Linux
python3 -m venv env
source env/bin/activate
```

#### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

#### 4. **Configure Environment Variables**
Create a `.env` file in the project root:

```env
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Development - SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Payment Gateway (Razorpay)
RAZORPAY_KEY_ID=your-key-id-here
RAZORPAY_KEY_SECRET=your-key-secret-here

# UPI Payment Details
UPI_ID=your-upi@bank
QR_CODE_PATH=files/qr_code.png
```

#### 5. **Create Database & Run Migrations**
```bash
python manage.py migrate
```

#### 6. **Create Superuser (Admin)**
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

#### 7. **Collect Static Files**
```bash
python manage.py collectstatic --noinput
```

#### 8. **Run Development Server**
```bash
python manage.py runserver
```

Visit: `http://localhost:8000`
Admin Panel: `http://localhost:8000/admin`

---

## 📋 URL Routes

All URL patterns are defined in `courses/urls.py`:

| Route | Method | View | Purpose |
|-------|--------|------|---------|
| `/` | GET | `HomePageView` | Landing page |
| `/signup` | GET, POST | `SignupView` | User registration |
| `/login` | GET, POST | `LoginView` | User login |
| `/logout` | POST | `signout` | User logout |
| `/courses/` | GET | `CoursesListView` | All active courses |
| `/course/<slug>` | GET | `coursePage` | Course details + video player |
| `/my-courses` | GET | `MyCoursesList` | Student's enrolled courses |
| `/check-out/<slug>` | GET | `checkout` | Razorpay payment page |
| `/verify_payment` | POST | `verifyPayment` | Razorpay payment verification |
| `/payments/` | GET, POST | `payment_page` | Manual payment form |
| `/payments/<slug>/` | GET, POST | `payment_page` | Manual payment for course |
| `/payment-confirm/` | POST | `payment_confirm` | Manual payment submission |
| `/api/validate-coupon/` | POST | `validate_coupon` | Coupon validation API |
| `/about/` | GET | Static page | About page |
| `/careers/` | GET | Static page | Careers page |
| `/privacy/` | GET | Static page | Privacy policy |
| `/terms/` | GET | Static page | Terms of service |
| `/newsletter/subscribe/` | POST | `newsletter_subscribe` | Newsletter signup |

---

## 💳 Payment Integration

### Razorpay Online Payments

**Flow:**
1. User selects course and clicks "Enroll Now"
2. Redirected to checkout page
3. Razorpay payment modal appears
4. After payment, webhook verifies transaction
5. UserCourse entry created on success
6. Confirmation email sent

**Configuration:**
```python
# In prantix/settings.py
KEY_ID = config('RAZORPAY_KEY_ID')           # Razorpay Key ID
KEY_SECRET = config('RAZORPAY_KEY_SECRET')   # Razorpay Key Secret
```

**Test Credentials:**
- Card: `4111 1111 1111 1111`
- Expiry: Any future date
- CVV: Any 3 digits

### Manual Payments

**Flow:**
1. User selects manual payment option
2. Fills payment form with transaction details
3. Uploads payment screenshot
4. Admin reviews in dashboard
5. Admin marks as confirmed/rejected
6. Automated emails sent to user

**Admin Dashboard Actions:**
- View all manual payment submissions
- Filter by status (Pending/Confirmed/Rejected)
- Search by transaction ID, username, course
- Add admin remarks
- Bulk approve/reject payments
- Automatic email notifications

---

## 🎫 Coupon System

### Coupon Features

1. **Discount Types:**
   - **Percentage:** 0-100% discount
   - **Fixed Amount:** Fixed rupee discount

2. **Time-Based Validity:**
   - All times stored and displayed in IST (Indian Standard Time)
   - Valid from and Valid to timestamps
   - Current validity status shown in admin

3. **Usage Limits:**
   - Set maximum uses per coupon
   - Track current usage count
   - Prevent exceeding max uses

4. **Admin Dashboard:**
   - Create/edit/delete coupons
   - Visual usage progress bar (0-100%)
   - Color-coded validity status
   - Timezone information display

### Coupon Validation API

**Endpoint:** `POST /api/validate-coupon/`

**Request Body:**
```json
{
    "code": "SUMMER20",
    "course_id": 1
}
```

**Response (Valid):**
```json
{
    "valid": true,
    "message": "Coupon applied successfully!",
    "discount_amount": 500,
    "final_price": 2500
}
```

**Response (Invalid):**
```json
{
    "valid": false,
    "message": "Coupon code expired or invalid"
}
```

---

## 🔐 Authentication & Authorization

### User Types

1. **Anonymous Users**
   - View homepage, course list
   - Preview marked videos
   - Cannot access enrolled courses

2. **Registered Users**
   - Register/login
   - Enroll in courses via payment
   - Access purchased courses
   - View dashboard

3. **Superusers (Admin)**
   - Full admin panel access
   - Manage courses, users, payments
   - Approve manual payments
   - Create/manage coupons

### Access Control

**Course Access Logic:**
```
if video is marked as preview:
    → Allow anonymous and registered users
else:
    if user is not authenticated:
        → Redirect to login
    else if user not enrolled:
        → Redirect to checkout
    else:
        → Allow access
```

---

## 🌐 Deployment to Azure App Service

### Prerequisites
- Azure subscription
- Azure CLI installed
- PostgreSQL Flexible Server instance
- Storage account for static files (optional)

### Deployment Steps

#### 1. **Create Azure Resources**
```bash
# Create resource group
az group create --name prantix-rg --location centralindia

# Create App Service Plan
az appservice plan create --name prantix-plan --resource-group prantix-rg --sku B2 --is-linux

# Create Web App
az webapp create --resource-group prantix-rg --plan prantix-plan --name prantix-app --runtime "PYTHON|3.11"

# Create PostgreSQL Server
az postgres flexible-server create --resource-group prantix-rg --name prantix-db --admin-user dbadmin --admin-password YourSecurePassword123!
```

#### 2. **Configure Deployment Settings**
```bash
# Set environment variables
az webapp config appsettings set --resource-group prantix-rg --name prantix-app --settings \
    DJANGO_SETTINGS_MODULE=prantix.deployment \
    DJANGO_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())") \
    DEBUG=False \
    WEBSITE_HOSTNAME=prantix-app.azurewebsites.net \
    AZURE_POSTGRESQL_CONNECTIONSTRING="dbname=prantix host=prantix-db.postgres.database.azure.com user=dbadmin@prantix-db password=YourSecurePassword123! sslmode=require" \
    RAZORPAY_KEY_ID=your-key-id \
    RAZORPAY_KEY_SECRET=your-key-secret \
    EMAIL_HOST_USER=your-email@outlook.com \
    EMAIL_HOST_PASSWORD=your-app-password
```

#### 3. **Deploy Code**
```bash
# Initialize Git repo (if not done)
git init
git add .
git commit -m "Initial commit for Azure deployment"

# Add Azure remote
az webapp deployment source config --resource-group prantix-rg --name prantix-app --repo-url https://github.com/Saket8538/prantix.git --branch main --manual-integration
```

#### 4. **Post-Deployment**
```bash
# SSH into App Service
az webapp ssh --resource-group prantix-rg --name prantix-app

# Inside SSH terminal:
cd /home/site/wwwroot
python manage.py migrate --settings=prantix.deployment
python manage.py createsuperuser --settings=prantix.deployment
python manage.py collectstatic --noinput --settings=prantix.deployment
```

#### 5. **Verify Deployment**
Visit: `https://prantix-app.azurewebsites.net`

### Azure-Specific Configuration

The project includes `prantix/deployment.py` with Azure optimizations:

- **SSL/HTTPS:** Automatic SSL termination (no SECURE_SSL_REDIRECT needed)
- **Database:** PostgreSQL Flexible Server connection
- **Static Files:** WhiteNoise middleware for efficient static file serving
- **Security:** CSRF, cookie security settings configured
- **Logging:** Azure-compatible logging setup

---

## 📧 Email Configuration

### Gmail/Outlook Setup

#### Gmail
1. Enable 2-factor authentication
2. Generate app password: https://myaccount.google.com/apppasswords
3. Set in `.env`:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### Outlook/Microsoft 365
1. Enable modern authentication
2. Generate app password
3. Set in `.env`:
```env
EMAIL_HOST=smtp.office365.com
EMAIL_HOST_USER=your-email@outlook.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Email Templates

Located in `courses/templates/courses/emails/`:

1. **newsletter_welcome.html** - Newsletter subscription confirmation
2. **user_payment_confirmed.html** - Payment success notification
3. **user_payment_rejected.html** - Payment failure notification
4. **user_payment_submitted.html** - Manual payment submission acknowledgment
5. **admin_payment_notification.html** - Admin payment submission alert

---

## 📊 Admin Dashboard Guide

### Course Management

**Path:** `/admin/courses/course/`

- **Add Course:**
  - Fill course details (name, slug, price, discount)
  - Set active status
  - Add thumbnail and resource files
  - Inline add Tags, Prerequisites, Learning outcomes, Videos

- **Edit Course:**
  - Modify any course field
  - Edit associated videos/tags
  - Update pricing and discount

### Payment Management

**Path:** `/admin/courses/payment/`

- View all Razorpay payments
- Filter by status or course
- View linked user and course

### Manual Payment Review

**Path:** `/admin/courses/manualpayment/`

- **Review Pending Payments:**
  - View transaction ID and screenshot
  - Check transaction date and amount
  - See applied coupon discount

- **Actions:**
  - Mark as Confirmed → User gains course access, receives confirmation email
  - Mark as Rejected → User notified with reason
  - Add remarks for audit trail

### Coupon Management

**Path:** `/admin/courses/couponcode/`

- **Create Coupon:**
  - Set code (auto-converted to uppercase)
  - Select discount type (percentage/fixed)
  - Set validity period (IST timezone)
  - Set usage limits

- **Monitor Usage:**
  - Visual progress bar showing usage %
  - Color coding (green < 50%, orange 50-80%, red > 80%)
  - Current validity status display
  - IST timezone information

### User Management

**Path:** `/admin/auth/user/`

- View all registered users
- Edit user details
- Manage permissions and staff status

---

## 🎨 Frontend Features

### Modern UI Components

**File:** `courses/static/courses/js/modern-ui.js`

1. **Intersection Observer Animations**
   - Fade-in animations on element entry
   - Applied to course cards, stat items, section titles

2. **Navbar Effects**
   - Dynamic background on scroll
   - Smooth transitions

3. **Interactive Elements**
   - Course card hover effects (lift animation)
   - Video play button functionality
   - Counter animations for statistics

4. **Alert Management**
   - Auto-dismiss alerts after 50 seconds
   - Persistent alerts for important notices
   - Payment instructions remain visible

### Responsive Design

- **Bootstrap 5** framework
- Mobile-first approach
- Responsive grid layout
- Touch-friendly buttons and forms

---

## 🧪 Testing

### Manual Testing Checklist

#### User Registration & Authentication
- [ ] Signup with valid email
- [ ] Signup validation (duplicate email, weak password)
- [ ] Login with correct credentials
- [ ] Login fails with wrong password
- [ ] Logout functionality
- [ ] Protected pages redirect to login

#### Course Browsing
- [ ] Homepage loads correctly
- [ ] Course list displays all active courses
- [ ] Course page displays videos and content
- [ ] Preview videos accessible without enrollment
- [ ] Non-preview videos blocked without enrollment

#### Payment Flow
- [ ] Razorpay checkout opens correctly
- [ ] Test payment succeeds with test card
- [ ] UserCourse created after payment
- [ ] Payment confirmation email sent
- [ ] Failed payment handled gracefully

#### Coupon System
- [ ] Valid coupon applies discount
- [ ] Expired coupon rejected
- [ ] Exceeded max uses coupon rejected
- [ ] Discount calculation correct
- [ ] Price updates on coupon application

#### Manual Payment
- [ ] Payment form displays correctly
- [ ] File upload (screenshot) works
- [ ] Form validation works
- [ ] Admin can review submissions
- [ ] Approval/rejection emails sent

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: Static Files Not Loading
**Solution:**
```bash
python manage.py collectstatic --noinput
# Check STATIC_ROOT and STATIC_URL settings
```

#### Issue: Database Connection Error
**Solution:**
```bash
# Verify DATABASE config in settings.py
# Test connection: python manage.py dbshell
# Run migrations: python manage.py migrate
```

#### Issue: Email Not Sending
**Solution:**
```bash
# Check EMAIL_BACKEND setting
# Verify credentials in .env
# Check spam/junk folder
# Enable "Less secure apps" if using Gmail
```

#### Issue: Razorpay Payment Fails
**Solution:**
```bash
# Verify KEY_ID and KEY_SECRET in settings
# Use test credentials for development
# Check ALLOWED_HOSTS for domain issues
```

#### Issue: Coupon Not Working
**Solution:**
```bash
# Verify coupon active status
# Check current time vs valid_from/valid_to in IST
# Verify used_count < max_uses
# Check course relationship
```

---

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to complex functions
- Keep templates DRY (Don't Repeat Yourself)

### Database Changes
```bash
# After modifying models.py
python manage.py makemigrations
python manage.py migrate
```

### Creating New Features
1. Update models if needed
2. Create forms (if form interaction required)
3. Write views with proper authentication
4. Create templates
5. Add URL routes
6. Test thoroughly
7. Update admin interface

---

## 🤝 Contributing

### Guidelines
1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes with clear commits
4. Push to branch: `git push origin feature/your-feature`
5. Open pull request with description

---

## 📄 License

This project is licensed under the **Apache License 2.0**. See LICENSE file for details.

### License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ Trademark use restricted
- ✅ License and copyright notice required

---

## 👤 Author

**Saket Verma**
- GitHub: [@Saket8538](https://github.com/Saket8538)
- Email: prantix.official@outlook.com
- Website: https://prantix.live

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- **Email:** prantix.official@outlook.com
- **GitHub Issues:** [Create an issue](https://github.com/Saket8538/prantix/issues)
- **Careers:** careers@prantix.example

---

## 🚀 Roadmap

### Planned Features
- [ ] Video streaming optimization (CDN integration)
- [ ] Course analytics dashboard
- [ ] Student progress tracking
- [ ] Discussion forums
- [ ] Certificate generation
- [ ] Mobile app (React Native)
- [ ] Advanced search and filtering
- [ ] Instructor dashboard
- [ ] Subscription model support
- [ ] Integration with LMS platforms

---

## 📚 Documentation Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Guide](https://getbootstrap.com/docs/5.0/)
- [Razorpay API Reference](https://razorpay.com/docs/api/)
- [Azure App Service Docs](https://docs.microsoft.com/en-us/azure/app-service/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## ⭐ Acknowledgments

- Django community for the excellent web framework
- Bootstrap team for responsive design
- Razorpay for payment processing
- Azure for cloud hosting
- All contributors and users

---

## 📊 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Oct 2025 | Initial release |
| 1.1.0 | Nov 2025 | Manual payment system added |
| 1.2.0 | Nov 2025 | Coupon system enhanced with IST timezone |

---

## 📋 Checklist for Initial Setup

- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Configure .env file
- [ ] Run migrations
- [ ] Create superuser
- [ ] Collect static files
- [ ] Test locally
- [ ] Deploy to Azure (or hosting of choice)
- [ ] Configure domain and SSL
- [ ] Set up email service
- [ ] Test payment gateway
- [ ] Create initial courses
- [ ] Monitor admin panel

---

**Last Updated:** November 2025
**Repository:** https://github.com/Saket8538/prantix
**Live Site:** https://prantix.live

---

## 🎯 Key Highlights

✨ **Production-Ready** - Fully configured for Azure deployment
🔐 **Secure** - CSRF protection, secure payments, SSL/TLS ready
📱 **Responsive** - Works perfectly on desktop, tablet, and mobile
💰 **Flexible Payments** - Razorpay online + manual verification
🎫 **Smart Coupons** - Time-based, usage-limited, IST-aware
📧 **Email Integration** - Automated notifications and confirmations
⚡ **Performance** - WhiteNoise static serving, optimized queries
🌍 **Global Ready** - Multi-timezone support, international payment capability

