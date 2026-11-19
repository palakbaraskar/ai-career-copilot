import os
import re
import json
import google.generativeai as genai

# Setup Gemini API configuration
api_key = os.getenv("GEMINI_API_KEY", "").strip()
if api_key and api_key != "your_gemini_api_key_here":
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Error configuring Gemini: {e}")


def get_gemini_model():
    # Find active flash model
    try:
        models_list = list(genai.list_models())
        for m in models_list:
            if "generateContent" in m.supported_generation_methods and "flash" in m.name.lower():
                return genai.GenerativeModel(m.name)
        for m in models_list:
            if "generateContent" in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")

    return genai.GenerativeModel("gemini-2.0-flash")


def clean_json_response(text: str) -> str:
    # Extract json block from text
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    text = re.sub(r"```(?:json)?", "", text).strip()
    return text.rstrip("`").strip()


# Fallback responses for local testing
def generate_fallback_resume_analysis(text: str) -> dict:
    lower = text.lower()
    score = 78
    if "python" in lower: score += 4
    if "react" in lower or "javascript" in lower: score += 4
    if "sql" in lower or "database" in lower: score += 4
    score = min(score, 94)

    return {
        "ats_score": score,
        "summary": "Demonstrated full-stack technical background with strong fundamentals in modern application development, API architecture, and database interactions.",
        "strengths": [
            "Clear technical skill taxonomy with relevant modern frameworks and toolsets",
            "Demonstrated hands-on experience delivering full-stack features and API integrations",
            "Structured layout with distinct sections for experience, education, and technical core"
        ],
        "weaknesses": [
            "Bullet points could leverage more quantifiable impact metrics (e.g., % latency drop, $ revenue, user count)",
            "Some sections lack keyword density expected by modern automated ATS parsers",
            "Action verbs could be more assertive (prefer 'Architected', 'Spearheaded' over 'Assisted')"
        ],
        "improvements": [
            "Transform passive bullet points: replace 'Helped develop features' with 'Engineered 5+ microservices improving throughput by 30%'",
            "Add a dedicated Cloud & DevOps subsection highlighting Docker, CI/CD, or AWS",
            "Include quantifiable scope metrics: team size, daily active users, or queries processed"
        ],
        "keywords_missing": [
            "Docker / Containerization",
            "CI/CD Pipelines",
            "Cloud Deployment (AWS/GCP)",
            "Unit Testing (Jest/PyTest)",
            "System Architecture"
        ],
        "section_scores": {
            "experience": score - 5,
            "skills": min(score + 6, 96),
            "education": 88,
            "formatting": 80
        },
        "top_roles": [
            "Full-Stack Software Engineer",
            "Backend Python Developer",
            "Frontend / React Web Engineer"
        ],
        "one_liner_pitch": "Results-driven Software Engineer experienced in building scalable web applications and high-throughput REST APIs."
    }


def generate_fallback_job_match(resume: str, jd: str) -> dict:
    return {
        "match_score": 82,
        "verdict": "Good Match",
        "verdict_reason": "Candidate possesses strong foundational alignment with the core programming languages and architectural patterns specified in the job description.",
        "matched_skills": [
            "Python",
            "RESTful API Design",
            "Relational Databases / SQL",
            "Frontend Component Architecture",
            "Git Version Control"
        ],
        "missing_skills": [
            "Kubernetes Orchestration",
            "High-Throughput Caching (Redis)",
            "Distributed Event Streaming (Kafka)",
            "Automated E2E Testing"
        ],
        "experience_match": "Meets Requirements",
        "tailored_summary": "Versatile Software Engineer with demonstrated experience delivering scalable full-stack applications. Proven track record architecting high-throughput REST APIs, optimizing relational databases, and crafting responsive user interfaces tailored to user-centric product requirements.",
        "action_items": [
            "Incorporate target keywords (Kubernetes, Redis) into your recent project descriptions",
            "Highlight API scalability and concurrency benchmarks from previous roles",
            "Emphasize unit test coverage and automated deployment practices in your summary"
        ],
        "learning_roadmap": [
            { "skill": "Container Orchestration (Kubernetes)", "resource": "Kubernetes Official Interactive Tutorials", "time": "1-2 weeks" },
            { "skill": "In-Memory Caching (Redis)", "resource": "Redis University - Fast Track Course", "time": "3-5 days" },
            { "skill": "Distributed System Design", "resource": "System Design Primer by Donne Martin (GitHub)", "time": "1 week" }
        ],
        "salary_range": "$115,000 - $140,000 USD",
        "interview_tip": "Be prepared to walk through your API architecture on a whiteboard, specifically explaining how you handled database connection pooling and error handling."
    }


