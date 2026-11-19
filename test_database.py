import os
import sys
from datetime import datetime


def test_all():

    print("==================================================")
    print("RUNNING COMPREHENSIVE AI CAREER CO-PILOT TEST SUITE")
    print("==================================================")

# 1. Test Config & App Initialization
from app import create_app
from db import db
from models import User, Resume, JobMatch, InterviewSession, InterviewAnswer

app = create_app()

with app.app_context():

    # Ensure tables exist
    db.create_all()

    print("[PASS] 1. Database tables created & verified.")

    # 2. Test User Registration & Password Hashing
    test_email = "test_user_unique@example.com"

    existing = User.query.filter_by(email=test_email).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()

    user1 = User(name="Alice Test", email=test_email)
    user1.set_password("Secret123!")

    db.session.add(user1)
    db.session.commit()

    assert user1.id is not None
    assert user1.password_hash != "Secret123!"
    assert user1.check_password("Secret123!")
    assert not user1.check_password("WrongPassword")

    print(f"[PASS] 2. User created with ID {user1.id} & secure password hashing verified.")

    # Test User 2
    user2_email = "bob_test_user@example.com"

    existing2 = User.query.filter_by(email=user2_email).first()

    if existing2:
        db.session.delete(existing2)
        db.session.commit()

    user2 = User(name="Bob Test", email=user2_email)
    user2.set_password("BobSecret456!")

    db.session.add(user2)
    db.session.commit()

    print(f"[PASS] 3. Second user created with ID {user2.id}.")

    # 3. Test Resume Save & Relationship
    test_analysis = {
        "ats_score": 88,
        "summary": "Full Stack Developer",
        "strengths": ["Python", "Flask", "PostgreSQL"],
        "weaknesses": ["Docker"],
        "improvements": ["Add metrics"],
        "keywords_missing": ["Kubernetes"],
        "section_scores": {
            "experience": 85,
            "skills": 90,
            "education": 90,
            "formatting": 85
        },
        "top_roles": ["Full Stack Engineer"],
        "one_liner_pitch": "Experienced developer."
    }

    resume = Resume(
        user_id=user1.id,
        resume_name="Alice_Resume_2026.pdf",
        ats_score=88,
        summary="Full Stack Developer",
        analysis_result=test_analysis
    )

    db.session.add(resume)
    db.session.commit()

    assert resume.id is not None
    assert user1.resumes.count() >= 1

    print("[PASS] 4. Resume record saved and linked.")

    # 4. Test Job Match Save & Relationship
    test_match_res = {
        "match_score": 85,
        "verdict": "Good Match",
        "verdict_reason": "Skills overlap significantly",
        "matched_skills": ["Python", "SQL"],
        "missing_skills": ["AWS"],
        "experience_match": "Meets Requirements",
        "tailored_summary": "Versatile engineer",
        "action_items": ["Learn AWS"],
        "learning_roadmap": [
            {"skill": "AWS", "resource": "Docs", "time": "1 week"}
        ],
        "salary_range": "$120k",
        "interview_tip": "Prepare system design"
    }

    job_match = JobMatch(
        user_id=user1.id,
        job_title="Senior Python Engineer",
        job_description="Looking for Python and SQL developer.",
        match_score=85,
        match_result=test_match_res
    )

    db.session.add(job_match)
    db.session.commit()

    assert job_match.id is not None
    assert user1.job_matches.count() >= 1

    print("[PASS] 5. Job Match record saved and linked.")

    # 5. Test Interview Session & Answers
    session = InterviewSession(
        user_id=user1.id,
        job_title="Full Stack Engineer",
        job_description="Tech role description",
        questions=[
            {
                "id": 1,
                "category": "Technical",
                "question": "What is REST?",
                "difficulty": "Easy"
            }
        ]
    )

    db.session.add(session)
    db.session.commit()

    assert session.id is not None

    test_eval_res = {
        "score": 9,
        "grade": "Excellent",
        "feedback": "Great explanation of REST constraints.",
        "what_worked": ["Clear terms"],
        "what_to_improve": ["Give examples"],
        "ideal_answer_outline": "Explain statelessness, uniform interface.",
        "star_analysis": {
            "situation": "N/A",
            "task": "N/A",
            "action": "N/A",
            "result": "N/A"
        },
        "follow_up_question": "How about GraphQL?"
    }

    answer = InterviewAnswer(
        session_id=session.id,
        question="What is REST?",
        answer="REST stands for Representational State Transfer...",
        score=9,
        feedback="Great explanation.",
        evaluation_result=test_eval_res
    )

    db.session.add(answer)
    db.session.commit()

    assert answer.id is not None
    assert session.answers.count() == 1

    print("[PASS] 6. Interview session and answer saved.")

    # 6. Test User Privacy & Data Isolation
    user2_resumes = Resume.query.filter_by(user_id=user2.id).all()
    assert len(user2_resumes) == 0

    user2_matches = JobMatch.query.filter_by(user_id=user2.id).all()
    assert len(user2_matches) == 0

    user2_sessions = InterviewSession.query.filter_by(user_id=user2.id).all()
    assert len(user2_sessions) == 0

    print("[PASS] 7. User data isolation verified.")

    # 7. Test Delete Operations
    resume_id_to_del = resume.id

    db.session.delete(resume)
    db.session.commit()

    assert db.session.get(Resume, resume_id_to_del) is None

    print("[PASS] 8. Record deletion verified.")

    # 8. Test HTTP Registration Endpoint
    with app.test_client() as client:

        reg_res = client.post(
            '/register',
            data={
                'name': 'Charlie Test',
                'email': 'charlie_new@example.com',
                'password': 'Password123!',
                'confirm_password': 'Password123!'
            },
            follow_redirects=False
        )

        assert reg_res.status_code in (200, 302)

        print("[PASS] 9. HTTP Registration endpoint tested.")

        # 9. Test Dashboard Authentication
        # Fresh client has no logged-in session
        with app.test_client() as fresh_client:

            dash_res = fresh_client.get(
                '/dashboard',
                follow_redirects=False
            )

            print("Dashboard Status:", dash_res.status_code)
            print("Redirect Location:", dash_res.headers.get('Location'))

            assert dash_res.status_code == 302, (
                f"Dashboard should redirect unauthenticated users. "
                f"Got {dash_res.status_code}"
            )

        print("[PASS] 10. Dashboard login protection verified.")

    # Cleanup test accounts
    for email in [
        test_email,
        user2_email,
        "charlie_new@example.com"
    ]:

        user = User.query.filter_by(email=email).first()

        if user:
            db.session.delete(user)

    db.session.commit()

    print("==================================================")
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("==================================================")
if __name__ == '__main__':
 test_all()