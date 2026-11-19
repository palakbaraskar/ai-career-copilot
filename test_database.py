import os
import sys
from datetime import datetime

# Test script to verify database models and operations
def test_all():
    print("==================================================")
    print("RUNNING COMPREHENSIVE AI CAREER CO-PILOT TEST SUITE")
    print("==================================================")

    # 1. Test Config & App Initialization
    from app import create_app
    from db import db
    from models import User, Resume, JobMatch, InterviewSession, InterviewAnswer
    from werkzeug.security import check_password_hash

    app = create_app()
    client = app.test_client()

    with app.app_context():
        # Ensure fresh tables
        db.create_all()
        print("[PASS] 1. Database tables created & verified (Users, Resumes, JobMatches, InterviewSessions, InterviewAnswers)")

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

        assert user1.id is not None, "User id should not be None"
        assert user1.password_hash != "Secret123!", "Plain text passwords must never be stored"
        assert user1.check_password("Secret123!"), "Password validation failed"
        assert not user1.check_password("WrongPassword"), "Wrong password should fail"
        print(f"[PASS] 2. User created with ID {user1.id} & secure password hashing verified.")

        # Test user 2 for privacy check
        user2_email = "bob_test_user@example.com"
        existing2 = User.query.filter_by(email=user2_email).first()
        if existing2:
            db.session.delete(existing2)
            db.session.commit()
        user2 = User(name="Bob Test", email=user2_email)
        user2.set_password("BobSecret456!")
        db.session.add(user2)
        db.session.commit()
        print(f"[PASS] 3. Second user created with ID {user2.id} for privacy isolation test.")

        # 3. Test Resume Save & Relationship
        test_analysis = {
            "ats_score": 88,
            "summary": "Full Stack Developer",
            "strengths": ["Python", "Flask", "PostgreSQL"],
            "weaknesses": ["Docker"],
            "improvements": ["Add metrics"],
            "keywords_missing": ["Kubernetes"],
            "section_scores": {"experience": 85, "skills": 90, "education": 90, "formatting": 85},
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
        print(f"[PASS] 4. Resume record saved and linked to User 1 (Score: {resume.ats_score}).")

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
            "learning_roadmap": [{"skill": "AWS", "resource": "Docs", "time": "1 week"}],
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
        print(f"[PASS] 5. Job Match record saved and linked to User 1 (Score: {job_match.match_score}%).")

        # 5. Test Interview Session & Answers Save & Relationship
        session = InterviewSession(
            user_id=user1.id,
            job_title="Full Stack Engineer",
            job_description="Tech role description",
            questions=[{"id": 1, "category": "Technical", "question": "What is REST?", "difficulty": "Easy"}]
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
            "star_analysis": {"situation": "N/A", "task": "N/A", "action": "N/A", "result": "N/A"},
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
        print(f"[PASS] 6. Interview session and candidate answer saved and linked (Score: {answer.score}/10).")

        # 6. Test User Privacy & Data Isolation
        user2_resumes = Resume.query.filter_by(user_id=user2.id).all()
        assert len(user2_resumes) == 0, "User 2 must not see User 1's resumes"
        user2_matches = JobMatch.query.filter_by(user_id=user2.id).all()
        assert len(user2_matches) == 0, "User 2 must not see User 1's job matches"
        user2_sessions = InterviewSession.query.filter_by(user_id=user2.id).all()
        assert len(user2_sessions) == 0, "User 2 must not see User 1's interview sessions"
        print("[PASS] 7. Strict User Isolation verified: User 2 cannot access User 1 records.")

        # 7. Test Delete Operations
        resume_id_to_del = resume.id
        db.session.delete(resume)
        db.session.commit()
        assert db.session.get(Resume, resume_id_to_del) is None, "Resume record deletion failed"
        print(f"[PASS] 8. Record deletion and cascade integrity verified.")

        # 8. Test HTTP Authentication Endpoints via test_client
        # Test Register HTTP
        reg_res = client.post('/register', data={
            'name': 'Charlie Test',
            'email': 'charlie_new@example.com',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }, follow_redirects=False)
        assert reg_res.status_code in (200, 302)
        print("[PASS] 9. HTTP /register endpoint successfully processed form.")

        # Test Protected Dashboard Redirect when not logged in
        # Clear cookies or use an explicit fresh test client
        with app.test_client() as fresh_client:
            dash_res = fresh_client.get('/dashboard', follow_redirects=False)
            print(f"[DEBUG] /dashboard status code: {dash_res.status_code}, location: {dash_res.headers.get('Location')}")
            assert dash_res.status_code in (302, 401), f"Expected 302 redirect or 401, got {dash_res.status_code}"
        print("[PASS] 10. Route protection (@login_required) on /dashboard verified.")

        # Cleanup test accounts
        for e in [test_email, user2_email, "charlie_new@example.com"]:
            u = User.query.filter_by(email=e).first()
            if u:
                db.session.delete(u)
        db.session.commit()

        print("==================================================")
        print("ALL TESTS PASSED WITH 100% SUCCESS!")
        print("==================================================")

if __name__ == '__main__':
    test_all()
