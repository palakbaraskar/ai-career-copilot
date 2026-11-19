import io
import PyPDF2
from services.gemini_service import ask_gemini, generate_fallback_resume_analysis

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Safely extract plain text from uploaded PDF bytes."""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        extracted = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted.append(text)
        return "\n".join(extracted)
    except Exception as e:
        print(f"[PDF EXTRACTION WARNING] {e}")
        try:
            return file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            return ""


def analyze_resume_text(resume_text: str) -> dict:
    """Run full ATS evaluation prompt against Gemini service."""
    prompt = f"""
You are a senior ATS (Applicant Tracking System) expert and career coach with 15+ years of experience.
Carefully analyze the following resume and return a detailed evaluation.

RESUME:
\"\"\"
{resume_text}
\"\"\"

Respond ONLY with a valid JSON object (no markdown, no explanation) using this exact schema:
{{
  "ats_score": <integer 0-100>,
  "summary": "<2-3 sentence holistic overview of this candidate>",
  "strengths": [
    "<concrete strength 1>",
    "<concrete strength 2>",
    "<concrete strength 3>"
  ],
  "weaknesses": [
    "<specific weakness 1>",
    "<specific weakness 2>",
    "<specific weakness 3>"
  ],
  "improvements": [
    "<actionable improvement 1 with example>",
    "<actionable improvement 2 with example>",
    "<actionable improvement 3 with example>"
  ],
  "keywords_missing": [
    "<important missing keyword 1>",
    "<important missing keyword 2>",
    "<important missing keyword 3>",
    "<important missing keyword 4>",
    "<important missing keyword 5>"
  ],
  "section_scores": {{
    "experience": <integer 0-100>,
    "skills": <integer 0-100>,
    "education": <integer 0-100>,
    "formatting": <integer 0-100>
  }},
  "top_roles": [
    "<best-fit role 1>",
    "<best-fit role 2>",
    "<best-fit role 3>"
  ],
  "one_liner_pitch": "<a compelling 1-sentence elevator pitch for this candidate>"
}}
"""
    try:
        return ask_gemini(prompt)
    except Exception as e:
        print(f"[RESUME SERVICE ERROR] {e}")
        return generate_fallback_resume_analysis(resume_text)
