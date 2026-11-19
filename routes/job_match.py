from flask import Blueprint, render_template, request, jsonify, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from services.job_match_service import match_job_description
from models import JobMatch
from db import db

job_match_bp = Blueprint('job_match', __name__)

@job_match_bp.route('/job-matcher')
def matcher_page():
    return render_template('job_matcher.html')


@job_match_bp.route('/api/match-job', methods=['POST'])
def match_job_api():
    data = request.get_json(silent=True) or {}
    resume_text = data.get("resume", "").strip()
    job_description = data.get("job_description", "").strip()
    job_title = data.get("job_title", "").strip()

    if not resume_text or not job_description:
        return jsonify({"error": "Both resume and job description are required"}), 400

    # Auto-extract job title from first line of job description if not provided
    if not job_title:
        first_line = job_description.strip().splitlines()[0]
        job_title = first_line[:120].strip() or "Target Role"

    # Execute match analysis via service
    result = match_job_description(resume_text, job_description)

    # If the user is authenticated, automatically save match record to database!
    if current_user.is_authenticated:
        try:
            new_record = JobMatch(
                user_id=current_user.id,
                job_title=job_title[:250],
                job_description=job_description[:3000],
                match_score=int(result.get("match_score", 0)),
                match_result=result
            )
            db.session.add(new_record)
            db.session.commit()
            result["saved_to_db"] = True
            result["record_id"] = new_record.id
        except Exception as e:
            db.session.rollback()
            print(f"[SAVE JOB MATCH DB ERROR] {e}")
            result["saved_to_db"] = False

    return jsonify(result)


@job_match_bp.route('/job-match/view/<int:match_id>')
@login_required
def view_job_match(match_id):
    # Enforce strict user ownership
    match_record = JobMatch.query.filter_by(id=match_id, user_id=current_user.id).first_or_404()
    return render_template('view_job_match.html', match_record=match_record)


@job_match_bp.route('/job-match/delete/<int:match_id>', methods=['POST'])
@login_required
def delete_job_match(match_id):
    match_record = JobMatch.query.filter_by(id=match_id, user_id=current_user.id).first_or_404()
    try:
        db.session.delete(match_record)
        db.session.commit()
        flash('Job match record deleted successfully.', 'info')
    except Exception as e:
        db.session.rollback()
        print(f"[DELETE JOB MATCH ERROR] {e}")
        flash('Failed to delete record from database.', 'error')

    return redirect(url_for('dashboard.user_dashboard'))
