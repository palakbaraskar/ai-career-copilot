# 🚀 AI Career Co-Pilot (3-in-1 Intelligent Suite)

An end-to-end intelligent career accelerator powered by **Python Flask**, **Google Gemini 1.5 Flash API**, and a modern **HTML5 / CSS3 / Vanilla JavaScript** Single-Page interface.

Designed specifically to be **resume-worthy, production-ready, and easy to explain during technical interviews**.

---

## 🌟 The 3 Integrated Projects

### 1. 📄 AI Resume ATS Analyzer
- **Dual Ingestion**: Upload resume PDFs (parsed in-memory via `PyPDF2`) or paste plain text.
- **ATS Metric Algorithm**: Generates an algorithmic 0–100 ATS compatibility score based on formatting, experience depth, skill taxonomy, and education.
- **Actionable Critique**: Highlights strong points, flags resume red flags (e.g., lack of measurable metrics), and provides concrete bullet-point rewrites.
- **Keyword Gap Analysis**: Identifies missing high-impact industry keywords to pass automated resume screening filters.

### 2. 🎯 Smart Job Matcher & Skill Gap Analyzer
- **Semantic Job Alignment**: Compares candidate profile directly against any target Job Description (JD).
- **Taxonomy Breakdown**: Segregates qualifications into **Matched Competencies** vs **Critical Missing Skills**.
- **Role-Tailored Summary**: Generates a 1st-person professional summary calibrated specifically to the job opening for one-click copy.
- **Curated Upskilling Roadmap**: Formulates a structured step-by-step learning pathway with specific resource suggestions and estimated timelines.

### 3. 🎙️ AI Mock Interview Prep Lab
- **Dynamic Role Simulation**: Generates custom Technical, Behavioral, and Situational questions for any given job title and description.
- **Interactive Practice Studio**: Candidates type their responses in real-time.
- **STAR Methodology Audit**: Evaluates answers across **Situation, Task, Action, and Result** pillars.
- **1–10 Scoring & Ideal Benchmark**: Provides instant constructive feedback, ideal answer outlines, and anticipated follow-up questions from the hiring manager.

---

## 🛠️ Tech Stack & Architecture

| Layer | Technologies | Role |
|-------|--------------|------|
| **Backend** | Python 3.10+, Flask, Flask-CORS | REST API routing, file streaming, prompt orchestration |
| **AI / LLM** | Google Gemini 1.5 Flash (`google-generativeai`) | High-speed, cost-effective inference with zero-shot JSON schemas |
| **Document Processing** | PyPDF2, BytesIO | In-memory binary PDF text extraction without disk I/O |
| **Frontend** | HTML5, Modern CSS (CSS Variables, Flexbox/Grid), Vanilla ES6+ JS | Zero heavy frontend dependencies; fast, responsive SPA experience |
| **Security & Config** | `python-dotenv` | API key isolation and environment configuration |

---

## ⚡ Quick Start Setup

### Step 1: Clone or Open Directory
```bash
cd "C:\Users\Palak Baraskar\OneDrive\Desktop\ai-career-copilot"
```

### Step 2: Create a Virtual Environment & Activate
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Add Your Free Google Gemini API Key
1. Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Create a `.env` file in the project root:
```env
GEMINI_API_KEY=AIzaSyYourActualGeminiKeyHere
```

### Step 5: Run the Server
```bash
python app.py
```
Open your browser at: **`http://127.0.0.1:5000`**

---

## 📁 Project File Structure

```
ai-career-copilot/
├── app.py                      # Flask REST microservice & Gemini endpoints
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables file
├── README.md                   # Full setup & architectural overview
├── INTERVIEW_GUIDE.md          # Complete interview talking guide & cheatsheet
├── templates/
│   ├── base.html               # Master layout with navbar, footer, & modals
│   ├── index.html              # Hub overview with metrics & project cards
│   ├── resume_analyzer.html    # Project 1: ATS Resume Parser & Grader
│   ├── job_matcher.html        # Project 2: Semantic JD Matcher & Gap Roadmap
│   └── interview_prep.html     # Project 3: STAR Mock Interview Chamber
└── static/
    ├── css/
    │   └── style.css           # Modern dark-mode styling with CSS variables
    └── js/
        └── main.js             # Client controller, API fetch calls, & sample data
```

---

## 💡 How to Demo in 30 Seconds
Every page comes equipped with a **"Load Sample"** button at the top right:
1. Go to **Resume Analyzer** → Click `Load Sample Resume` → Click `Run Gemini ATS Audit`.
2. Go to **Job Matcher** → Click `Load Sample Match Data` → Click `Run Semantic Gap Analysis`.
3. Go to **Interview Prep Lab** → Click `Load Sample Software Role` → Click `Generate AI Mock Interview Session` → Pick a question, type your answer, and review the **STAR audit**!
