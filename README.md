# FoodFlow — Expiry-Aware Food Donation Platform
**University CSE Lab Project**

FoodFlow is a full-stack Django web application designed to help surplus food reach people before it expires. The platform connects food donors (restaurants, households, grocers, caterers) with verified recipients (NGOs, community kitchens, shelters, and individuals in need) through automated safety screening, live expiry urgency tracking, local matching alerts, and 8-character token verification for handovers.

---

## 🌟 Key Features

1. **Role-Based Access Control**: Separate dashboards, workflows, and permissions for Food Donors, Recipients, and Platform Administrators.
2. **Dynamic Live Expiry Urgency**: Automatic classification into `SAFE` (>6h), `WARNING` (2-6h), `URGENT` (<2h), and `EXPIRED` states with real-time browser countdowns.
3. **Automated Safety Screening**: Real-time screening against high-risk food keywords (raw meat, sashimi, unpasteurized items, etc.) with automated blocking.
4. **Area-Based Recipient Notifications**: Automatically alerts matching verified recipients in the same area or city when surplus food is posted.
5. **Race-Condition Safe Claiming**: Concurrency-protected claiming using database row-locking (`select_for_update`) and atomic transactions (`transaction.atomic`).
6. **8-Character Pickup Verification Code**: Unique hexadecimal code generated for the recipient and verified by the donor during physical handover.
7. **Two-Layer Expired Food Auto-Hiding**:
   - *Layer 1*: Recipient queries strictly use `FoodListing.visible_to_recipients()` to prevent displaying expired donations.
   - *Layer 2*: An automated management command (`expiry_sweep`) updates statuses, closes timed-out pickup windows, and sends alerts.

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Django 5.x (Django ORM, Authentication, Console Email Backend)
- **Database**: SQLite3 (ACID-compliant transactions for local development)
- **Frontend**: HTML5, CSS3 (Responsive Grid & Custom Variables), Vanilla JavaScript (No heavy frameworks or build steps)

---

## 📂 Project Structure

```text
FoodFlow-1/
├── manage.py                          # Django command-line runner
├── requirements.txt                   # Minimal project dependencies
├── README.md                          # Complete documentation & viva guide
├── .gitignore                         # Standard git ignore rules
├── db.sqlite3                         # SQLite database (auto-generated)
│
├── config/                            # Root project configuration package
│   ├── __init__.py
│   ├── settings.py                    # Project settings & FOODFLOW_SETTINGS
│   ├── urls.py                        # Root URL routing
│   ├── wsgi.py                        # WSGI entrypoint
│   └── asgi.py                        # ASGI entrypoint
│
├── accounts/                          # User accounts, authentication & profiles
│   ├── models.py                      # User (AbstractUser), Donor, Recipient
│   ├── forms.py                       # Registration, login, profile forms
│   ├── views.py                       # Auth views & role-based dashboards
│   ├── urls.py                        # Account routes (/register/, /login/, etc.)
│   ├── admin.py                       # Admin verification actions
│   ├── tests.py                       # Registration & role tests
│   └── management/commands/
│       └── seed_foodflow_demo.py      # Demo dataset seeder
│
├── locations/                         # Physical address management & geo-matching
│   ├── models.py                      # Location model (unique constraints & indexes)
│   ├── services.py                    # LocationMatchingService (area/city matching)
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── listings/                          # Food listings, safety & expiry tracking
│   ├── models.py                      # FoodListing, ExpiryTracker, FoodSafetyCheck
│   ├── services.py                    # ExpiryService & SafetyService
│   ├── forms.py                       # FoodListingForm with expiry validations
│   ├── views.py                       # Donor management & Recipient browse views
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── management/commands/
│       └── expiry_sweep.py            # Management command for expired food sweep
│
├── claims/                            # Food reservation & pickup verification
│   ├── models.py                      # Claim model (8-char pickup code)
│   ├── services.py                    # ClaimService (atomic locking & handovers)
│   ├── forms.py                       # ClaimForm & PickupVerificationForm
│   ├── views.py                       # Claim creation, list, cancellation, verify
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── notifications/                     # In-app notifications & email dispatch
│   ├── models.py                      # Notification model
│   ├── services.py                    # NotificationService
│   ├── views.py                       # Notification list & unread count JSON
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── templates/                         # Django HTML templates
│   ├── base.html                      # Main layout template
│   ├── home.html                      # Landing page with live impact stats
│   ├── partials/                      # Reusable navbar, alerts, and footer
│   ├── accounts/                      # Register, login, profile, dashboards
│   ├── listings/                      # Cards, forms, browse, detail pages
│   ├── claims/                        # My claims, claim detail, pickup verify
│   └── notifications/                 # In-app notification center
│
└── static/                            # Static CSS and Vanilla JS assets
    ├── css/styles.css                 # Responsive styling & design system
    ├── js/countdown.js                # Live dynamic countdown timer
    ├── js/claims.js                   # Double-submit guard & confirmation
    └── js/notifications.js            # Periodic unread notification poller
```

