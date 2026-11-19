import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "career-copilot-dev-secret-key-2026")
    
    # Database Configuration
    raw_db_url = os.getenv("DATABASE_URL", "").strip()
    if raw_db_url:
        # Standardize prefix for SQLAlchemy and psycopg2
        if raw_db_url.startswith("postgres://"):
            raw_db_url = raw_db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif raw_db_url.startswith("postgresql://") and not raw_db_url.startswith("postgresql+"):
            raw_db_url = raw_db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

        # Handle passwords containing special characters (e.g. '@', '%')
        try:
            prefix, rest = raw_db_url.split("://", 1)
            if "@" in rest:
                last_at = rest.rfind("@")
                user_pass = rest[:last_at]
                host_db = rest[last_at + 1:]
                if ":" in user_pass:
                    user, pwd = user_pass.split(":", 1)
                    # URL-encode password cleanly
                    encoded_pwd = urllib.parse.quote_plus(urllib.parse.unquote_plus(pwd))
                    raw_db_url = f"{prefix}://{user}:{encoded_pwd}@{host_db}"
        except Exception as e:
            print(f"[CONFIG URL PARSE WARNING] {e}")

        SQLALCHEMY_DATABASE_URI = raw_db_url
    else:
        # Default local PostgreSQL with explicit psycopg2 driver
        SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/career_copilot_db"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
