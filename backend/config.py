class Config:
    SECRET_KEY = "super-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///Database.db"
    SECURITY_PASSWORD_SALT = "hahahahah"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Only for development/testing
    # SECURITY_REGISTERABLE = False