---

## 🚀 Setup & Execution Guide

### 1. Create and Activate Virtual Environment

**On Windows (PowerShell / Command Prompt):**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 3. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 4. Populate Demo Dataset (Recommended for Lab Evaluation)
We provide a built-in demo seeder that creates an admin, verified donor, verified & unverified recipients, and sample listings across all urgency and safety states:
```bash
python manage.py seed_foodflow_demo
```

---

### 5. (Optional) Create Custom Superuser
```bash
python manage.py createsuperuser
```

---

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit the website at: **`http://127.0.0.1:8000/`**
Access the Django Admin at: **`http://127.0.0.1:8000/admin/`**

---

### 7. Run the Expiry Sweep Background Task
Simulate or run the automated background expiry sweep:
```bash
python manage.py expiry_sweep
```

---

### 8. Run Automated Test Suite
```bash
python manage.py test
```

---

## 🔑 Demo Credentials

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Django Admin, user verification, listing moderation |
| **Verified Donor** | `greengarden` | `donor123` | Post donations, edit listings, verify pickup codes |
| **Verified Recipient** | `hopefoundation` | `recipient123` | Browse food, claim available items, receive pickup codes |
| **Unverified Recipient** | `john_doe` | `recipient123` | Demonstrates verification-guard blocking claims |

---

## 🎓 CSE Lab Viva & Architectural Guide

### 1. What is Django and why use it for this project?
Django is a high-level Python web framework that follows the **MVT (Model-View-Template)** architectural pattern. It provides built-in authentication, an Object-Relational Mapper (ORM), form validation, CSRF protection, and an administrative interface out of the box.

### 2. Why use a Custom User Model (`AbstractUser`)?
Django's default user model has only username, email, and basic fields. By subclassing `AbstractUser` as `accounts.User` before initial migrations, we cleanly added the `role` (`donor` vs `recipient`) and `phone` fields without hacky profile workarounds, while preserving standard authentication tools (`login`, `logout`, `authenticate`).

### 3. Difference between `ForeignKey` and `OneToOneField` in FoodFlow
- `OneToOneField`: Used for `Donor` and `Recipient` profiles linked to `User`. Each `User` has exactly one profile. Similarly, each `FoodListing` has one `ExpiryTracker` and one `FoodSafetyCheck`.
- `ForeignKey`: Represents a one-to-many relationship. For example, one `Donor` can post many `FoodListing` records, and one `FoodListing` can have multiple `Claim` records from recipients.

### 4. Why use a Service Layer (`services.py`)?
Instead of putting business logic inside Views (which leads to "fat views" that are hard to test and maintain), we use dedicated services:
- `ExpiryService`: Centralizes urgency classification and status updates.
- `SafetyService`: Centralizes keyword screening and risk categorization.
- `ClaimService`: Manages concurrency-safe reservations and pickup verification.
- `LocationMatchingService`: Encapsulates proximity fallback logic.
- `NotificationService`: Handles multi-channel alerts and email dispatch.

### 5. Why `transaction.atomic()` and `select_for_update()`?
When two recipients try to claim the last 5 portions of a meal simultaneously:
- `transaction.atomic()` guarantees that all database updates succeed together or roll back entirely.
- `select_for_update()` places an exclusive row-level lock on the `FoodListing` record during the transaction. The second request must wait until the first finishes, recalculating `quantity_available` and preventing double-claiming / negative stock race conditions.

### 6. How does Expiry Detection work?
Expiry time (`expires_at`) is stored in the database as a timezone-aware DateTime. Remaining time is **never** statically stored in the database; it is dynamically calculated as `expires_at - timezone.now()`.
- **Query Layer**: `FoodListing.visible_to_recipients()` excludes expired food in all browsing views.
- **Background Layer**: `python manage.py expiry_sweep` scans the database to update `status='expired'` and alert recipients with pending claims.

### 7. How does the 8-Character Pickup Code work?
When a verified recipient reserves food, `ClaimService` generates a unique 8-character token using Python's cryptographically secure `secrets.token_hex(4).upper()`. During physical food pickup, the recipient presents this code. The donor enters it into `/donor/pickups/verify/`, and the server marks the claim completed inside an atomic transaction.

---

## 👥 4-Member Team Distribution

- **Member 1 (Authentication & Accounts)**: Custom User model, Donor/Recipient profile architecture, registration/login workflows, role guards, and profile management.
- **Member 2 (Listings, Expiry & Safety)**: FoodListing models, `ExpiryService` urgency thresholds, `SafetyService` keyword screening, and `expiry_sweep` management command.
- **Member 3 (Claims & Pickup Verification)**: Concurrency-safe `ClaimService`, row-locking (`select_for_update`), 8-character token generation, and donor verification workflow.
- **Member 4 (Frontend, Notifications & Admin)**: Responsive HTML/CSS templates, vanilla countdown & polling scripts, in-app notification center, and Django Admin customization.
