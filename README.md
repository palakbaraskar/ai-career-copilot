🚀 AI Career Co-Pilot

An AI-powered career toolkit built with Python Flask, PostgreSQL and the Google Gemini API. It helps job seekers analyze their resume, match it against job descriptions, and practise interviews, with every result saved to a personal account.

🌟 Features
📄 Resume ATS Analyzer
Upload a PDF (text extracted in memory with PyPDF2) or paste plain text.
Get an ATS-style score, summary, strengths, weaknesses and section scores.
See missing keywords and concrete improvement suggestions.
🎯 Job Matcher & Skill Gap Analysis
Compare your resume with any job description.
See matched skills vs missing skills and an overall match score.
Get a tailored summary, action items and a step-by-step learning roadmap.
🎙️ Mock Interview Lab
Generate interview questions for any job title.
Type your answers and get a score, feedback, an ideal answer outline and a follow-up question.
🔐 Accounts & Dashboard
Register, log in and log out with Flask-Login.
Passwords are stored as hashes (Werkzeug), never as plain text.
A login-protected dashboard shows your own activity.
All results are stored in PostgreSQL and linked to your account.
🛠️ Tech Stack
Layer	Technologies	Role
Backend	Python, Flask, Flask-CORS	Routing (blueprints), request handling
Authentication	Flask-Login, Werkzeug	Sessions and password hashing
Database	PostgreSQL, Flask-SQLAlchemy, psycopg2-binary	Data storage and ORM models
AI	Google Gemini API (google-generativeai)	Resume analysis, job matching, interview feedback
Document Processing	PyPDF2	PDF text extraction
Frontend	HTML, CSS, JavaScript, Jinja2 templates	User interface
Configuration	python-dotenv	Environment variables
📁 Project Structure
ai-career-copilot/
├── app.py                 # Application factory, extensions, blueprint registration
├── config.py              # Configuration from environment variables
├── db.py                  # SQLAlchemy instance
├── models.py              # Database models (5 tables)
├── routes/                # Flask blueprints
│   ├── auth.py            #   registration, login, logout
│   ├── dashboard.py       #   user dashboard
│   ├── resume.py          #   resume ATS analysis
│   ├── job_match.py       #   job matching and skill gaps
│   └── interview.py       #   mock interview lab
├── services/              # Supporting logic (AI and document processing)
├── templates/             # HTML templates
├── static/                # CSS and JavaScript
├── test_database.py       # Database, authentication and access checks
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── POSTGRES_SETUP.md      # Extra PostgreSQL setup notes
└── INTERVIEW_GUIDE.md     # Notes for explaining the project in interviews
🗄️ Database Overview

Five tables are created automatically on startup.

Table	Purpose
users	Name, email, hashed password and creation time of each account
resumes	Analyzed resumes: name, ATS score, summary and full analysis (JSON)
job_matches	Job comparisons: title, description, match score and full result (JSON)
interview_sessions	Mock interview sessions: job title, optional description and generated questions (JSON)
interview_answers	Answered questions: question, answer, score, feedback and full evaluation (JSON)

A user has many resumes, job matches and interview sessions. An interview session has many answers. Deleting a user also deletes their records.

⚡ Quick Start
1. Clone and set up the environment
bash
git clone https://github.com/palakbaraskar/ai-career-copilot.git
cd ai-career-copilot
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
bash
pip install -r requirements.txt
2. Create the PostgreSQL database
bash
# Windows:  psql -U postgres
# Linux:    sudo -u postgres psql
# macOS:    psql postgres
sql
CREATE DATABASE career_copilot_db;
3. Get a Gemini API key

Create a free key at Google AI Studio.

4. Configure .env

Copy .env.example to .env (copy on Windows, cp on Linux/macOS) and fill in your values:

env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/career_copilot_db
SECRET_KEY=a_long_random_secret_string

.env is listed in .gitignore; never commit it.

5. Run the app
bash
python app.py

Open http://127.0.0.1:5000, create an account at /register, log in, and open the dashboard.

The console shows whether PostgreSQL connected. If it cannot connect, the app falls back to a local SQLite file (career_copilot.db), so check the message to see which database is in use.

🧪 Database Tests
bash
python test_database.py

Checks table creation, user creation and password hashing, saving and linking of records, per-user data separation, record deletion, the registration endpoint and login protection of /dashboard. It creates temporary test accounts in the configured database and removes them at the end, so use a development database.

🔮 Future Improvements
Deploy the application online
Database migrations with Flask-Migrate
Automated tests with pytest
Rate limiting for AI requests
Export reports as PDF
Progress charts on the dashboard
👩‍💻 Author

Palak Baraskar
B.Tech CSE, Indore Institute of Science and Technology
GitHub: github.com/palakbaraskar
