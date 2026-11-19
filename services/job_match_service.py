from services.gemini_service import ask_gemini, generate_fallback_job_match

def match_job_description(resume_text: str, job_description: str) -> dict:
    """Run full job matching & gap analysis prompt against Gemini service."""
    prompt = f"""
You are a senior technical recruiter and career strategist.
Compare the resume against the job description and provide a comprehensive match analysis.

RESUME:
\"\"\"
{resume_text}
\"\"\"

JOB DESCRIPTION:
\"\"\"
{job_description}
\"\"\"

Respond ONLY with a valid JSON object (no markdown, no explanation) using this exact schema:
{{
  "match_score": <integer 0-100>,
  "verdict": "<one of: Excellent Match | Good Match | Partial Match | Poor Match>",
  "verdict_reason": "<2 sentence explanation of the verdict>",
  "matched_skills": [
    "<matched skill/keyword 1>",
    "<matched skill/keyword 2>",
    "<matched skill/keyword 3>"
  ],
  "missing_skills": [
    "<missing skill 1>",
    "<missing skill 2>",
    "<missing skill 3>",
    "<missing skill 4>"
  ],
  "experience_match": "<one of: Exceeds Requirements | Meets Requirements | Below Requirements>",
  "tailored_summary": "<a rewritten professional summary (3-4 sentences) specifically tailored for this role, written in first person>",
  "action_items": [
    "<specific action item 1>",
    "<specific action item 2>",
    "<specific action item 3>"
  ],
  "learning_roadmap": [
    {{ "skill": "<skill name>", "resource": "<specific course/book/platform>", "time": "<estimated time>" }},
    {{ "skill": "<skill name>", "resource": "<specific course/book/platform>", "time": "<estimated time>" }},
    {{ "skill": "<skill name>", "resource": "<specific course/book/platform>", "time": "<estimated time>" }}
  ],
  "salary_range": "<estimated salary range for this role in USD>",
  "interview_tip": "<one insider tip for interviewing for this specific role>"
}}
"""
    try:
        return ask_gemini(prompt)
    except Exception as e:
        print(f"[JOB MATCH SERVICE ERROR] {e}")
        return generate_fallback_job_match(resume_text, job_description)
