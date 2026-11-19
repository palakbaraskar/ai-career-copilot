# 🗄️ PostgreSQL Setup Guide for AI Career Co-Pilot

This guide explains how to connect and run your AI Career Co-Pilot with PostgreSQL on your local system or via a hosted PostgreSQL cloud instance (Supabase, Neon, Railway, Render, or ElephantSQL).

---

## 1. Local PostgreSQL Setup (Windows)

### Step 1: Install PostgreSQL
If PostgreSQL is not already installed on your machine:
1. Download the installer from: [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Run the installer and remember the master password you set for the default `postgres` user.

### Step 2: Create the Database
Open **SQL Shell (psql)** or **pgAdmin 4**, or run in command prompt:

```sql
-- Connect as postgres user
psql -U postgres

-- Create the application database
CREATE DATABASE career_copilot_db;
```

### Step 3: Configure `.env`
In your `ai-career-copilot/.env` file, add your PostgreSQL connection string:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/career_copilot_db
SECRET_KEY=career-copilot-secure-secret-key-2026
```
*(Replace `YOUR_PASSWORD` with your actual PostgreSQL password).*

---

## 2. Free Cloud PostgreSQL Setup (Alternative: Supabase / Neon)
If you prefer not running a local server on your laptop, you can get a 100% free hosted PostgreSQL database:

1. Sign up for free at [neon.tech](https://neon.tech) or [supabase.com](https://supabase.com).
2. Create a new project and copy your connection string (URI).
3. Paste it directly into your `.env`:
```env
DATABASE_URL=postgresql://user:password@ep-xyz.us-east-2.aws.neon.tech/career_copilot_db?sslmode=require
```

---

## 3. Install Dependencies & Run the App

Open your VS Code terminal in `ai-career-copilot`:

```powershell
# 1. Install required packages
pip install -r requirements.txt

# 2. Run automated test suite to verify database connection & models
python test_database.py

# 3. Start the Flask application
python app.py
```

---

## 4. Automatic Table Generation & Resilience
When `app.py` runs, it will **automatically create all 5 tables** in PostgreSQL:
1. `users` (Authentication & password hashes)
2. `resumes` (Saved ATS evaluations)
3. `job_matches` (Saved job compatibility audits)
4. `interview_sessions` (Saved mock interview question pools)
5. `interview_answers` (Candidate answers & STAR evaluation breakdowns)

> **Resilience Fallback**: If PostgreSQL service is not yet running or credentials are not yet configured, the system gracefully initializes a local database (`career_copilot.db`) so your development server never crashes while you are configuring PostgreSQL!
