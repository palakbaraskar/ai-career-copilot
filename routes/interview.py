from flask import Blueprint, render_template, request, jsonify, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from services.gemini_service import ask_gemini, generate_fallback_questions, generate_fallback_evaluation
from models import InterviewSession, InterviewAnswer
from db import db

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/interview-prep')
def prep_page():
    return render_template('interview_prep.html')


@interview_bp.route('/api/generate-questions', methods=['POST'])
def generate_questions_api():
    data = request.get_json(silent=True) or {}
    job_title = data.get("job_title", "").strip()
    job_description = data.get("job_description", "").strip()
    resume_text = data.get("resume", "").strip()

    if not job_title:
        return jsonify({"error": "Job title is required"}), 400

    prompt = f"""
You are a senior technical interviewer at a top tech company.
Generate a comprehensive, realistic mock interview session.

JOB TITLE: {job_title}
JOB DESCRIPTION: {job_description if job_description else "Not provided — use job title context."}
CANDIDATE RESUME: {resume_text if resume_text else "Not provided — generate general questions for the role."}

Respond ONLY with a valid JSON object (no markdown, no explanation) using this exact schema:
{{
  "intro": "<a friendly 1-sentence intro message from the interviewer>",
  "questions": [
    {{
      "id": 1,
      "category": "Behavioral",
      "question": "<full question text>",
      "hint": "<what a great answer should cover, in 1 sentence>",
      "difficulty": "Easy"
    }},
    {{
      "id": 2,
      "category": "Technical",
      "question": "<full question text>",
      "hint": "<what a great answer should cover>",
      "difficulty": "Medium"
    }},
    {{
      "id": 3,
      "category": "Situational",
      "question": "<full question text>",
      "hint": "<what a great answer should cover>",
      "difficulty": "Medium"
    }},
    {{
      "id": 4,
      "category": "Technical",
      "question": "<full question text>",
      "hint": "<what a great answer should cover>",
      "difficulty": "Hard"
    }},
    {{
      "id": 5,
      "category": "Behavioral",
      "question": "<full question text>",
      "hint": "<what a great answer should cover>",
      "difficulty": "Easy"
    }},
    {{
      "id": 6,
      "category": "Role-Specific",
      "question": "<full question text specific to this role>",
      "hint": "<what a great answer should cover>",
      "difficulty": "Hard"
    }}
  ],
  "tips": [
    "<interview tip 1 specific to this role>",
    "<interview tip 2>",
    "<interview tip 3>"
  ]
}}
"""

    try:
        result = ask_gemini(prompt)
    except Exception as e:
        print(f"[GENERATE QUESTIONS ERROR] {e}")
        result = generate_fallback_questions(job_title)

    # If the user is authenticated, save the session to database
    if current_user.is_authenticated:
        try:
            session_record = InterviewSession(
                user_id=current_user.id,
                job_title=job_title[:250],
                job_description=job_description[:3000] if job_description else "",
                questions=result.get("questions", [])
            )
            db.session.add(session_record)
            db.session.commit()
            result["saved_to_db"] = True
            result["session_id"] = session_record.id
        except Exception as e:
            db.session.rollback()
            print(f"[SAVE INTERVIEW SESSION DB ERROR] {e}")
            result["saved_to_db"] = False

    return jsonify(result)


@interview_bp.route('/api/evaluate-answer', methods=['POST'])
def evaluate_answer_api():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    answer = data.get("answer", "").strip()
    job_title = data.get("job_title", "").strip()
    category = data.get("category", "General")
    session_id = data.get("session_id")

    if not question or not answer:
        return jsonify({"error": "Question and answer are required"}), 400

    prompt = f"""
You are a senior interviewer evaluating a candidate's response during a mock interview.

JOB TITLE: {job_title}
QUESTION CATEGORY: {category}
QUESTION: {question}
CANDIDATE'S ANSWER: {answer}

Evaluate the answer thoroughly. For behavioral questions, check if STAR method was used.
For technical questions, check correctness and depth.

Respond ONLY with a valid JSON object (no markdown, no explanation) using this exact schema:
{{
  "score": <integer 0-10>,
  "grade": "<one of: Excellent | Good | Average | Needs Improvement>",
  "feedback": "<3-4 sentences of constructive, specific feedback>",
  "what_worked": [
    "<specific thing that worked well 1>",
    "<specific thing that worked well 2>"
  ],
  "what_to_improve": [
    "<specific improvement 1>",
    "<specific improvement 2>"
  ],
  "ideal_answer_outline": "<a brief outline of what a perfect answer would include (3-4 bullet points as a single string with \\n)>",
  "star_analysis": {{
    "situation": "<was situation clearly defined? yes/no + comment>",
    "task": "<was the task/challenge clear? yes/no + comment>",
    "action": "<were specific actions described? yes/no + comment>",
    "result": "<was a measurable result given? yes/no + comment>"
  }},
  "follow_up_question": "<a likely follow-up question the interviewer might ask>"
}}
"""

    try:
        result = ask_gemini(prompt)
    except Exception as e:
        print(f"[EVALUATE ANSWER ERROR] {e}")
        result = generate_fallback_evaluation(question, answer)

    # If the user is authenticated, save the answer under the session
    if current_user.is_authenticated:
        try:
            # If session_id is provided, verify ownership
            target_session = None
            if session_id:
                target_session = InterviewSession.query.filter_by(id=session_id, user_id=current_user.id).first()

            # If not provided, link to the user's latest session or create one
            if not target_session:
                target_session = InterviewSession.query.filter_by(user_id=current_user.id).order_by(InterviewSession.created_at.desc()).first()

            if not target_session:
                target_session = InterviewSession(
                    user_id=current_user.id,
                    job_title=job_title or "Technical Role",
                    job_description="",
                    questions=[]
                )
                db.session.add(target_session)
                db.session.commit()

            answer_record = InterviewAnswer(
                session_id=target_session.id,
                question=question,
                answer=answer,
                score=int(result.get("score", 0)),
                feedback=result.get("feedback", ""),
                evaluation_result=result
            )
            db.session.add(answer_record)
            db.session.commit()
            result["saved_to_db"] = True
            result["answer_id"] = answer_record.id
            result["session_id"] = target_session.id
        except Exception as e:
            db.session.rollback()
            print(f"[SAVE INTERVIEW ANSWER DB ERROR] {e}")
            result["saved_to_db"] = False

    return jsonify(result)


@interview_bp.route('/interview/view/<int:session_id>')
@login_required
def view_interview_session(session_id):
    # Enforce strict user ownership
    session_record = InterviewSession.query.filter_by(id=session_id, user_id=current_user.id).first_or_404()
    answers = session_record.answers.order_by(InterviewAnswer.created_at.asc()).all()
    return render_template('view_interview.html', session_record=session_record, answers=answers)


@interview_bp.route('/interview/delete/<int:session_id>', methods=['POST'])
@login_required
def delete_interview_session(session_id):
    session_record = InterviewSession.query.filter_by(id=session_id, user_id=current_user.id).first_or_404()
    try:
        db.session.delete(session_record)
        db.session.commit()
        flash('Interview session and all associated answers deleted.', 'info')
    except Exception as e:
        db.session.rollback()
        print(f"[DELETE INTERVIEW ERROR] {e}")
        flash('Failed to delete interview session from database.', 'error')

    return redirect(url_for('dashboard.user_dashboard'))
