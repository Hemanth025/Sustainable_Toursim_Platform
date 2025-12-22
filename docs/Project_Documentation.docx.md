# AI-Powered Sustainable Tourism Platform (EcoJourney)
## Comprehensive Project Documentation

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [System Architecture](#system-architecture)
4. [Project Flow](#project-flow)
5. [Core Modules & Models Explained](#core-modules--models-explained)
6. [Feature Implementation Details](#feature-implementation-details)
7. [Database Design](#database-design)
8. [Standards Compliance](#standards-compliance)
9. [Development Workflow](#development-workflow)
10. [Viva Questions - Set 1](#viva-questions---set-1)
11. [Viva Questions - Set 2](#viva-questions---set-2)

---

## 1. Project Overview

### 1.1 Project Title
**AI-Powered Sustainable Tourism Platform (EcoJourney)**

### 1.2 Project Description
EcoJourney is a comprehensive web-based sustainable tourism platform designed to promote eco-friendly travel practices in India. The platform leverages rule-based artificial intelligence to provide personalized travel recommendations, calculate carbon footprints, offer dynamic pricing insights, integrate local economies, and enhance cultural engagement through Augmented Reality (AR) technology.

### 1.3 Problem Statement
Tourism is one of the largest industries globally, but it poses significant environmental challenges:
- High carbon emissions from travel
- Over-tourism damaging natural habitats
- Economic leakage away from local communities
- Cultural heritage degradation
- Lack of awareness among tourists about sustainable practices

### 1.4 Solution Offered
EcoJourney addresses these challenges by:
- Recommending eco-friendly destinations based on user preferences
- Calculating and comparing carbon footprints of travel options
- Suggesting optimal booking times for budget-conscious sustainable travel
- Promoting local guides, homestays, and community tourism
- Using WebAR to educate tourists about cultural heritage and sustainability

### 1.5 Project Objectives
| Objective | Description |
|-----------|-------------|
| **Objective 1** | Personalized Travel Recommendations using Rule-Based AI |
| **Objective 2** | Environmental Impact Assessment (Carbon Footprint Calculator) |
| **Objective 3** | Dynamic Pricing Models for Smart Booking |
| **Objective 4** | Local Economy Integration for Community Support |
| **Objective 5** | Augmented Reality (AR) for Cultural Engagement |

---

## 2. Technology Stack

### 2.1 Backend Technologies
| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Primary programming language | 3.10+ |
| **Flask** | Web application framework | 2.x |
| **MySQL** | Relational database | 8.0+ |
| **mysql-connector-python** | Database connectivity | Latest |
| **bcrypt/hashlib** | Password hashing | Latest |

### 2.2 Frontend Technologies
| Technology | Purpose |
|------------|---------|
| **HTML5** | Page structure and semantic markup |
| **Tailwind CSS** | Utility-first CSS framework for styling |
| **JavaScript (ES6+)** | Interactive functionality and AJAX calls |
| **Jinja2** | Template engine (Flask integrated) |

### 2.3 AR Technologies
| Technology | Purpose |
|------------|---------|
| **AR.js** | Lightweight marker-based Augmented Reality library |
| **A-Frame** | Declarative 3D web framework for WebXR |
| **Hiro Marker** | Standard AR marker pattern |

### 2.4 Development Tools
- **Visual Studio Code** - Primary IDE
- **Git** - Version control
- **Python Virtual Environment** - Dependency isolation
- **Browser DevTools** - Debugging and testing

---

## 3. System Architecture

### 3.1 Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  HTML5 Templates + Tailwind CSS + JavaScript              │   │
│  │  - index.html, planner.html, itinerary.html               │   │
│  │  - carbon.html, pricing.html, local.html, ar.html         │   │
│  │  - Authentication: welcome.html, signup.html, signin.html │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Flask Application (app.py)                               │   │
│  │  ├── Route Handlers (API endpoints)                       │   │
│  │  ├── Authentication Middleware                            │   │
│  │  └── Session Management                                   │   │
│  │                                                           │   │
│  │  Rule-Based AI Modules (modules/)                         │   │
│  │  ├── recommendation_engine.py (Scoring Algorithm)         │   │
│  │  ├── carbon_calculator.py (Emission Calculations)         │   │
│  │  ├── pricing_engine.py (Seasonal Pricing Logic)           │   │
│  │  ├── knowledge_base.py (Hardcoded Data Repository)        │   │
│  │  └── auth_module.py (User Authentication)                 │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  MySQL Database (ecojourney_db)                           │   │
│  │  └── users table (authentication data)                    │   │
│  │                                                           │   │
│  │  Hardcoded Knowledge Base                                 │   │
│  │  ├── DESTINATIONS dictionary (10 Indian destinations)     │   │
│  │  ├── TRANSPORT_EMISSIONS (carbon emission factors)        │   │
│  │  ├── ACCOMMODATION_EMISSIONS (lodging impact data)        │   │
│  │  ├── SEASONAL_PRICING (pricing multipliers)               │   │
│  │  └── FESTIVAL_PERIODS (festival premium data)             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Folder Structure

```
Sustainable_Tourism/
├── app.py                          # Main Flask application (639 lines)
├── config.py                       # Configuration settings
├── setup_database.py               # Database initialization script
│
├── modules/                        # Rule-Based AI Modules
│   ├── __init__.py                 # Package initialization
│   ├── knowledge_base.py           # Hardcoded destination data (239 lines)
│   ├── recommendation_engine.py    # Scoring-based recommendations (195 lines)
│   ├── carbon_calculator.py        # Emission calculations (216 lines)
│   ├── pricing_engine.py           # Dynamic pricing logic (230 lines)
│   └── auth_module.py              # User authentication (592 lines)
│
├── templates/                      # Jinja2 HTML Templates
│   ├── base.html                   # Base template with navigation
│   ├── index.html                  # Landing page
│   ├── planner.html                # Multi-step travel planner
│   ├── itinerary.html              # Generated itinerary display
│   ├── carbon.html                 # Carbon footprint calculator
│   ├── pricing.html                # Dynamic pricing insights
│   ├── local.html                  # Local economy showcase
│   ├── ar.html                     # WebAR experience
│   ├── welcome.html                # Authentication landing
│   ├── signup.html                 # User registration
│   ├── signin.html                 # User login
│   ├── verify_otp.html             # OTP verification
│   ├── forgot_password.html        # Password reset request
│   ├── reset_password.html         # Password reset form
│   └── error.html                  # Error page
│
├── static/                         # Static assets
│   ├── css/styles.css              # Custom CSS styles
│   └── js/main.js                  # Client-side JavaScript
│
└── docs/                           # Documentation
    ├── capstone_documentation.md
    ├── implementation_plan.md
    └── Project_Documentation.docx.md
```

---

## 4. Project Flow

### 4.1 User Journey Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                         USER JOURNEY FLOW                             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   ┌───────────┐      ┌─────────────┐      ┌──────────────┐           │
│   │  Welcome  │ ───▶ │   Sign Up   │ ───▶ │  OTP Verify  │           │
│   │   Page    │      │   (Form)    │      │              │           │
│   └───────────┘      └─────────────┘      └──────┬───────┘           │
│         │                                        │                    │
│         │            ┌─────────────┐             │                    │
│         └──────────▶ │   Sign In   │ ◀───────────┘                   │
│                      │   (Login)   │                                  │
│                      └──────┬──────┘                                  │
│                             │                                         │
│                             ▼                                         │
│   ┌───────────────────────────────────────────────────────────────┐  │
│   │                      HOME PAGE (index.html)                    │  │
│   │   Features: Platform Overview, Quick Access to All Modules     │  │
│   └───────────────────────────────────────────────────────────────┘  │
│                             │                                         │
│         ┌───────────────────┼───────────────────┐                    │
│         │                   │                   │                    │
│         ▼                   ▼                   ▼                    │
│   ┌───────────┐      ┌───────────┐       ┌───────────┐              │
│   │  Travel   │      │  Carbon   │       │  Dynamic  │              │
│   │  Planner  │      │Calculator │       │  Pricing  │              │
│   └─────┬─────┘      └───────────┘       └───────────┘              │
│         │                                                            │
│         ▼                                                            │
│   ┌───────────────────────────────────────────────────────────────┐  │
│   │           MULTI-STEP TRAVEL PLANNING WIZARD                    │  │
│   │   Step 1: Budget Selection (Low/Medium/High)                   │  │
│   │   Step 2: Travel Type (Adventure/Nature/Cultural/etc.)         │  │
│   │   Step 3: Duration (Number of Days)                            │  │
│   │   Step 4: Sustainability Preference (1-10 Scale)               │  │
│   └───────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ▼                                                            │
│   ┌───────────────────────────────────────────────────────────────┐  │
│   │              RECOMMENDATION ENGINE PROCESSING                   │  │
│   │   - Score destinations using rule-based algorithm               │  │
│   │   - Apply budget, type, duration, and eco-score weights         │  │
│   │   - Apply seasonal bonus for current month                      │  │
│   │   - Return Top 5 ranked destinations                            │  │
│   └───────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ▼                                                            │
│   ┌───────────────────────────────────────────────────────────────┐  │
│   │              ITINERARY GENERATION                               │  │
│   │   - Day-by-day activity plan                                    │  │
│   │   - Eco-tips for each day                                       │  │
│   │   - Accommodation suggestions                                   │  │
│   │   - Local guide recommendations                                 │  │
│   └───────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ▼                                                            │
│   ┌───────────┐      ┌───────────┐       ┌───────────┐              │
│   │   Local   │      │   WebAR   │       │   Logout  │              │
│   │ Economy   │      │Experience │       │           │              │
│   └───────────┘      └───────────┘       └───────────┘              │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### 4.2 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│    USER INPUT                   PROCESSING                    OUTPUT     │
│    ─────────                   ──────────                    ──────     │
│                                                                          │
│   ┌──────────┐              ┌──────────────┐             ┌──────────┐   │
│   │ Budget   │──┐           │              │             │ Top 5    │   │
│   │ Type     │  │           │ Scoring      │             │ Destina- │   │
│   │ Duration │  ├──────────▶│ Algorithm    │────────────▶│ -tions   │   │
│   │ Eco-Pref │  │           │ (100 pts max)│             │ + Scores │   │
│   └──────────┘──┘           └──────────────┘             └──────────┘   │
│                                     │                                    │
│                                     ▼                                    │
│   ┌──────────┐              ┌──────────────┐             ┌──────────┐   │
│   │Transport │              │              │             │Emissions │   │
│   │ Mode     │─────────────▶│ Carbon       │────────────▶│ Report   │   │
│   │ Distance │              │ Calculator   │             │+ Altern- │   │
│   │ Nights   │              │              │             │ -atives  │   │
│   └──────────┘              └──────────────┘             └──────────┘   │
│                                     │                                    │
│                                     ▼                                    │
│   ┌──────────┐              ┌──────────────┐             ┌──────────┐   │
│   │ Destina- │              │              │             │ Monthly  │   │
│   │ -tion    │─────────────▶│ Pricing      │────────────▶│ Analysis │   │
│   │ Month    │              │ Engine       │             │ + Advice │   │
│   └──────────┘              └──────────────┘             └──────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Core Modules & Models Explained

### 5.1 Rule-Based AI Model (NOT Machine Learning)

**Important Note:** This project uses **Rule-Based Artificial Intelligence**, NOT Machine Learning. This means:
- No training datasets are used
- No model training or fitting is required
- All logic is based on predefined rules and decision matrices
- Results are deterministic and transparent

### 5.2 Recommendation Engine (`recommendation_engine.py`)

#### 5.2.1 Scoring Algorithm
The recommendation system uses a **weighted scoring algorithm** with a maximum score of 100 points:

| Factor | Max Points | Criteria |
|--------|------------|----------|
| **Budget Match** | 25 pts | Exact budget level match |
| **Travel Type** | 30 pts | Destination type matches preference |
| **Duration-Distance** | 20 pts | Travel time suitable for trip length |
| **Sustainability** | 25 pts | Eco-score matches user preference |
| **Seasonal Bonus** | 10 pts | Current month is in best season |

#### 5.2.2 Scoring Logic Example
```python
# Budget Matching (25 points max)
if dest["budget_level"] == budget:
    score += 25  # Exact match
elif budget == "medium" and dest["budget_level"] in ["low", "medium"]:
    score += 15  # Within range

# Travel Type Matching (30 points max)
if travel_type in dest["type"]:
    score += 30  # Direct match

# Sustainability Matching (25 points max)
eco_match = abs(dest["eco_score"] - sustainability_pref)
if eco_match <= 1:
    score += 25  # Close match
```

#### 5.2.3 Output
- Returns **Top 5 destinations** sorted by score
- Includes match reasons, eco-scores, and sustainability features

### 5.3 Carbon Calculator (`carbon_calculator.py`)

#### 5.3.1 Emission Factors (ISO 14001 Aligned)
| Transport Mode | kg CO₂ per km | Rating |
|----------------|---------------|--------|
| **Bicycle** | 0.000 | 🌿 Best |
| **Train** | 0.041 | ⭐ Recommended |
| **Electric Car** | 0.053 | Good |
| **Bus** | 0.089 | Moderate |
| **Car** | 0.171 | High |
| **Flight** | 0.255 | ⚠️ Highest |

#### 5.3.2 Calculation Functions
1. **`calculate_transport_emissions()`** - Computes travel emissions with alternatives
2. **`calculate_accommodation_emissions()`** - Calculates lodging impact
3. **`calculate_food_emissions()`** - Estimates food-related carbon footprint
4. **`calculate_total_footprint()`** - Complete trip carbon assessment

#### 5.3.3 Eco-Rating System
| Rating | Emissions per Day | Color |
|--------|-------------------|-------|
| A | < 5 kg CO₂ | Green |
| B | 5-10 kg CO₂ | Light Green |
| C | 10-20 kg CO₂ | Yellow |
| D | 20-35 kg CO₂ | Orange |
| E | > 35 kg CO₂ | Red |

### 5.4 Pricing Engine (`pricing_engine.py`)

#### 5.4.1 Seasonal Pricing Multipliers
| Season | Months | Price Multiplier |
|--------|--------|------------------|
| **Off-Peak** | Jun, Jul, Aug | 0.8x (20% savings) |
| **Shoulder** | Apr, May, Sep | 1.2x |
| **Peak** | Oct - Mar | 1.5x |

#### 5.4.2 Festival Premiums
| Festival | Month | Multiplier |
|----------|-------|------------|
| **New Year** | January Week 1 | 1.9x |
| **Diwali** | October/November | 1.8x |
| **Christmas** | December Week 4 | 1.7x |
| **Holi** | March Weeks 2-3 | 1.4x |

#### 5.4.3 Key Functions
1. **`get_current_season()`** - Determines current pricing season
2. **`calculate_price_level()`** - Computes price index for a destination
3. **`get_best_time_to_book()`** - Finds optimal booking months
4. **`generate_booking_advice()`** - Creates personalized recommendations

### 5.5 Knowledge Base (`knowledge_base.py`)

#### 5.5.1 Destination Data Structure
Each destination includes:
```python
"destination_id": {
    "name": "Full Name",
    "type": ["adventure", "nature", "spiritual"],  # Multiple types
    "eco_score": 8,                                 # 1-10 sustainability rating
    "budget_level": "medium",                       # low/medium/high
    "best_season": ["october", "november", ...],    # Optimal months
    "carbon_rating": "medium",                      # Travel impact
    "sustainability_features": ["feature1", "feature2"],
    "local_guides": ["Guide 1", "Guide 2"],
    "homestays": ["Homestay 1", "Homestay 2"],
    "distance_from_delhi": 1500,                    # km
    "description": "Detailed description",
    "ar_content": {
        "cultural_info": "Historical/cultural information",
        "eco_tips": "Sustainability tips for visitors"
    }
}
```

#### 5.5.2 Available Destinations (10 Total)
1. **Manali** - Adventure, Nature, Spiritual (Eco-Score: 8)
2. **Kerala Backwaters** - Nature, Relaxation, Cultural (Eco-Score: 9)
3. **Rishikesh** - Spiritual, Adventure, Nature (Eco-Score: 8)
4. **Jaipur** - Cultural, Heritage, Luxury (Eco-Score: 6)
5. **Coorg** - Nature, Relaxation, Adventure (Eco-Score: 9)
6. **Ladakh** - Adventure, Spiritual, Nature (Eco-Score: 7)
7. **Andaman Islands** - Beach, Adventure, Nature (Eco-Score: 8)
8. **Varanasi** - Spiritual, Cultural, Heritage (Eco-Score: 5)
9. **Munnar** - Nature, Relaxation, Adventure (Eco-Score: 9)
10. **Goa** - Beach, Relaxation, Cultural (Eco-Score: 6)

### 5.6 Authentication Module (`auth_module.py`)

#### 5.6.1 Features Implemented
- **User Registration** with field validation
- **OTP Verification** for signup (6-digit, 10-minute expiry)
- **Multi-Factor Authentication** for login
- **Password Reset** functionality
- **Session Management** with remember-me tokens
- **Password Strength Validation**

#### 5.6.2 Security Measures
| Feature | Implementation |
|---------|----------------|
| Password Hashing | bcrypt/hashlib SHA-256 |
| OTP Generation | Cryptographically random 6 digits |
| Session Security | Flask secret key + HTTPS |
| Input Validation | Server-side + Client-side |

---

## 6. Feature Implementation Details

### 6.1 Multi-Step Travel Planner
**Route:** `/planner` + `/itinerary/<destination_id>`

**Process:**
1. User enters preferences via 4-step wizard
2. Frontend sends AJAX request to `/api/recommendations`
3. Recommendation engine scores all destinations
4. Top 5 results displayed with match reasons
5. User selects destination → generates itinerary

### 6.2 Carbon Footprint Calculator
**Route:** `/carbon`

**Process:**
1. User selects transport mode, distance, accommodation type
2. Backend calculates emissions using fixed factors
3. Displays total footprint with eco-rating (A-E)
4. Shows greener alternatives with savings percentage
5. Calculates trees needed for carbon offset

### 6.3 Dynamic Pricing Insights
**Route:** `/pricing`

**Process:**
1. User selects destination
2. Pricing engine analyzes 12 months
3. Displays price level chart (Low to Premium)
4. Highlights best-value months
5. Provides booking advice

### 6.4 Local Economy Integration
**Route:** `/local`

**Process:**
1. Displays local guides and homestays per destination
2. Shows sustainability features
3. Promotes community-based tourism
4. Aligns with UNWTO guidelines

### 6.5 WebAR Cultural Engagement
**Route:** `/ar`

**Technology Stack:**
- AR.js for marker detection
- A-Frame for 3D rendering
- Hiro marker pattern

**Process:**
1. User opens AR page on mobile
2. Points camera at Hiro marker
3. 3D cultural content overlays
4. Sustainability tips displayed

---

## 7. Database Design

### 7.1 Database: `ecojourney_db`

### 7.2 Users Table Schema
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    otp_code VARCHAR(6),
    otp_expiry DATETIME,
    is_verified BOOLEAN DEFAULT FALSE,
    remember_token VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 7.3 ER Diagram
```
┌─────────────────────────────────────────┐
│                  USERS                   │
├─────────────────────────────────────────┤
│ PK  id              INT AUTO_INCREMENT  │
│     first_name      VARCHAR(50)          │
│     last_name       VARCHAR(50)          │
│ UK  username        VARCHAR(50)          │
│ UK  email           VARCHAR(100)         │
│ UK  phone           VARCHAR(20)          │
│     password_hash   VARCHAR(255)         │
│     otp_code        VARCHAR(6)           │
│     otp_expiry      DATETIME             │
│     is_verified     BOOLEAN              │
│     remember_token  VARCHAR(100)         │
│     created_at      DATETIME             │
│     updated_at      DATETIME             │
└─────────────────────────────────────────┘
```

---

## 8. Standards Compliance

### 8.1 ISO 14001 (Environmental Management System)

| ISO 14001 Element | Platform Implementation |
|-------------------|-------------------------|
| **Environmental Policy** | Visible carbon transparency in all recommendations |
| **Planning** | Pre-travel environmental impact assessment |
| **Implementation** | Greener alternatives provided for each choice |
| **Checking** | Continuous eco-score monitoring and feedback |
| **Management Review** | Improvement recommendations based on user choices |

### 8.2 UNWTO Sustainable Tourism Guidelines

| UNWTO Guideline | Implementation |
|-----------------|----------------|
| Support Local Economy | Local guides and homestays prominently featured |
| Cultural Preservation | WebAR cultural heritage engagement |
| Environmental Protection | Carbon calculator with offset suggestions |
| Visitor Education | Eco-tips throughout user journey |
| Community Benefit | Sustainability tags on all booking options |

### 8.3 GDPR Compliance

| Principle | Implementation |
|-----------|----------------|
| **Data Minimization** | Only essential user data collected |
| **Purpose Limitation** | Data used solely for authentication |
| **Storage Limitation** | Session-based for recommendations |
| **Security** | Encrypted passwords, secure sessions |
| **User Rights** | Account deletion available |

---

## 9. Development Workflow

### 9.1 Setup Instructions

```bash
# 1. Clone/Navigate to project directory
cd Sustainable_Tourism

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Install dependencies
pip install flask mysql-connector-python bcrypt

# 5. Setup MySQL database
python setup_database.py

# 6. Run the application
python app.py

# 7. Open browser: http://localhost:5000
```

### 9.2 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Home page |
| `/welcome` | GET | Auth landing page |
| `/signup` | GET/POST | User registration |
| `/signin` | GET/POST | User login |
| `/verify-signup` | GET/POST | OTP verification |
| `/verify-signin` | GET/POST | MFA verification |
| `/logout` | GET | User logout |
| `/planner` | GET/POST | Travel planner |
| `/itinerary/<id>` | GET | Generated itinerary |
| `/carbon` | GET/POST | Carbon calculator |
| `/pricing` | GET | Pricing insights |
| `/local` | GET | Local economy page |
| `/ar` | GET | WebAR experience |
| `/api/recommendations` | POST | Get recommendations (AJAX) |
| `/api/carbon` | POST | Calculate carbon (AJAX) |
| `/api/pricing/<id>` | GET | Get pricing data (AJAX) |

---

## 10. Viva Questions - Set 1

### Basic Understanding Questions (Q1-Q10)

**Q1. What is the main objective of the EcoJourney project?**
> **Answer:** EcoJourney is an AI-powered sustainable tourism platform that helps travelers make eco-friendly travel decisions. It provides personalized destination recommendations, calculates carbon footprints, offers dynamic pricing insights, promotes local economies, and uses WebAR for cultural engagement.

**Q2. Why was rule-based AI chosen instead of Machine Learning?**
> **Answer:** Rule-based AI was chosen because:
> 1. No training data is required - all logic is hardcoded
> 2. Results are transparent and deterministic
> 3. Faster development with instant deployment
> 4. No need for model training or maintenance
> 5. Suitable for academic demonstration within time constraints
> 6. Easier to explain and validate the logic

**Q3. Explain the technology stack used in this project.**
> **Answer:** 
> - **Backend:** Python with Flask framework
> - **Frontend:** HTML5, Tailwind CSS, JavaScript
> - **Database:** MySQL with mysql-connector-python
> - **AR:** AR.js + A-Frame for WebAR
> - **Template Engine:** Jinja2 (Flask integrated)

**Q4. What are the five main objectives implemented in this project?**
> **Answer:**
> 1. Personalized Travel Recommendations using scoring algorithm
> 2. Environmental Impact Assessment (Carbon Calculator)
> 3. Dynamic Pricing Models for smart booking
> 4. Local Economy Integration (guides, homestays)
> 5. Augmented Reality for Cultural Engagement

**Q5. How does the recommendation engine score destinations?**
> **Answer:** The scoring algorithm uses a weighted point system (max 100 points):
> - Budget Match: 25 points
> - Travel Type Match: 30 points
> - Duration-Distance Optimization: 20 points
> - Sustainability Preference: 25 points
> - Seasonal Bonus: 10 points (if current month is ideal)

**Q6. What emission factors are used in the carbon calculator?**
> **Answer:** Industry-standard emission factors (kg CO₂/km):
> - Flight: 0.255
> - Car: 0.171
> - Bus: 0.089
> - Electric Car: 0.053
> - Train: 0.041 (Recommended)
> - Bicycle: 0.000 (Zero emissions)

**Q7. Explain the seasonal pricing model.**
> **Answer:** The pricing engine uses multipliers:
> - Off-Peak (Jun-Aug): 0.8x (20% savings)
> - Shoulder (Apr, May, Sep): 1.2x
> - Peak (Oct-Mar): 1.5x
> Festival periods have additional premiums (Diwali: 1.8x, Christmas: 1.7x, etc.)

**Q8. What is WebAR and which libraries are used?**
> **Answer:** WebAR is Augmented Reality that runs in web browsers without requiring app installation. This project uses:
> - AR.js: Lightweight marker-based AR library
> - A-Frame: Declarative 3D web framework
> - Hiro Marker: Standard AR marker pattern for detection

**Q9. How is user authentication implemented?**
> **Answer:** 
> - Registration with field validation (username, email, phone uniqueness)
> - Password hashing using bcrypt/hashlib
> - 6-digit OTP verification for signup (10-minute expiry)
> - Multi-Factor Authentication for login
> - Session management with remember-me tokens

**Q10. What database is used and what table structure exists?**
> **Answer:** MySQL database `ecojourney_db` with a `users` table containing:
> - User identifiers (id, username, email, phone)
> - Personal info (first_name, last_name)
> - Security (password_hash, otp_code, otp_expiry)
> - Status (is_verified, remember_token)
> - Timestamps (created_at, updated_at)

### Technical Deep-Dive Questions (Q11-Q20)

**Q11. How does the itinerary generation work day-by-day?**
> **Answer:** The `generate_itinerary()` function:
> 1. Gets destination data from knowledge base
> 2. Creates activity pools based on destination types
> 3. Day 1: Arrival and orientation
> 4. Middle days: Rotates through activities; adds sustainable activities if eco-preference ≥ 7
> 5. Last day: Departure
> 6. Adds daily eco-tips from a predefined list
> 7. Suggests accommodation based on budget and sustainability preference

**Q12. Explain the GDPR compliance approach.**
> **Answer:**
> - **Data Minimization:** Only essential data collected
> - **Purpose Limitation:** Data used only for authentication
> - **Storage Limitation:** Recommendations are session-based, not stored
> - **User Rights:** Account deletion functionality
> - **Security:** Encrypted passwords, secure sessions
> - **Transparency:** No hidden data collection

**Q13. How does the eco-rating system work?**
> **Answer:** The eco-rating system grades trips from A (best) to E (worst):
> - Rating A: < 5 kg CO₂/day (Green)
> - Rating B: 5-10 kg CO₂/day (Light Green)
> - Rating C: 10-20 kg CO₂/day (Yellow)
> - Rating D: 20-35 kg CO₂/day (Orange)
> - Rating E: > 35 kg CO₂/day (Red)

**Q14. What ISO 14001 elements are implemented?**
> **Answer:** ISO 14001 (Environmental Management System) elements:
> - Environmental Policy: Carbon transparency
> - Planning: Pre-travel impact assessment
> - Implementation: Greener alternatives
> - Checking: Continuous eco-score monitoring
> - Management Review: Improvement recommendations

**Q15. How does festival period pricing work?**
> **Answer:** Festival periods have premium multipliers:
> - The system checks current month and week number
> - If a festival matches, its multiplier is applied
> - The higher of season or festival multiplier is used
> - Example: New Year (January Week 1) has 1.9x multiplier

**Q16. Explain the authentication flow for sign-up.**
> **Answer:**
> 1. User fills signup form with validation
> 2. Server checks uniqueness of username, email, phone
> 3. Password is hashed using bcrypt
> 4. User record created with is_verified=False
> 5. 6-digit OTP generated with 10-minute expiry
> 6. User enters OTP on verification page
> 7. Upon successful verification, is_verified=True
> 8. User can now sign in

**Q17. How are greener alternatives calculated?**
> **Answer:** For each transport carbon calculation:
> 1. Calculate emissions for selected mode
> 2. Calculate emissions for all alternative modes
> 3. Compute savings percentage: `(selected - alternative) / selected * 100`
> 4. Sort alternatives by emissions (lowest first)
> 5. Display alternatives with savings percentage

**Q18. What middleware is used for route protection?**
> **Answer:** The `check_authentication()` middleware:
> 1. Runs before each request using `@app.before_request`
> 2. Checks if route is protected (configurable list)
> 3. Verifies session has 'user_id'
> 4. If not authenticated, redirects to welcome page
> 5. Public routes (welcome, signup, signin) are excluded

**Q19. How does the sustainability preference affect recommendations?**
> **Answer:** Sustainability preference (1-10 scale) affects:
> - Destination scoring: Lower difference = higher score
> - Itinerary activities: Preference ≥ 7 triggers sustainable activities
> - Accommodation: High preference suggests homestays
> - Score weight: 25 points for eco-score matching

**Q20. Explain the AR experience user flow.**
> **Answer:**
> 1. User opens `/ar` page on mobile browser
> 2. Camera permission requested and granted
> 3. AR.js initializes video feed analysis
> 4. User points camera at Hiro marker
> 5. AR.js detects marker, sends to A-Frame
> 6. A-Frame renders 3D content overlay
> 7. Cultural information and eco-tips displayed
> 8. No app installation required

### Project-Specific Questions (Q21-Q25)

**Q21. What are the 10 destinations in the knowledge base?**
> **Answer:** 
> 1. Manali (Eco-Score: 8)
> 2. Kerala Backwaters (Eco-Score: 9)
> 3. Rishikesh (Eco-Score: 8)
> 4. Jaipur (Eco-Score: 6)
> 5. Coorg (Eco-Score: 9)
> 6. Ladakh (Eco-Score: 7)
> 7. Andaman Islands (Eco-Score: 8)
> 8. Varanasi (Eco-Score: 5)
> 9. Munnar (Eco-Score: 9)
> 10. Goa (Eco-Score: 6)

**Q22. How does local economy integration work?**
> **Answer:** Each destination has:
> - List of local guides with contact info
> - Traditional homestays for authentic experiences
> - Sustainability features (organic farming, community tourism)
> - The `/local` page showcases these options
> - Promotes community-based tourism over large hotels

**Q23. What UNWTO guidelines does this project follow?**
> **Answer:**
> - Support Local Economy: Promotes local guides and homestays
> - Cultural Preservation: WebAR for heritage education
> - Environmental Protection: Carbon calculator with alternatives
> - Visitor Education: Eco-tips throughout the journey
> - Community Benefit: Sustainability tags on options

**Q24. How does the platform handle errors?**
> **Answer:**
> - Custom error handlers for 404 and 500
> - Error template (`error.html`) with user-friendly messages
> - Try-catch blocks in database operations
> - Graceful degradation if MySQL unavailable
> - Session-based error messages using Flask flash

**Q25. What makes this project innovative?**
> **Answer:**
> - Integration of 5 sustainability pillars in one platform
> - Rule-based AI without ML dependency
> - WebAR without native app installation
> - ISO 14001 and UNWTO compliance
> - Session-based privacy (GDPR friendly)
> - Gamified eco-scores to encourage sustainable choices

---

## 11. Viva Questions - Set 2

### Architecture & Design Questions (Q1-Q10)

**Q1. Explain the three-tier architecture of this application.**
> **Answer:**
> - **Presentation Layer:** HTML templates, Tailwind CSS, JavaScript for user interface
> - **Business Logic Layer:** Flask app with route handlers, rule-based AI modules
> - **Data Layer:** MySQL database for users, hardcoded knowledge base for destinations

**Q2. Why is Flask chosen over Django for this project?**
> **Answer:**
> - Lightweight and minimal boilerplate
> - Microframework suitable for smaller projects
> - Flexible - choose own ORM, template engine
> - Faster development for academic projects
> - Easy to understand for demonstration

**Q3. How is the code organized into modules?**
> **Answer:**
> - `app.py`: Main Flask application with routes
> - `modules/knowledge_base.py`: All hardcoded data
> - `modules/recommendation_engine.py`: Scoring algorithm
> - `modules/carbon_calculator.py`: Emission calculations
> - `modules/pricing_engine.py`: Seasonal pricing logic
> - `modules/auth_module.py`: User authentication

**Q4. What design patterns are used in this project?**
> **Answer:**
> - **MVC Pattern:** Models (knowledge_base), Views (templates), Controllers (routes)
> - **Decorator Pattern:** Flask route decorators, login_required
> - **Factory Pattern:** Database connection creation
> - **Template Pattern:** Jinja2 template inheritance (base.html)

**Q5. How does the session management work?**
> **Answer:**
> - Flask's session object stores user_id after login
> - Secret key encrypts session cookies
> - Session lifetime: 24 hours (configurable)
> - Remember-me token for persistent login (30 days)
> - Session cleared on logout

**Q6. Explain the template inheritance structure.**
> **Answer:**
> - `base.html`: Contains header, navigation, footer, common CSS/JS
> - Child templates extend base.html using `{% extends %}`
> - Content blocks: `{% block content %}{% endblock %}`
> - Avoids code duplication across pages

**Q7. How are API endpoints structured?**
> **Answer:**
> - Page routes: Return rendered HTML templates
> - API routes (/api/*): Return JSON for AJAX calls
> - Authentication routes: Handle form submissions
> - Error routes: Custom 404 and 500 handlers

**Q8. What is the purpose of config.py?**
> **Answer:**
> - Centralizes MySQL database credentials
> - Defines OTP configuration (expiry, length)
> - Sets session lifetime parameters
> - Specifies password requirements
> - Contains table creation SQL

**Q9. How does the frontend communicate with the backend?**
> **Answer:**
> - Form submissions: Traditional POST requests
> - Dynamic content: AJAX calls to `/api/*` endpoints
> - Response format: JSON for APIs, HTML for pages
> - JavaScript handles API responses and updates UI

**Q10. What is the static folder structure?**
> **Answer:**
> - `static/css/styles.css`: Custom CSS overrides
> - `static/js/main.js`: Client-side JavaScript
> - Used for additional styling beyond Tailwind
> - Served directly by Flask's static file handler

### Security Questions (Q11-Q15)

**Q11. How are passwords securely stored?**
> **Answer:**
> - Passwords are hashed using bcrypt/hashlib
> - Salt is automatically added
> - Original password cannot be recovered
> - Verification compares hashes, not plain text
> - Minimum 8 characters with complexity requirements

**Q12. What are the password strength requirements?**
> **Answer:**
> - Minimum length: 8 characters
> - Must contain uppercase letter
> - Must contain lowercase letter
> - Must contain digit
> - Must contain special character
> - Password strength score (0-100) calculated

**Q13. How does OTP verification prevent abuse?**
> **Answer:**
> - 6-digit random OTP generated
> - 10-minute expiry window
> - Stored in database with expiry timestamp
> - One-time use - cleared after verification
> - Resend option with new expiry

**Q14. How is SQL injection prevented?**
> **Answer:**
> - Parameterized queries with placeholders
> - mysql-connector uses prepared statements
> - No string concatenation in SQL queries
> - Example: `cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))`

**Q15. What session security measures are implemented?**
> **Answer:**
> - Cryptographically generated secret key
> - Session data encrypted in cookies
> - Session timeout (24 hours)
> - New session ID on login
> - Session cleared on logout

### Performance & Scalability Questions (Q16-Q20)

**Q16. How can the knowledge base be expanded?**
> **Answer:**
> - Add new destinations to DESTINATIONS dictionary
> - Add new transport modes to TRANSPORT_EMISSIONS
> - Update seasonal pricing dates
> - Add new festival periods
> - No code changes to engine logic needed

**Q17. What caching strategies could improve performance?**
> **Answer:**
> - Cache recommendation results for common inputs
> - Redis/Memcached for session storage
> - Browser caching for static assets
> - CDN for Tailwind CSS and AR.js

**Q18. How would you scale this application?**
> **Answer:**
> - Horizontal scaling with load balancer
> - Database replication for read scaling
> - Containerization with Docker
> - Move knowledge base to database for editing
> - Implement API rate limiting

**Q19. What are the current limitations?**
> **Answer:**
> - Hardcoded data limits flexibility
> - Single MySQL instance bottleneck
> - No real-time data integration
> - AR requires specific marker
> - No mobile app (web-only)

**Q20. How does the application handle concurrent users?**
> **Answer:**
> - Flask handles multiple threads
> - Database connection pooling possible
> - Session storage is per-user
> - Stateless API design
> - No shared mutable state

### Testing & Deployment Questions (Q21-Q25)

**Q21. How would you test the recommendation engine?**
> **Answer:**
> - Unit tests for scoring logic
> - Test with various input combinations
> - Verify budget matching points
> - Check travel type scoring
> - Validate top 5 results ordering

**Q22. What browser testing is required for AR?**
> **Answer:**
> - Mobile browser with camera access
> - HTTPS required for camera (except localhost)
> - Test on Chrome, Safari, Firefox mobile
> - Verify marker detection accuracy
> - Check AR overlay positioning

**Q23. How would you deploy this application?**
> **Answer:**
> - Set production secret key
> - Disable debug mode
> - Use production WSGI server (Gunicorn)
> - Set up reverse proxy (Nginx)
> - Configure SSL/HTTPS
> - Use cloud MySQL (AWS RDS, Azure MySQL)

**Q24. What monitoring would you implement?**
> **Answer:**
> - Application logs for errors
> - Database query performance
> - API response times
> - User authentication failures
> - Session activity tracking

**Q25. What improvements would you suggest for future versions?**
> **Answer:**
> 1. Move knowledge base to database with admin panel
> 2. Add real-time pricing APIs
> 3. Implement booking functionality
> 4. Add social sharing features
> 5. Create mobile app version
> 6. Add user reviews and ratings
> 7. Implement gamification (badges, achievements)
> 8. Add multi-language support
> 9. Integrate payment gateway
> 10. Add offline PWA capabilities

---

## Conclusion

The EcoJourney AI-Powered Sustainable Tourism Platform successfully demonstrates:

✅ **Rule-Based AI** - Transparent scoring algorithm without ML dependencies

✅ **Environmental Assessment** - ISO 14001 aligned carbon calculations

✅ **Smart Pricing** - Seasonal and festival-aware pricing

✅ **Local Economy** - Community tourism promotion

✅ **WebAR Integration** - Browser-based augmented reality

✅ **Secure Authentication** - OTP-verified user management

✅ **Standards Compliance** - UNWTO, ISO 14001, GDPR

This project showcases the integration of sustainability principles with modern web technologies to promote responsible tourism in India.

---

*Document Version: 1.0*
*Last Updated: December 2024*
*Prepared for: Capstone Phase 2 Examination*
