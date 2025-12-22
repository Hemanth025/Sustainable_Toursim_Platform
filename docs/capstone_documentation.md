# AI-Powered Sustainable Tourism Platform
## Capstone Phase 2 Documentation

---

## Project Overview

**Project Title:** AI-Powered Sustainable Tourism Platform (EcoJourney)

**Objective:** Design and implement a web-based sustainable tourism platform using rule-based AI, carbon footprint assessment, dynamic pricing logic, and WebAR cultural engagement.

**Technology Stack:**
- **Backend:** Flask (Python)
- **Frontend:** HTML5 + Tailwind CSS
- **AR:** AR.js + A-Frame (WebAR)
- **Logic:** Rule-based decision systems (No ML/Datasets)

---

## Academic Compliance

### Mandatory Constraints Met

| Constraint | Implementation |
|------------|----------------|
| ❌ No Datasets | All data is hardcoded in `knowledge_base.py` |
| ❌ No ML Training | Pure rule-based logic in recommendation engine |
| ✅ Rule-Based AI | Decision matrices for all recommendations |
| ✅ Hardcoded Knowledge | 10 destinations with sustainability data |
| ✅ AR Compulsory | WebAR using AR.js + A-Frame |
| ✅ Short Timeframe | Modular, copy-paste ready implementation |

---

## Project Objectives Implementation

### Objective 1: Personalized Travel Recommendations

**File:** `modules/recommendation_engine.py`

**Logic:**
- Rule-based scoring system (0-100 points)
- Factors: Budget match (25pts), Travel type (30pts), Duration-distance (20pts), Sustainability (25pts)
- Seasonal bonus for current month
- Returns top 5 ranked destinations

**UI/UX:** Multi-step wizard form with eco-nudges at each step

---

### Objective 2: Environmental Impact Assessment

**File:** `modules/carbon_calculator.py`

**Industry-Standard Emission Factors (kg CO2):**
- Flight: 0.255/km
- Train: 0.041/km (Recommended)
- Bus: 0.089/km
- Car: 0.171/km

**Features:**
- Total footprint calculation
- Eco-score (1-10 scale)
- Greener alternatives with savings %
- Trees needed for offset
- ISO 14001 alignment points

---

### Objective 3: Dynamic Pricing Models

**File:** `modules/pricing_engine.py`

**Pricing Logic:**
| Season | Months | Multiplier |
|--------|--------|------------|
| Peak | Oct-Mar | 1.5x |
| Shoulder | Apr, May, Sep | 1.2x |
| Off-Peak | Jun-Aug | 0.8x |

**Festival Premiums:** Diwali (1.8x), Christmas (1.7x), New Year (1.9x), Holi (1.4x)

**Output:** Best time to book, monthly price analysis, booking advice

---

### Objective 4: Local Economy Integration

**File:** `modules/knowledge_base.py` → Local guides, homestays per destination

**UNWTO Alignment:**
- Local community benefit tracking
- Economic leakage minimization
- Cultural heritage preservation
- Sustainability tagging system

**UI:** Dedicated `/local` page showcasing guides and homestays

---

### Objective 5: Augmented Reality Cultural Engagement

**File:** `templates/ar.html`

**Technology:**
- AR.js: Lightweight marker-based AR library
- A-Frame: Declarative 3D web framework
- Marker: Standard Hiro pattern

**Features:**
- No app installation required
- Cultural site information overlay
- Sustainability tips at each site
- Works on mobile browsers

---

## Standards Mapping

### ISO 14001 (Environmental Management)

| ISO 14001 Element | Platform Implementation |
|-------------------|------------------------|
| Environmental Policy | Carbon footprint transparency |
| Planning | Pre-travel impact assessment |
| Implementation | Greener alternatives provided |
| Checking | Continuous eco-score monitoring |
| Management Review | Feedback-based recommendations |

### UNWTO Guidelines

| Guideline | Implementation |
|-----------|----------------|
| Support Local Economy | Local guides and homestays promotion |
| Cultural Preservation | AR cultural heritage engagement |
| Environmental Protection | Carbon calculator with alternatives |
| Visitor Education | Eco-tips throughout journey |
| Community Benefit | Sustainability tags on all options |

### GDPR Compliance

- **Zero Data Storage:** No databases used
- **Session-Only Processing:** Recommendations cleared after session
- **Transparency:** No hidden data collection
- **User Control:** No account required

---

## UI/UX Design Rationale

### Sustainability-Driven Design Patterns

1. **Eco-Nudges:** Green badges highlight sustainable options
2. **Default Greener:** Eco-friendly options pre-selected
3. **Carbon Indicators:** Real-time footprint display
4. **Social Proof:** "87% chose this eco option" messages
5. **Progress Visualization:** Gamified eco-scores

### How UI Influences Sustainable Decisions

- Multi-step form separates choices, reducing cognitive overload
- Visual eco indicators create immediate feedback
- Greener alternatives shown with savings percentages
- AR engagement educates at point of experience

---

## Folder Structure

```
Sustainable_Tourism/
├── app.py                      # Flask main application
├── modules/
│   ├── __init__.py
│   ├── knowledge_base.py       # Hardcoded destination data
│   ├── recommendation_engine.py # Rule-based AI
│   ├── carbon_calculator.py    # ISO 14001 emissions
│   └── pricing_engine.py       # Seasonal pricing logic
├── templates/
│   ├── base.html               # Base template
│   ├── index.html              # Landing page
│   ├── planner.html            # Travel wizard
│   ├── itinerary.html          # Day-by-day plan
│   ├── carbon.html             # Carbon calculator
│   ├── pricing.html            # Smart pricing
│   ├── local.html              # Local economy
│   ├── ar.html                 # WebAR experience
│   └── error.html              # Error page
├── static/
│   ├── css/styles.css
│   └── js/main.js
└── docs/
    └── capstone_documentation.md
```

---

## Viva Preparation Points

### Q1: Why rule-based instead of Machine Learning?
**A:** Rule-based systems offer transparency, instant deployment, no training data requirements, and deterministic outputs suitable for academic demonstration within time constraints.

### Q2: How does AR enhance sustainability?
**A:** AR reduces printed materials, delivers contextual eco-tips at cultural sites, and enhances visitor education without physical infrastructure.

### Q3: Explain ISO 14001 relevance
**A:** ISO 14001 provides a framework for environmental management. Our carbon tracking aligns with "Planning" and "Checking" elements, while greener alternatives support "Continuous Improvement."

### Q4: How is GDPR compliance achieved?
**A:** Zero data storage model - all processing is session-based with no persistent user data. No cookies, no tracking, no database.

### Q5: Scalability considerations?
**A:** Modular architecture allows knowledge base expansion. Rule parameters can be tuned. AR markers can be added for new sites.

### Q6: What makes this innovative?
**A:** Integration of 5 sustainability pillars (recommendations, carbon, pricing, local economy, AR) in a cohesive platform with no external dependencies.

---

## How to Run

```bash
# Navigate to project directory
cd Sustainable_Tourism

# Install Flask (if not installed)
pip install flask

# Run the application
python app.py

# Open browser to http://localhost:5000
```

---

## Conclusion

This Capstone Phase-2 project successfully demonstrates an AI-powered sustainable tourism platform that:

1. ✅ Uses rule-based intelligence without ML/datasets
2. ✅ Implements WebAR for cultural engagement
3. ✅ Aligns with ISO 14001 and UNWTO standards
4. ✅ Features purposeful UI/UX design
5. ✅ Is academically valid and completable in short timeframe

---

*Document prepared for Capstone Phase 2 Examination*