def generate_fallback_questions(job_title: str) -> dict:
    return {
        "intro": f"Welcome! We are thrilled to discuss your background for the {job_title} role. Let's explore your technical approach and past engineering challenges.",
        "questions": [
            {
                "id": 1,
                "category": "Behavioral",
                "question": "Tell me about a challenging technical deadline you faced. How did you prioritize tasks and ensure project delivery?",
                "hint": "Use the STAR method: describe the critical deadline, trade-offs made, and the measurable outcome.",
                "difficulty": "Easy"
            },
            {
                "id": 2,
                "category": "Technical",
                "question": f"How do you design a high-throughput RESTful API for a {job_title} application while ensuring low latency and data consistency?",
                "hint": "Discuss HTTP status codes, indexing, caching layers (e.g. Redis), and database connection pooling.",
                "difficulty": "Medium"
            },
            {
                "id": 3,
                "category": "Situational",
                "question": "If a critical production service starts throwing 500 Internal Server errors during peak traffic, what is your step-by-step triage strategy?",
                "hint": "Mention server logs, monitoring metrics (Datadog/CloudWatch), rollback procedures, and post-mortems.",
                "difficulty": "Hard"
            },
            {
                "id": 4,
                "category": "Technical",
                "question": "Explain the difference between synchronous and asynchronous request processing. When would you choose a background task queue?",
                "hint": "Compare blocking I/O with message queues (Celery/RabbitMQ) for long-running jobs.",
                "difficulty": "Medium"
            },
            {
                "id": 5,
                "category": "Behavioral",
                "question": "Describe a situation where you had a technical disagreement with a team member. How did you resolve it constructively?",
                "hint": "Focus on data-driven decision making, code reviews, and maintaining team velocity.",
                "difficulty": "Easy"
            },
            {
                "id": 6,
                "category": "Role-Specific",
                "question": f"What architectural patterns would you introduce in your first 90 days as a {job_title} to improve code maintainability?",
                "hint": "Discuss modularity, CI/CD automated linting, documentation, and automated test coverage.",
                "difficulty": "Hard"
            }
        ],
        "tips": [
            "Structure every behavioral answer using Situation -> Task -> Action -> Result.",
            "Quantify results whenever possible (e.g. 'reduced latency by 35%').",
            "Be transparent about trade-offs in technical architectural decisions."
        ]
    }


def generate_fallback_evaluation(question: str, answer: str) -> dict:
    word_count = len(answer.split())
    score = min(max(int(word_count / 15) + 5, 6), 9)

    return {
        "score": score,
        "grade": "Good" if score >= 7 else "Average",
        "feedback": f"Solid response that addresses the core premise of the question. You demonstrated good technical vocabulary and problem awareness. To elevate this answer to a 10/10, expand further on quantifiable business results and specific technologies used.",
        "what_worked": [
            "Directly answered the question prompt without unnecessary filler",
            "Maintained a professional, engineering-focused tone throughout the response",
            "Highlighted your personal contributions clearly"
        ],
        "what_to_improve": [
            "Incorporate measurable business metrics (e.g., % improvement, time saved, team impact)",
            "Explicitly highlight the 'Result' phase to tie back to the original business challenge"
        ],
        "ideal_answer_outline": "• Situation: Set the context, team size, and immediate obstacle.\n• Task: Specify your exact ownership and the key constraint (time/budget).\n• Action: Detail 2-3 concrete technical steps you executed.\n• Result: Share the measurable positive outcome with numbers.",
        "star_analysis": {
            "situation": "Identified context and background challenge effectively.",
            "task": "Outlined the primary objective clearly.",
            "action": "Described key implementation steps taken.",
            "result": "Could be strengthened with explicit metric numbers."
        },
        "follow_up_question": "If you had to redo that project today with modern tooling, what architecture choice would you change?"
    }


def ask_gemini(prompt: str) -> dict:
    current_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    if current_key and current_key != "your_gemini_api_key_here":
        try:
            model = get_gemini_model()
            response = model.generate_content(prompt)
            raw = clean_json_response(response.text)
            parsed = json.loads(raw)
            return parsed
        except Exception as e:
            print(f"Gemini API error: {e}")
    
    # Handle response types
    if "mock interview session" in prompt.lower() or "interview session" in prompt.lower() or "interview questions" in prompt.lower():
        title = "Software Engineer"
        match = re.search(r"JOB TITLE:\s*([^\n\r]+)", prompt)
        if match:
            title = match.group(1).strip()
        return generate_fallback_questions(title)
    elif "CANDIDATE'S ANSWER:" in prompt:
        return generate_fallback_evaluation("", prompt)
    elif "match analysis" in prompt.lower() or ("JOB DESCRIPTION:" in prompt and "verdict" in prompt):
        return generate_fallback_job_match("", "")
    elif "RESUME:" in prompt:
        return generate_fallback_resume_analysis(prompt)
    else:
        title = "Software Engineer"
        match = re.search(r"JOB TITLE:\s*([^\n\r]+)", prompt)
        if match:
            title = match.group(1).strip()
        return generate_fallback_questions(title)
