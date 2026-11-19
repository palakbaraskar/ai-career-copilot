from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from models import Resume, JobMatch, InterviewSession, InterviewAnswer
from db import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def user_dashboard():   
    user_resumes = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.created_at.desc()).all()
    user_matches = JobMatch.query.filter_by(user_id=current_user.id).order_by(JobMatch.created_at.desc()).all()
    user_sessions = InterviewSession.query.filter_by(user_id=current_user.id).order_by(InterviewSession.created_at.desc()).all()

    total_resumes = len(user_resumes)
    avg_ats_score = round(sum(r.ats_score for r in user_resumes) / total_resumes) if total_resumes > 0 else 0

    total_matches = len(user_matches)
    avg_match_score = round(sum(m.match_score for m in user_matches) / total_matches) if total_matches > 0 else 0

    total_interviews = len(user_sessions)

    activities = []
    for r in user_resumes[:5]:
        activities.append({
            'type': 'resume',
            'title': f'Analyzed Resume: {r.resume_name}',
            'score': f'{r.ats_score}/100 ATS Score',
            'date': r.created_at,
            'id': r.id,
            'url': f'/resume/view/{r.id}'
        })
    for m in user_matches[:5]:
        activities.append({
            'type': 'match',
            'title': f'Matched Role: {m.job_title}',
            'score': f'{m.match_score}% Match',
            'date': m.created_at,
            'id': m.id,
            'url': f'/job-match/view/{m.id}'
        })
    for s in user_sessions[:5]:
        answer_count = s.answers.count()
        activities.append({
            'type': 'interview',
            'title': f'Interview Session: {s.job_title}',
            'score': f'{answer_count} Answers Evaluated',
            'date': s.created_at,
            'id': s.id,
            'url': f'/interview/view/{s.id}'
        })
    activities.sort(key=lambda x: x['date'], reverse=True)
    recent_activities = activities[:8]

    return render_template(
        'dashboard.html',
        total_resumes=total_resumes,
        avg_ats_score=avg_ats_score,
        total_matches=total_matches,
        avg_match_score=avg_match_score,
        total_interviews=total_interviews,
        user_resumes=user_resumes,
        user_matches=user_matches,
        user_sessions=user_sessions,
        recent_activities=recent_activities
    )
