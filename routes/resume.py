from flask import Blueprint, render_template, request, jsonify, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from services.resume_service import extract_text_from_pdf, analyze_resume_text
from models import Resume
from db import db

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/resume-analyzer')
def analyzer_page():
    return render_template('resume_analyzer.html')


@resume_bp.route('/api/analyze-resume', methods=['POST'])
def analyze_resume_api():
    resume_text = ""
    resume_name = "Uploaded Resume"

    if "file" in request.files and request.files["file"].filename:
        file = request.files["file"]
        resume_name = file.filename
        raw = file.read()
        if file.filename.lower().endswith(".pdf"):
            resume_text = extract_text_from_pdf(raw)
        else:
            resume_text = raw.decode("utf-8", errors="ignore")
    elif request.form.get("text"):
        resume_text = request.form["text"]
        resume_name = "Pasted Resume Text"
    elif request.is_json:
        resume_text = request.json.get("text", "")
        resume_name = request.json.get("name", "Resume Submission")

    if not resume_text.strip():
        return jsonify({"error": "No resume content provided"}), 400

    # Execute ATS analysis via service
    result = analyze_resume_text(resume_text)

    # If the user is authenticated, automatically save analysis to database!
    saved_record_id = None
    if current_user.is_authenticated:
        try:
            new_record = Resume(
                user_id=current_user.id,
                resume_name=resume_name[:250],
                ats_score=int(result.get("ats_score", 0)),
                summary=result.get("summary", "")[:1000],
                analysis_result=result
            )
            db.session.add(new_record)
            db.session.commit()
            saved_record_id = new_record.id
            result["saved_to_db"] = True
            result["record_id"] = saved_record_id
        except Exception as e:
            db.session.rollback()
            print(f"[SAVE RESUME DB ERROR] {e}")
            result["saved_to_db"] = False

    return jsonify(result)


@resume_bp.route('/resume/view/<int:resume_id>')
@login_required
def view_resume(resume_id):
    # Enforce strict user ownership
    resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
    return render_template('view_resume.html', resume=resume)


@resume_bp.route('/resume/delete/<int:resume_id>', methods=['POST'])
@login_required
def delete_resume(resume_id):
    resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
    try:
        db.session.delete(resume)
        db.session.commit()
        flash('Resume analysis record deleted successfully.', 'info')
    except Exception as e:
        db.session.rollback()
        print(f"[DELETE RESUME ERROR] {e}")
        flash('Failed to delete record from database.', 'error')

    return redirect(url_for('dashboard.user_dashboard'))
