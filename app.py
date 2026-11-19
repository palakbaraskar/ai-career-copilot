import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv

from config import Config
from db import db
from models import User

# Load environment configuration
load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable Cross-Origin Resource Sharing
    CORS(app)

    # Initialize Database with resilience
    db_initialized = False
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            db_initialized = True
            print("[DATABASE] Successfully connected and verified primary database tables!")
    except Exception as e:
        print(f"[DATABASE NOTICE] Primary database connection encountered: {e}")

    if not db_initialized:
        try:
            print("[DATABASE FALLBACK] Initializing local resilient database: sqlite:///career_copilot.db")
            if "sqlalchemy" in app.extensions:
                del app.extensions["sqlalchemy"]
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_copilot.db'
            db.init_app(app)
            with app.app_context():
                db.create_all()
                print("[DATABASE] Fallback database tables verified successfully!")
        except Exception as ex:
            print(f"[DATABASE ERROR] Could not initialize fallback: {ex}")

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Route Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.resume import resume_bp
    from routes.job_match import job_match_bp
    from routes.interview import interview_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(job_match_bp)
    app.register_blueprint(interview_bp)

    # Landing page route
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

# Main entry point instance
app = create_app()

if __name__ == '__main__':
    # Production guideline: debug=False in production, debug=True for local development
    is_debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    app.run(debug=is_debug, port=5000)
